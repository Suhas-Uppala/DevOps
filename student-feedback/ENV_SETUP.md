# Environment Variables Setup Guide

## 🔐 Security Best Practices

Your sensitive configuration data is stored in `.env` file which is **NOT committed to Git**.

## 📋 Setup Instructions

### Step 1: Copy the Example File
```powershell
cd backend
cp .env.example .env
```

### Step 2: Edit the .env File
Open `backend/.env` and update with your actual values:

```properties
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=student_feedback_db
FLASK_ENV=development
FLASK_DEBUG=True
```

## 🌐 Configuration Options

### Local Development (Default)
```properties
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=student_feedback_db
```

### MongoDB Atlas (Cloud - Production)
```properties
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
DATABASE_NAME=student_feedback_db
FLASK_ENV=production
FLASK_DEBUG=False
```

**Replace:**
- `username` - Your MongoDB Atlas username
- `password` - Your MongoDB Atlas password
- `cluster0.xxxxx` - Your cluster address

### Docker Compose Setup
```properties
MONGODB_URI=mongodb://mongodb:27017/
DATABASE_NAME=student_feedback_db
```

## 🚨 Important Security Notes

1. **NEVER commit `.env` to Git** - It's already in `.gitignore`
2. **Use `.env.example`** - This is safe to commit (no real credentials)
3. **Different credentials per environment** - Dev, staging, production should have separate databases
4. **Use strong passwords** - For production MongoDB instances
5. **Rotate credentials regularly** - Change passwords periodically

## ✅ Verification

Check if `.env` is properly ignored:
```powershell
git status
```

You should NOT see `.env` in the list of files to commit.

## 🔄 Team Collaboration

When a new team member joins:
1. They clone the repository (no `.env` file)
2. They copy `.env.example` to `.env`
3. They ask team lead for actual credentials
4. They update their local `.env` file

## 📁 Files Explained

- `.env` - **Your actual credentials** (Git ignored, never commit)
- `.env.example` - **Template with placeholders** (safe to commit)
- `.gitignore` - **Ensures `.env` is never committed**
- `ENV_SETUP.md` - **This guide** (safe to commit)

## 🐛 Troubleshooting

**Problem:** "Can't connect to MongoDB"
- Check if MongoDB is running: `mongosh` or MongoDB Compass
- Verify `MONGODB_URI` is correct in your `.env`
- For Atlas, check if your IP is whitelisted

**Problem:** "ModuleNotFoundError: No module named 'dotenv'"
```powershell
pip install python-dotenv
```

**Problem:** ".env file not loading"
- Ensure `.env` is in the `backend/` directory
- Check file name is exactly `.env` (not `.env.txt`)
- Restart the Flask server after changing `.env`

## 🚀 Production Deployment

For production (Heroku, AWS, Azure, etc.):
1. **DO NOT** upload `.env` file to server
2. Use platform's environment variable system:
   - Heroku: Config Vars
   - AWS: Parameter Store / Secrets Manager
   - Azure: App Settings
   - Docker: Environment variables in docker-compose.yml

Example for Heroku:
```powershell
heroku config:set MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
heroku config:set DATABASE_NAME="student_feedback_db"
```
