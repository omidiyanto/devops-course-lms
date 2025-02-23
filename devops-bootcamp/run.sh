#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting DevOps Bootcamp Application...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python 3.10 or later."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing backend dependencies...${NC}"
pip install -r backend/requirements.txt

# Check if .env file exists, if not create it from example
if [ ! -f "backend/.env" ]; then
    echo -e "${BLUE}Creating .env file from .env.example...${NC}"
    cp backend/.env.example backend/.env
    echo "Please update the backend/.env file with your configuration values."
fi

# Start backend server in background
echo -e "${BLUE}Starting Flask backend server...${NC}"
cd backend && python3 app.py &
FLASK_PID=$!

# Start frontend server in background
echo -e "${BLUE}Starting frontend server...${NC}"
cd ../frontend && python3 -m http.server 8000 &
FRONTEND_PID=$!

echo -e "${GREEN}Application is running!${NC}"
echo -e "${GREEN}Frontend: http://localhost:8000${NC}"
echo -e "${GREEN}Backend: http://localhost:5000${NC}"
echo "Press Ctrl+C to stop the servers"

# Handle script termination
trap "echo -e '\n${BLUE}Stopping servers...${NC}' && kill $FLASK_PID $FRONTEND_PID" INT TERM

# Wait for both processes
wait
