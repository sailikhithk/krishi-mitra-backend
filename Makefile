.PHONY: setup activate install create_db run

# Step 1: Create a virtual environment
setup:
	python -m venv venv

# Step 2: Activate the virtual environment
activate:
	source venv/Scripts/activate

# Step 3: Install the required packages
install:
	pip install -r requirements.txt

# Step 4: Create the database tables
create_db:
	python create_db.py

# Step 5: Run the FastAPI application
run:
	python run.py

# Combine all steps
all: setup activate install create_db run
