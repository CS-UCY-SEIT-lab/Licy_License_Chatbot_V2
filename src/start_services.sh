#!/bin/bash

# Command 1: Run a Python script in the background
rasa run actions &

# Command 2: Run a Node.js server in the background
rasa run --enable-api &

# Command 3: Run a long-running process (e.g., sleep for 60 seconds) in the background
cd backend && python chatbot.py &
