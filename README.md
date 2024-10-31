# Krishi Mitra Backend

Krishi Mitra is an agricultural application designed to provide farmers with essential tools and information for managing their crops, bidding on produce, monitoring soil health, accessing weather data, and availing government schemes.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [Database Initialization](#database-initialization)
- [Inserting Dummy Data](#inserting-dummy-data)
- [API Endpoints](#api-endpoints)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [License](#license)

## Features

- User Authentication
- Soil Health Monitoring
- Bidding Platform for Crops
- Government Schemes Access
- Real-time Weather Data
- Market Prices for Crops
- CRUD operations for all entities

## Project Structure

```
./
├── .env
├── .gitignore
├── compare_schemas.py
├── create_db.py
├── directory_tree.txt
├── generate_directory_tree.py
├── insert_dummy_data.py
├── inspect_db.py
├── Makefile
├── output.txt
├── requirements.txt
├── run.py
├── setup.sh
├── alembic/
├── app/
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── __init__.py
│   ├── crud/
│   │   ├── bid.py
│   │   ├── scheme.py
│   │   ├── soil_health.py
│   │   ├── user.py
│   │   └── __init__.py
│   ├── models/
│   │   ├── bid.py
│   │   ├── scheme.py
│   │   ├── soil_health.py
│   │   ├── user.py
│   │   └── __init__.py
│   ├── routers/
│   │   ├── bidding.py
│   │   ├── scheme.py
│   │   ├── soil_health.py
│   │   ├── user.py
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── bid.py
│   │   ├── scheme.py
│   │   ├── soil_health.py
│   │   ├── user.py
│   │   └── __init__.py
│   └── utils/
│       ├── auth.py
│       ├── helpers.py
│       └── __init__.py
└── tests/
```

## Setup and Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/yourusername/krishi-mitra-backend.git
   cd krishi-mitra-backend
   ```

2. **Create a virtual environment and activate it**:

   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database Initialization

To create the database tables, run:

```sh
python create_db.py
```

## Inserting Dummy Data

To insert dummy data into the database, run:

```sh
python insert_dummy_data.py
```

## API Endpoints

The API documentation is available at: [http://localhost:8000/docs](http://localhost:8000/docs)

The following endpoints are available:

### Users

- **POST** `/users/` - Create a new user
- **GET** `/users/` - Get all users
- **GET** `/users/{user_id}` - Get a user by ID
- **PUT** `/users/{user_id}` - Update a user by ID
- **DELETE** `/users/{user_id}` - Delete a user by ID

### Soil Health

- **POST** `/soil-health/` - Create a new soil health record
- **GET** `/soil-health/` - Get all soil health records
- **GET** `/soil-health/{soil_health_id}` - Get a soil health record by ID
- **PUT** `/soil-health/{soil_health_id}` - Update a soil health record by ID
- **DELETE** `/soil-health/{soil_health_id}` - Delete a soil health record by ID

### Bids

- **POST** `/bids/` - Create a new bid
- **GET** `/bids/` - Get all bids
- **GET** `/bids/{bid_id}` - Get a bid by ID
- **PUT** `/bids/{bid_id}` - Update a bid by ID
- **DELETE** `/bids/{bid_id}` - Delete a bid by ID

### Schemes

- **POST** `/schemes/` - Create a new scheme
- **GET** `/schemes/` - Get all schemes
- **GET** `/schemes/{scheme_id}` - Get a scheme by ID
- **PUT** `/schemes/{scheme_id}` - Update a scheme by ID
- **DELETE** `/schemes/{scheme_id}` - Delete a scheme by ID

### Weather Data

- **POST** `/weather/` - Create a new weather record
- **GET** `/weather/` - Get all weather records
- **GET** `/weather/{weather_id}` - Get a weather record by ID
- **PUT** `/weather/{weather_id}` - Update a weather record by ID
- **DELETE** `/weather/{weather_id}` - Delete a weather record by ID

### Market Prices

- **POST** `/market-prices/` - Create a new market price record
- **GET** `/market-prices/` - Get all market price records
- **GET** `/market-prices/{market_price_id}` - Get a market price record by ID
- **PUT** `/market-prices/{market_price_id}` - Update a market price record by ID
- **DELETE** `/market-prices/{market_price_id}` - Delete a market price record by ID

## Running the Application

To run the application, use:

```sh
uvicorn app.main:app --reload
```

## Testing

To run tests, execute:

```sh
pytest
```

## Database Fix:

whenever database is not connecting, we need to open services.msc in Win+R and then start the postgres services

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
