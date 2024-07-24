#!/bin/bash

# Step 1: Create a virtual environment
python -m venv venv

# Step 2: Activate the virtual environment
source venv/Scripts/activate

# Step 3: Install the required packages
pip install -r requirements.txt

# Step 4: Create the database tables
python create_db.py

# Step 5: Run the FastAPI application
python run.py
