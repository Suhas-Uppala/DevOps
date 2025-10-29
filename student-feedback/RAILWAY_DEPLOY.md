# 🚂 Railway Deployment Guide

## 📋 Quick Deployment Steps

### 1️⃣ Push Your Code to GitHub

```powershell
# Initialize git (if not already done)
cd D:\projects\DevOps\student-feedback
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Student Feedback API"

# Create GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/student-feedback.git
git branch -M main
git push -u origin main
```

### 2️⃣ Deploy on Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `student-feedback` repository
5. Railway will automatically detect and deploy

### 3️⃣ Add MongoDB Database

**Option A: Railway MongoDB Plugin**
1. In your Railway project dashboard
2. Click **"+ New"** → **"Database"** → **"Add MongoDB"**
3. Railway will automatically add `MONGODB_URI` environment variable

**Option B: MongoDB Atlas (Free Cloud)**
1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster
3. Get connection string
4. Add to Railway environment variables

### 4️⃣ Configure Environment Variables

In Railway dashboard, go to **Variables** tab and add:

```bash
# Required
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=student_feedback_db

# Optional
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
```

**Note:** Railway automatically provides `PORT` variable, so you don't need to set it manually.

### 5️⃣ Deploy!

Railway will automatically deploy when you push to GitHub. You can also manually redeploy from the dashboard.

## 📁 Files Created for Railway

✅ **start.sh** - Shell script to start the application
✅ **railway.json** - Railway configuration
✅ **backend/Procfile** - Process file for Railway
✅ **app.py** - Updated to use `PORT` environment variable

## 🔗 Get Your Deployment URL

After deployment, Railway provides a public URL like:
```
https://your-app-name.up.railway.app
```

## 🧪 Test Your Deployment

```powershell
# Replace with your Railway URL
$BASE_URL = "https://your-app-name.up.railway.app"

# Test home endpoint
Invoke-RestMethod -Uri "$BASE_URL/" -Method Get

# Test health endpoint
Invoke-RestMethod -Uri "$BASE_URL/health" -Method Get

# Get all feedback
Invoke-RestMethod -Uri "$BASE_URL/feedback" -Method Get

# Add new feedback
$body = @{
    student_name = "Test Student"
    comment = "Great deployment!"
    rating = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "$BASE_URL/feedback" -Method Post -Body $body -ContentType "application/json"
```

## 🌐 Update Frontend

Update your `frontend/index.html` to use Railway URL:

```javascript
// Replace this line:
const API_URL = 'http://localhost:5000';

// With your Railway URL:
const API_URL = 'https://your-app-name.up.railway.app';
```

## 📊 Railway Dashboard Features

- **Logs**: View real-time application logs
- **Metrics**: Monitor CPU, memory, network usage
- **Deployments**: Track deployment history
- **Variables**: Manage environment variables
- **Settings**: Configure custom domains

## 🔐 Security Checklist

Before deploying to production:

- [ ] `.env` file is in `.gitignore` (already done ✅)
- [ ] Use strong MongoDB password
- [ ] Set `FLASK_DEBUG=False` in production
- [ ] Add MongoDB Atlas IP whitelist (0.0.0.0/0 for Railway)
- [ ] Use environment variables for all secrets
- [ ] Enable CORS only for your frontend domain (optional)

## 🐛 Troubleshooting

### Deployment Failed
- Check Railway logs in dashboard
- Verify `requirements.txt` is correct
- Ensure MongoDB connection string is valid

### Can't Connect to MongoDB
- Check `MONGODB_URI` format
- For Atlas: Whitelist all IPs (0.0.0.0/0) in Network Access
- Verify database user has read/write permissions

### App Crashes on Start
- Check Railway logs for error messages
- Verify all dependencies in `requirements.txt`
- Test MongoDB connection with health endpoint

### Wrong Port Error
- Railway automatically sets `PORT` environment variable
- `app.py` now reads from `PORT` env variable
- Don't hardcode port 5000

## 🚀 Continuous Deployment

Railway automatically redeploys when you push to GitHub:

```powershell
# Make changes to your code
git add .
git commit -m "Update feature"
git push origin main

# Railway automatically deploys! 🎉
```

## 💰 Railway Pricing

- **Free Tier**: $5 credit per month (enough for small apps)
- **Hobby Plan**: $5/month for more resources
- **Pro Plan**: Pay as you grow

## 🔄 Alternative Platforms

If you want to try other platforms:

- **Render.com** - Similar to Railway, also uses `start.sh`
- **Heroku** - Uses `Procfile` (already created)
- **Vercel** - For serverless deployment
- **Google Cloud Run** - Uses `Dockerfile` (already created)

## 📚 Additional Resources

- [Railway Docs](https://docs.railway.app)
- [MongoDB Atlas Guide](https://www.mongodb.com/docs/atlas/getting-started/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)

## ✅ Success Indicators

After deployment, you should see:

1. ✅ Green checkmark in Railway dashboard
2. ✅ Public URL accessible
3. ✅ MongoDB connected (check logs)
4. ✅ Health endpoint returns "healthy"
5. ✅ Can add/retrieve feedback via API

---

**Need Help?** Check Railway logs first, they show detailed error messages!
