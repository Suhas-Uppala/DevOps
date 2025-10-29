#!/bin/bash

# Railway Start Script for Student Feedback API

echo "🚀 Starting Student Feedback API on Railway..."

# Navigate to backend directory
cd backend

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run database migrations or setup if needed
echo "🗄️  Checking database connection..."

# Start the Flask application
echo "✅ Starting Flask server..."
python app.py
