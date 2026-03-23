#!/bin/bash
# Starts the backend and frontend with one command.
# Run with: ./start.sh

echo "Starting Internship Tracker..."

# Start the FastAPI backend in the background
uvicorn api:app --reload &
BACKEND_PID=$!

# Start the React frontend in the background
cd frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "Backend running at http://localhost:8000"
echo "Frontend running at http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers."

# Wait and kill both on Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
