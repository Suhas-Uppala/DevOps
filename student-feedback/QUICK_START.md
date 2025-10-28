# 🎓 QUICK START GUIDE - Follow These Steps!

## ✅ STEP 1: CHECK PYTHON (Already Done!)
Your Python is installed and packages are ready!

## 🚀 STEP 2: START THE SERVER

**WHERE TO RUN:** Open PowerShell in this folder:
`d:\projects\DevOps\student-feedback\backend`

**COMMAND TO RUN:**
```powershell
python app.py
```

**WHAT YOU'LL SEE:**
```
🚀 Starting Student Feedback API...
📝 API will be available at http://localhost:5000
 * Running on http://0.0.0.0:5000
```

**KEEP THIS WINDOW OPEN!** Don't close it while testing.

---

## 🧪 STEP 3: TEST THE API

**Open a NEW PowerShell window** and run these commands:

### Test 1: Check if API is running
```powershell
curl http://localhost:5000
```

### Test 2: Get all feedback (will be empty at first)
```powershell
curl http://localhost:5000/feedback
```

### Test 3: Add feedback
```powershell
$body = @{
    student_name = "John Doe"
    comment = "Great course!"
    rating = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/feedback" -Method Post -Body $body -ContentType "application/json"
```

### Test 4: Get feedback again (now you'll see the one you added!)
```powershell
curl http://localhost:5000/feedback
```

---

## 🌐 STEP 4: OPEN WEB INTERFACE

1. Go to this folder in File Explorer:
   `d:\projects\DevOps\student-feedback\frontend`

2. **Double-click** `index.html`

3. Your browser will open with a beautiful interface!

4. Try:
   - Adding feedback through the form
   - Viewing all feedback
   - Deleting feedback
   - Watching statistics update

---

## ✅ STEP 5: RUN TESTS

**Open a NEW PowerShell window:**

```powershell
cd d:\projects\DevOps\student-feedback\backend
pytest tests/ -v
```

**You'll see:**
```
test_home_endpoint PASSED ✅
test_health_endpoint PASSED ✅
test_get_feedback_empty PASSED ✅
test_add_feedback_success PASSED ✅
... and more!
```

---

## 📊 WHAT EACH FILE DOES

```
student-feedback/
│
├── backend/
│   ├── app.py              ← Main Flask API (the brain!)
│   ├── requirements.txt    ← List of packages needed
│   └── tests/
│       └── test_app.py     ← Tests to check everything works
│
├── frontend/
│   └── index.html          ← Beautiful web page
│
├── Dockerfile              ← Instructions for Docker
├── .github/workflows/
│   └── ci-cd.yml          ← Automatic testing pipeline
└── README.md               ← Full documentation
```

---

## 🎯 YOUR DEVOPS PROJECT CHECKLIST

- ✅ Python Flask REST API
- ✅ Unit Tests with pytest  
- ✅ Docker configuration
- ✅ CI/CD Pipeline (GitHub Actions)
- ✅ Frontend interface
- ✅ Complete documentation

---

## 🐛 TROUBLESHOOTING

### Server won't start?
**Error:** Port 5000 is already in use
**Fix:**
```powershell
netstat -ano | findstr :5000
taskkill /PID <number> /F
```

### Module not found?
**Fix:**
```powershell
cd d:\projects\DevOps\student-feedback\backend
pip install -r requirements.txt
```

### Tests failing?
**Make sure:** Server is NOT running when you run tests
(Stop the server with Ctrl+C first)

---

## 🎉 YOU'RE READY!

This is a complete DevOps project with:
1. ✅ REST API
2. ✅ Tests
3. ✅ Docker
4. ✅ CI/CD
5. ✅ Documentation

**Perfect for your resume and interviews!** 🚀

---

## 📚 NEXT: PUSH TO GITHUB

See the main README.md for instructions on:
- Creating a GitHub repository
- Pushing your code
- Watching the CI/CD pipeline run automatically!
