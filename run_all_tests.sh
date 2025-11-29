#!/bin/bash

echo "🚀 Starting Smoke Test Suite..."

# 1. Backend Smoke Test
echo "-----------------------------------"
echo "📡 Running Backend Smoke Check..."
python backend/check_system.py
if [ $? -ne 0 ]; then
    echo "❌ Backend Smoke Check Failed!"
    exit 1
fi

# 2. Backend Unit Tests (Pytest)
echo "-----------------------------------"
echo "🧪 Running Backend Unit Tests..."
cd backend
pytest
if [ $? -ne 0 ]; then
    echo "❌ Backend Unit Tests Failed!"
    exit 1
fi
cd ..

# 3. Frontend Tests
echo "-----------------------------------"
echo "⚛️ Running Frontend Tests..."
cd frontend
npm run test -- --watchAll=false
if [ $? -ne 0 ]; then
    echo "❌ Frontend Tests Failed!"
    exit 1
fi
cd ..

echo "-----------------------------------"
echo "✅ All Systems Go! Repo is healthy."
exit 0
