# Boomerang API

A server side web API that uses CRUD operations to create events, send bulk SMS invites and view invitee responses, 
built using the Flask microframework, SQLite database and Twilio Programmable SMS API (https://www.twilio.com/docs/sms). 

## Requirements

On a Linux environment, run the following commands:
```bash
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6 python3.6-dev
sudo apt-get update
sudo apt-get install curl
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install virtualenv
```

## Getting Started

```bash
# Clone this repository and cd into it:
git clone https://github.com/thesillypeanut/boomerang-api.git
cd boomerang-api/

# Create and activate your virtual environment:
virtualenv venv
source venv/bin/activate

# Install your project dependencies:
pip install -r requirements.txt

# Start the server:
python3 run.py
```

## Try Out the API

This is a sample testing flow of creating an event, inviting guests and viewing invitee responses.

Create a user:
```bash
curl -H "Content-Type: application/json" -X POST -d '{"username":"USERNAME", "password":"PASSWORD"}' http://localhost:5000/api/v1/users/
```

Login the user:
```bash
curl --user <USERNAME>:<PASSWORD> http://localhost:5000/api/v1/users/login
```
You will receive an authentication token. Please note that you need to use the token you received in the previous step 
to perform most requests from here on. For your convenience, you can save the token in an environment variable:
```bash
export TOKEN="YOUR-TOKEN-HERE"
echo "$TOKEN"
```
Your token will expire in 1 hour. Login again to get a new token and update your environment variable as necessary.

Create an event:



## Database Models and API Usage

<img src="/database_design.png">

### Database
```bash
# Initialize db:
curl -X GET http://localhost:5000/api/v1/db/init
```

### Product
```bash
# Fetch all products:
curl -X GET http://localhost:5000/api/v1/products/

# Fetch all available (inventory count > 0) products:
curl -X GET http://localhost:5000/api/v1/products/available

# Filter products using queries in the route (only "equal to" queries are supported):
curl -X GET http://localhost:5000/api/v1/products/?price=10.4\&inventory_count=300

# Fetch a single product by id:
curl -X GET http://localhost:5000/api/v1/products/<product_id>

# Create a product with title, price (float) and inventory_count (int):
curl -H "Content-Type: application/json" -X POST -d '{"title":"TITLE", "price":<float_price>, "inventory_count":<inven_int>}' http://localhost:5000/api/v1/products/

# Edit a product's title, price (float) and/or inventory_count (int):
curl -H "Content-Type: application/json" -X PUT -d '{"title":"NEWTITLE", "price":<new_float_price>, "inventory_count":<new_inven_int>}' http://localhost:5000/api/v1/products/<product_id>

# Delete a product:
curl -X DELETE http://localhost:5000/api/v1/products/<product_id>
```

### User (and Token Authentication)
```bash
# Create a user with a username and password:
curl -H "Content-Type: application/json" -X POST -d '{"username":"USERNAME", "password":"PASSWORD"}' http://localhost:5000/api/v1/users/

# Login with the username and password you selected using Basic Authentication:
curl --user <USERNAME>:<PASSWORD> http://localhost:5000/api/v1/users/login
```

Please note that you need to use the token you received in the previous step to perform most requests from here on.
For your convenience, you can save the token in an environment variable:
```bash
export TOKEN="YOUR-TOKEN-HERE"
echo "$TOKEN"
```
Your token will expire in 1 hour. Login again to get a new token and update your environment variable as necessary.

```bash
# Fetch all users:
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/users/

# Fetch a single user with id:
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/users/<user_id>

# Edit your username and/or password:
curl -H "x-access-token: $TOKEN" -H "Content-Type: application/json" -X PUT -d '{"username":"NEWUSERNAME", "password":"NEWPASSWORD"}' http://localhost:5000/api/v1/users/<user_id>

# Delete your user record:
curl -H "x-access-token: $TOKEN" -X DELETE http://localhost:5000/api/v1/users/<user_id>
```

### Cart-Item
```bash
# Create a cart-item with a product id and quantity (int):
curl -H "x-access-token: $TOKEN" -H "Content-Type: application/json" -X POST -d '{"product_id":"PRODUCTID", "quantity":<quantity_int>}' http://localhost:5000/api/v1/cart-items/

# Fetch all cart-items associated with a cart_id (note that a user can have multiple "ordered" 
# carts and only one "unordered" cart):
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/cart-items/?cart_id=<cart_id>

# Fetch a single cart-item with id:
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/cart-items/<cart-item-id>

# Edit a cart item quantity:
curl -H "x-access-token: $TOKEN" -H "Content-Type: application/json" -X PUT -d '{"quantity":<new_quantity_int>}' http://localhost:5000/api/v1/cart-items/<cart-item-id>

# Delete a cart item:
curl -H "x-access-token: $TOKEN" -X DELETE http://localhost:5000/api/v1/cart-items/<cart_item_id>
```

### Cart
```bash
# Fetch all carts (note that a user can have multiple "ordered" carts and only one "unordered" cart):
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/carts/

# Fetch a single cart with id:
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/carts/<cart_id>

# Delete a cart:
curl -H "x-access-token: $TOKEN" -X DELETE http://localhost:5000/api/v1/carts/<cart_id>
```

### Order
```bash
# Create an order on a cart with cart_id:
curl -H "x-access-token: $TOKEN" -H "Content-Type: application/json" -X POST -d '{"cart_id":"CARTID"}' http://localhost:5000/api/v1/orders/

# Fetch all orders:
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/orders/

# Fetch a single order with id:
curl -H "x-access-token: $TOKEN" -X GET http://localhost:5000/api/v1/orders/<order_id>
```

## Migrations
Migrations need to be run to propagate changes we make to our models (eg. adding a field, deleting a model).
Flask-Migrate uses Alembic to autogenerate migrations for us.

```bash
# Initialize migrations:
python3 manage.py db init

# Run migrations:
python3 manage.py db migrate

# Apply migrations to the database:
python3 manage.py db upgrade
```

## Testing
Unit tests are written to automate testing for the various services.

```bash
# Run all tests:
pytest

# Run all tests with debugging (no capture):
pytest -s

# Run a single test (file-path::class-name::test-name):
pytest tests/unit/test_user_service.py::UserTestCase::test_list_all_users_is_successful
```