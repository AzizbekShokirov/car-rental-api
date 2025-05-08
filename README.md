# Car Rental API

A RESTful API service built with Django and Django REST Framework to manage cars and rentals for a car rental service.

## Features

- Car Management API (CRUD operations)
- Rental Management API (CRUD operations)
- Rent Price Management API (Read operations)
- Overdue Rentals API (Read operations)
- API Documentation with Swagger

## Tech Stack

- Python 3.10+
- Django 4.0+
- Django REST Framework 3.13+
- DRF Spectacular
- SQLite/PostgreSQL
- Docker

## Setup Instructions

### Without Docker

Clone the repository:

```bash
git clone https://github.com/yourusername/car-rental-api.git
cd car-rental-api
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Initialize rental prices:

```bash
python manage.py initialize_rentprices
```

Start the development server:

```bash
python manage.py runserver
```

### With Docker

Clone the repository:

```bash
git clone https://github.com/yourusername/car-rental-api.git
cd car-rental-api
```

Build and start the containers:

```bash
docker-compose up --build
```

## API Endpoints

### Cars

- **GET** `/api/cars/` - List all cars
- **POST** `/api/cars/` - Create a new car
- **GET** `/api/cars/{id}/` - Retrieve a specific car by ID
- **PUT/PATCH** `/api/cars/{id}/` - Update a car by ID
- **DELETE** `/api/cars/{id}/` - Delete a car by ID
- **GET** `/api/cars/vin/?vin_number={vin}` - Retrieve a car by VIN number

### Rentals

- **GET** `/api/rentals/` - List all rentals
- **POST** `/api/rentals/` - Create a new rental
- **GET** `/api/rentals/{id}/` - Retrieve a specific rental by ID
- **PUT/PATCH** `/api/rentals/{id}/` - Update a rental by ID
- **DELETE** `/api/rentals/{id}/` - Delete a rental by ID
- **GET** `/api/rentals/overdue/` - List all overdue rentals

### Rent Prices

- **GET** `/api/rentprices/` - List all rental prices by car type

## API Documentation

API documentation is available at:

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI Schema: `/api/schema/`

## Example Requests

### Create a Car

```bash
curl -X POST http://localhost:8000/api/cars/ \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "Toyota",
    "model": "Corolla",
    "car_type": "SEDAN",
    "color": "Blue",
    "engine_size": 1.8,
    "fuel_type": "PETROL",
    "odometer": 0,
    "year_of_production": 2023,
    "vin_number": "1HGBH41JXMN109186",
    "registration_number": "AB123CD"
  }'
```

### Create a Rental

```bash
curl -X POST http://localhost:8000/api/rentals/ \
  -H "Content-Type: application/json" \
  -d '{
    "registration_number": "AB123CD",
    "rent_duration": 7,
    "rent_start_date": "2023-09-01"
  }'
```

### Mark a Rental as Complete

```bash
curl -X PATCH http://localhost:8000/api/rentals/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "rent_complete": true
  }'
```

### Get Overdue Rentals

```bash
curl -X GET http://localhost:8000/api/rentals/overdue/
```

## Database Schema

### Car Model

- brand: CharField
- model: CharField
- car_type: CharField (choices)
- color: CharField
- engine_size: DecimalField
- fuel_type: CharField (choices)
- odometer: IntegerField
- year_of_production: IntegerField
- vin_number: CharField (unique)
- registration_number: CharField (unique)

### RentPrice Model

- car_type: CharField (choices)
- daily_rate: DecimalField

### Rental Model

- car: ForeignKey (Car)
- rent_start_date: DateField
- rent_duration: IntegerField
- rent_complete: BooleanField
- rent_end_date: property (calculated)
- price: property (calculated)
- fine: property (calculated)

## License

This project is licensed under the MIT License.
