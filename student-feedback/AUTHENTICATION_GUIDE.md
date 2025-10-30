# 🔐 Authentication Guide - Student Feedback System

## Overview

This application now includes **JWT-based user authentication** to secure the feedback management system. Users must register and login to submit, view, or delete feedback.

---

## 🎯 Features

✅ **User Registration** - Create new accounts with username and password  
✅ **User Login** - Secure login with JWT token generation  
✅ **Protected Endpoints** - All feedback operations require authentication  
✅ **Token-Based Security** - 24-hour expiring JWT tokens  
✅ **Password Hashing** - Bcrypt encryption for secure password storage  
✅ **Session Management** - Automatic logout on token expiration  

---

## 📋 How It Works

### 1. **User Registration Flow**

1. Open `auth.html` in your browser
2. Click on the **Register** tab
3. Fill in:
   - Username (minimum 3 characters)
   - Email (optional)
   - Password (minimum 6 characters)
   - Confirm Password
4. Click **Register**
5. Upon success, you'll be redirected to login

**API Endpoint:** `POST /register`

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": "user_id_here",
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

---

### 2. **User Login Flow**

1. Open `auth.html` in your browser
2. Enter your **Username** and **Password**
3. Click **Login**
4. Upon success:
   - JWT token is stored in localStorage
   - Redirected to `index.html` (main feedback page)

**API Endpoint:** `POST /login`

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "secure123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user_id_here",
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

---

### 3. **Protected Feedback Operations**

All feedback endpoints now require authentication:

#### **Get All Feedback** - `GET /feedback`
**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

#### **Submit Feedback** - `POST /feedback`
**Headers:**
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

**Body:**
```json
{
  "student_name": "John Doe",
  "comment": "Great course!",
  "rating": 5
}
```

#### **Delete Feedback** - `DELETE /feedback/<id>`
**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

---

## 🔧 Technical Details

### **Backend (Flask)**

1. **JWT Token Generation:**
   - Uses `PyJWT` library
   - Token expires in 24 hours
   - Contains user_id and username in payload

2. **Password Security:**
   - Uses `bcrypt` for password hashing
   - Passwords are never stored in plain text
   - Salt automatically generated for each password

3. **Authentication Decorator:**
   ```python
   @token_required
   def protected_endpoint(current_user):
       # Only accessible with valid JWT token
       pass
   ```

4. **Secret Key Configuration:**
   - Set in `app.config['SECRET_KEY']`
   - Change in production via environment variable

### **Frontend (HTML/JavaScript)**

1. **Token Storage:**
   - Stored in `localStorage.getItem('authToken')`
   - Persists across browser sessions

2. **Automatic Redirect:**
   - Checks authentication on page load
   - Redirects to `auth.html` if no token

3. **API Requests:**
   - All requests include `Authorization: Bearer <token>` header
   - Handles 401 errors (expired/invalid token)

---

## 🚀 Quick Start

### **Step 1: Update Environment Variables**

Add to your `.env` file:
```bash
SECRET_KEY=your-super-secret-key-change-in-production
```

### **Step 2: Install Dependencies**

```bash
pip install PyJWT==2.8.0 bcrypt==4.1.2
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

### **Step 3: Start Backend**

```bash
cd student-feedback/backend
python app.py
```

### **Step 4: Open Frontend**

1. Open `frontend/auth.html` in browser
2. Register a new account
3. Login with your credentials
4. Start using the feedback system!

---

## 🧪 Testing Authentication

### **1. Test Registration API**

```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123"
  }'
```

### **2. Test Login API**

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test123"
  }'
```

**Save the token from response!**

### **3. Test Protected Endpoint**

```bash
curl -X GET http://localhost:5000/feedback \
  -H "Authorization: Bearer <your_token_here>"
```

### **4. Test Token Expiration**

Wait 24 hours or decode the token at [jwt.io](https://jwt.io) to check expiration.

---

## 🛡️ Security Best Practices

### **For Development:**
✅ Use the default secret key  
✅ Test with localhost  
✅ Check browser console for token issues

### **For Production:**
⚠️ **Change SECRET_KEY** - Use a strong random string  
⚠️ **Use HTTPS** - Never send tokens over HTTP  
⚠️ **Validate Inputs** - Check username/password formats  
⚠️ **Limit Login Attempts** - Prevent brute force attacks  
⚠️ **Store Tokens Securely** - Consider httpOnly cookies  
⚠️ **Rotate Keys** - Change secret key periodically  

---

## 🐛 Troubleshooting

### **"Token is missing" Error**
- You're not logged in
- Token was deleted from localStorage
- **Solution:** Login again

### **"Token has expired" Error**
- Your session expired (24 hours)
- **Solution:** Login again

### **"Invalid token" Error**
- Token was corrupted
- Secret key changed on server
- **Solution:** Login again

### **"Username already exists" Error**
- Username is taken
- **Solution:** Choose a different username

### **"Invalid username or password" Error**
- Wrong credentials
- **Solution:** Check your username and password

---

## 📁 File Structure

```
student-feedback/
├── backend/
│   ├── app.py                 # Updated with authentication
│   ├── requirements.txt       # Added PyJWT, bcrypt
│   └── .env                   # Add SECRET_KEY here
├── frontend/
│   ├── index.html            # Protected main page
│   └── auth.html             # New login/register page
└── AUTHENTICATION_GUIDE.md   # This file
```

---

## 🔄 Database Collections

### **users** Collection (MongoDB)
```json
{
  "_id": "ObjectId",
  "username": "john_doe",
  "password": "$2b$12$hashed_password_here",
  "email": "john@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### **feedbacks** Collection (MongoDB)
```json
{
  "_id": "ObjectId",
  "student_name": "John Doe",
  "comment": "Great course!",
  "rating": 5,
  "created_at": "2024-01-01T00:00:00Z",
  "created_by": "user_id_here"
}
```

---

## 🎓 Learning Points

1. **JWT Tokens** - Stateless authentication mechanism
2. **Password Hashing** - Never store plain text passwords
3. **Bearer Authentication** - Standard HTTP authentication
4. **Token Expiration** - Security through time-limited access
5. **localStorage** - Browser storage for client-side tokens

---

## 📚 API Documentation

### Updated Endpoints:

| Method | Endpoint | Auth Required | Description |
|--------|----------|--------------|-------------|
| GET | `/` | ❌ No | API information |
| POST | `/register` | ❌ No | Register new user |
| POST | `/login` | ❌ No | Login user |
| GET | `/feedback` | ✅ Yes | Get all feedback |
| POST | `/feedback` | ✅ Yes | Submit feedback |
| DELETE | `/feedback/<id>` | ✅ Yes | Delete feedback |

---

## 🎉 Success!

You now have a fully secured Student Feedback System with user authentication! 🔐

**Next Steps:**
1. Deploy to Railway with new dependencies
2. Add more user features (profile, password reset)
3. Implement role-based access (admin, student)
4. Add user activity logs

---

**Created by:** GitHub Copilot 🤖  
**Version:** 2.0.0 with Authentication  
**Last Updated:** 2024
