# 🗄️ MongoDB Setup Guide for Student Feedback System

## Option 1: Install MongoDB Locally (Recommended for Development)

### Step 1: Download MongoDB
1. Go to: https://www.mongodb.com/try/download/community
2. Select:
   - Version: Latest
   - Platform: Windows
   - Package: MSI
3. Click **Download**

### Step 2: Install MongoDB
1. Run the downloaded `.msi` file
2. Choose **Complete** installation
3. **Important:** Check "Install MongoDB as a Service"
4. Keep all default settings
5. Click **Install**

### Step 3: Verify Installation
Open PowerShell and run:
```powershell
mongod --version
```

You should see the MongoDB version.

### Step 4: Start MongoDB Service
```powershell
# Start MongoDB service
net start MongoDB

# Check if it's running
Get-Service MongoDB
```

---

## Option 2: Use MongoDB Atlas (Free Cloud Database)

### Step 1: Create Account
1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Sign up for free
3. Choose **Free Shared Cluster** (M0)

### Step 2: Create Cluster
1. Select **AWS** as provider
2. Choose closest region
3. Click **Create Cluster** (takes 3-5 minutes)

### Step 3: Create Database User
1. Go to **Database Access** → **Add New Database User**
2. Username: `student_feedback_user`
3. Password: Create a strong password (save it!)
4. User Privileges: **Read and write to any database**
5. Click **Add User**

### Step 4: Whitelist IP Address
1. Go to **Network Access** → **Add IP Address**
2. Click **Allow Access from Anywhere** (0.0.0.0/0)
3. Click **Confirm**

### Step 5: Get Connection String
1. Go to **Database** → Click **Connect**
2. Choose **Connect your application**
3. Copy the connection string
4. Replace `<password>` with your actual password

Example:
```
mongodb+srv://student_feedback_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### Step 6: Update .env File
Edit `backend/.env`:
```
MONGODB_URI=mongodb+srv://student_feedback_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=student_feedback_db
```

---

## Install Python MongoDB Driver

```powershell
cd D:\projects\DevOps\student-feedback\backend
pip install -r requirements.txt
```

---

## Start Your Application

```powershell
cd D:\projects\DevOps\student-feedback\backend
python app.py
```

You should see:
```
✅ Connected to MongoDB: student_feedback_db
🚀 Starting Student Feedback API...
```

---

## Test MongoDB Connection

### Using MongoDB Shell (if installed locally)
```powershell
# Connect to MongoDB
mongosh

# Show databases
show dbs

# Use your database
use student_feedback_db

# Show collections
show collections

# View all feedback
db.feedbacks.find().pretty()

# Count documents
db.feedbacks.countDocuments()

# Delete all (for testing)
db.feedbacks.deleteMany({})
```

### Using Python Script
Create `test_mongodb.py`:
```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['student_feedback_db']
collection = db['feedbacks']

# Test insert
result = collection.insert_one({
    "student_name": "Test User",
    "comment": "Testing MongoDB",
    "rating": 5
})

print(f"✅ Inserted ID: {result.inserted_id}")

# Test find
feedbacks = list(collection.find())
print(f"📊 Total feedback: {len(feedbacks)}")
```

Run it:
```powershell
python test_mongodb.py
```

---

## Troubleshooting

### Problem: MongoDB service not running
```powershell
# Start the service
net start MongoDB
```

### Problem: Connection timeout
- Check if MongoDB is running: `Get-Service MongoDB`
- Check firewall settings
- For Atlas: Verify IP whitelist

### Problem: Authentication failed
- Verify username and password in connection string
- Check database user permissions

### Problem: Module not found
```powershell
pip install pymongo
```

---

## Docker MongoDB (Alternative)

If you have Docker installed:

```powershell
# Run MongoDB in Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Check if running
docker ps

# Stop MongoDB
docker stop mongodb

# Remove container
docker rm mongodb
```

---

## Environment Variables

Your `backend/.env` file should look like:

**For Local MongoDB:**
```
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=student_feedback_db
```

**For MongoDB Atlas:**
```
MONGODB_URI=mongodb+srv://username:password@cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=student_feedback_db
```

---

## Verify Everything Works

1. Start backend: `python app.py`
2. Check console for: `✅ Connected to MongoDB`
3. Open UI: `D:\projects\DevOps\student-feedback\frontend\index.html`
4. Add some feedback
5. Restart server - feedback should persist! 🎉

---

## Benefits of MongoDB

✅ **Persistent Storage** - Data survives server restarts
✅ **Scalable** - Can handle millions of records
✅ **Flexible Schema** - Easy to add new fields
✅ **Cloud-Ready** - Works with MongoDB Atlas
✅ **Professional** - Industry-standard database

---

## What Changed in Your Code

1. ✅ Added `pymongo` to requirements.txt
2. ✅ Updated `app.py` to use MongoDB
3. ✅ Added fallback to in-memory if MongoDB not available
4. ✅ Created `.env` file for configuration
5. ✅ Updated delete endpoint to handle MongoDB ObjectId

---

## Next Steps

1. Choose MongoDB option (Local or Atlas)
2. Follow setup steps above
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `.env` file
5. Run the application!

**Your data will now persist across restarts! 🎉**
