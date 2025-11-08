"""
Student Feedback Management System - Flask API with MongoDB and Authentication
A simple REST API for collecting and managing student feedback with user authentication
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import os
import jwt
import bcrypt
from functools import wraps

app = Flask(__name__)

# Secret key for JWT
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Enable CORS for all routes - allow all origins for development
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "DELETE", "OPTIONS", "PUT"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False
    }
})

# MongoDB Configuration
# Default to localhost for development/CI. In production, set MONGODB_URI to your
# Atlas connection string via environment variables or secrets. Do NOT commit
# production credentials into the repository.
#
# Note: GitHub Actions service host for the mongodb service below will be
# reachable at 'mongodb' (service name). In CI we set MONGODB_URI accordingly.
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'student_feedback_db')

# Initialize MongoDB connection
feedback_collection = None
users_collection = None
client = None

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Test the connection
    client.admin.command('ping')
    db = client[DATABASE_NAME]
    feedback_collection = db['feedbacks']
    users_collection = db['users']
    print(f"✅ Connected to MongoDB: {DATABASE_NAME}")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")
    print("⚠️  Running without database - using in-memory storage")
    feedback_collection = None
    users_collection = None
    client = None

# Fallback in-memory storage if MongoDB is not available
feedback_list = []
users_list = []
feedback_id_counter = 1


# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer TOKEN
            except IndexError:
                return jsonify({'success': False, 'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'success': False, 'error': 'Token is missing'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated


@app.route('/')
def home():
    """API home endpoint - shows API information"""
    return jsonify({
        "message": "🎓 Student Feedback Management API",
        "status": "running",
        "version": "2.0.0",
        "endpoints": {
            "GET /": "API information",
            "POST /register": "Register new user",
            "POST /login": "Login user",
            "GET /feedback": "Get all feedback (requires auth)",
            "POST /feedback": "Add new feedback (requires auth)",
            "DELETE /feedback/<id>": "Delete feedback by ID (requires auth)"
        }
    })


# ============================================
# AUTHENTICATION ENDPOINTS
# ============================================

@app.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'Username and password are required'
            }), 400
        
        username = data.get('username').strip()
        password = data.get('password')
        email = data.get('email', '').strip()
        
        if len(username) < 3:
            return jsonify({
                'success': False,
                'error': 'Username must be at least 3 characters'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'success': False,
                'error': 'Password must be at least 6 characters'
            }), 400
        
        # Check if user already exists
        if users_collection is not None:
            # MongoDB version
            existing_user = users_collection.find_one({'username': username})
            if existing_user:
                return jsonify({
                    'success': False,
                    'error': 'Username already exists'
                }), 409
            
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create user
            new_user = {
                'username': username,
                'password': hashed_password,
                'email': email,
                'created_at': datetime.utcnow()
            }
            
            result = users_collection.insert_one(new_user)
            user_id = str(result.inserted_id)
        else:
            # In-memory version
            existing_user = next((u for u in users_list if u['username'] == username), None)
            if existing_user:
                return jsonify({
                    'success': False,
                    'error': 'Username already exists'
                }), 409
            
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create user
            user_id = len(users_list) + 1
            new_user = {
                'id': user_id,
                'username': username,
                'password': hashed_password,
                'email': email,
                'created_at': datetime.utcnow().isoformat()
            }
            users_list.append(new_user)
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': {
                'id': user_id,
                'username': username,
                'email': email
            }
        }), 201
        
    except Exception as e:
        print(f"Registration Error: {e}")
        return jsonify({
            'success': False,
            'error': f'Server error during registration: {str(e)}'
        }), 500


@app.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'Username and password are required'
            }), 400
        
        username = data.get('username').strip()
        password = data.get('password')
        
        # Find user
        user = None
        if users_collection is not None:
            # MongoDB version
            user = users_collection.find_one({'username': username})
            if user:
                user_id = str(user['_id'])
        else:
            # In-memory version
            user = next((u for u in users_list if u['username'] == username), None)
            if user:
                user_id = user['id']
        
        # Check if user exists
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid username or password'
            }), 401
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return jsonify({
                'success': False,
                'error': 'Invalid username or password'
            }), 401
        
        # Generate JWT token (expires in 24 hours)
        token = jwt.encode({
            'user_id': user_id,
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user_id,
                'username': username,
                'email': user.get('email', '')
            }
        }), 200
        
    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify({
            'success': False,
            'error': f'Server error during login: {str(e)}'
        }), 500


# ============================================
# FEEDBACK ENDPOINTS (PROTECTED)
# ============================================

@app.route('/feedback', methods=['GET'])
@token_required
def get_feedback(current_user):
    """Get all feedback entries (requires authentication)"""
    try:
        if feedback_collection is not None:
            # MongoDB version
            feedbacks = list(feedback_collection.find())
            # Convert ObjectId to string for JSON serialization
            for feedback in feedbacks:
                feedback['_id'] = str(feedback['_id'])
            
            return jsonify({
                "success": True,
                "count": len(feedbacks),
                "data": feedbacks,
                "source": "mongodb"
            }), 200
        else:
            # Fallback to in-memory storage
            return jsonify({
                "success": True,
                "count": len(feedback_list),
                "data": feedback_list,
                "source": "memory"
            }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/feedback', methods=['POST'])
@token_required
def add_feedback(current_user):
    """Add new feedback (requires authentication)"""
    global feedback_id_counter
    
    # Get JSON data from request
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400
    
    if 'student_name' not in data or not data['student_name']:
        return jsonify({
            "success": False,
            "error": "student_name is required"
        }), 400
    
    if 'comment' not in data or not data['comment']:
        return jsonify({
            "success": False,
            "error": "comment is required"
        }), 400
    
    # Create feedback object
    feedback = {
        "student_name": data['student_name'],
        "comment": data['comment'],
        "rating": data.get('rating', 0),
        "created_at": datetime.now().isoformat(),
        "created_by": current_user
    }
    
    try:
        if feedback_collection is not None:
            # MongoDB version
            result = feedback_collection.insert_one(feedback)
            feedback['_id'] = str(result.inserted_id)
            feedback['id'] = str(result.inserted_id)
            
            return jsonify({
                "success": True,
                "message": "Feedback added successfully to MongoDB",
                "data": feedback
            }), 201
        else:
            # Fallback to in-memory storage
            feedback['id'] = feedback_id_counter
            feedback_list.append(feedback)
            feedback_id_counter += 1
            
            return jsonify({
                "success": True,
                "message": "Feedback added successfully (memory)",
                "data": feedback
            }), 201
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/feedback/<string:feedback_id>', methods=['DELETE'])
@token_required
def delete_feedback(current_user, feedback_id):
    """Delete feedback by ID (requires authentication)"""
    global feedback_list
    
    try:
        if feedback_collection is not None:
            # MongoDB version
            try:
                result = feedback_collection.delete_one({"_id": ObjectId(feedback_id)})
                
                if result.deleted_count > 0:
                    return jsonify({
                        "success": True,
                        "message": f"Feedback with ID {feedback_id} deleted successfully"
                    }), 200
                else:
                    return jsonify({
                        "success": False,
                        "error": f"Feedback with ID {feedback_id} not found"
                    }), 404
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": f"Invalid ID format: {str(e)}"
                }), 400
        else:
            # Fallback to in-memory storage
            try:
                feedback_id_int = int(feedback_id)
                initial_length = len(feedback_list)
                feedback_list = [f for f in feedback_list if f.get('id') != feedback_id_int]
                
                if len(feedback_list) < initial_length:
                    return jsonify({
                        "success": True,
                        "message": f"Feedback with ID {feedback_id} deleted successfully"
                    }), 200
                else:
                    return jsonify({
                        "success": False,
                        "error": f"Feedback with ID {feedback_id} not found"
                    }), 404
            except ValueError:
                return jsonify({
                    "success": False,
                    "error": "Invalid ID format"
                }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    # Get port from environment variable (Railway/Heroku) or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    print("🚀 Starting Student Feedback API...")
    print(f"📝 API will be available at http://0.0.0.0:{port}")
    print(f"📚 Visit http://0.0.0.0:{port} for API documentation")
    
    # Use debug=False for production
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
