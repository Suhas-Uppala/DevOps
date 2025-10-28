"""
Test MongoDB Connection
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'student_feedback_db')

print("🔍 Testing MongoDB Connection...")
print(f"URI: {MONGODB_URI}")
print(f"Database: {DATABASE_NAME}")
print("-" * 50)

try:
    # Connect to MongoDB
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    
    # Test connection
    client.server_info()
    print("✅ Successfully connected to MongoDB!")
    
    # Get database
    db = client[DATABASE_NAME]
    print(f"✅ Database '{DATABASE_NAME}' is accessible")
    
    # Get collection
    collection = db['feedbacks']
    
    # Count documents
    count = collection.count_documents({})
    print(f"📊 Current feedback count: {count}")
    
    # Test insert
    test_doc = {
        "student_name": "Test Student",
        "comment": "Testing MongoDB connection",
        "rating": 5,
        "test": True
    }
    
    result = collection.insert_one(test_doc)
    print(f"✅ Test document inserted with ID: {result.inserted_id}")
    
    # Verify insert
    found = collection.find_one({"_id": result.inserted_id})
    if found:
        print(f"✅ Document retrieved successfully: {found['student_name']}")
    
    # Clean up test document
    collection.delete_one({"_id": result.inserted_id})
    print("✅ Test document cleaned up")
    
    # List all databases
    print("\n📚 Available databases:")
    for db_name in client.list_database_names():
        print(f"  - {db_name}")
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! MongoDB is working correctly!")
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Troubleshooting:")
    print("1. Make sure MongoDB is installed and running")
    print("2. Check if MongoDB service is started: net start MongoDB")
    print("3. Verify connection string in .env file")
    print("4. For Atlas, check IP whitelist and credentials")
