"""
Student Feedback Management System - Flask API with MongoDB
A simple REST API for collecting and managing student feedback
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os

app = Flask(__name__)

# Enable CORS for all routes - allow all origins for development
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False
    }
})

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'student_feedback_db')

# Initialize MongoDB connection
try:
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    feedback_collection = db['feedbacks']
    print(f"✅ Connected to MongoDB: {DATABASE_NAME}")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")
    print("⚠️  Running without database - data will be lost on restart")
    client = None
    db = None
    feedback_collection = None

# Fallback in-memory storage if MongoDB is not available
feedback_list = []
feedback_id_counter = 1


@app.route('/')
def home():
    """API home endpoint - shows API information"""
    return jsonify({
        "message": "🎓 Student Feedback Management API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /feedback": "Get all feedback",
            "POST /feedback": "Add new feedback",
            "DELETE /feedback/<id>": "Delete feedback by ID"
        }
    })


@app.route('/feedback', methods=['GET'])
def get_feedback():
    """Get all feedback entries"""
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
def add_feedback():
    """Add new feedback"""
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
        "created_at": datetime.now().isoformat()
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
def delete_feedback(feedback_id):
    """Delete feedback by ID"""
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
