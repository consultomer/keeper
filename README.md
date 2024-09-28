# Keeper Project

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Database Initialization](#database-initialization)
- [Configuration](#configuration)
- [Installation](#installation)
  - [Local Installation](#local-installation)
  - [Docker Installation](#docker-installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

Keeper is a web application designed to manage various entities such as customers, employees, invoices, dispatches, and users. The application provides CRUD (Create, Read, Update, Delete) operations for each entity and includes authentication mechanisms.

## Features
- Add, edit, and delete products
- Manage customer information
- Create and manage invoices
- Track delivery status
- Generate sales reports
- User authentication and authorization

## Technologies Used
- **Backend:** Flask, Python
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** MySQL
- **APIs:** RESTful API
- **Deployment:** Docker or locally

## Database Initialization

The database can be initialized in two ways:

1. **Using the `/initialize_database` route:**
    - This route will initialize the database using the SQL commands provided in the `initialize_database.sql` file.
    - Navigate to `http://127.0.0.1:5000/initialize_database` to initialize the database.

2. **Running the `mysql.sql` script:**
    - You can manually run the `mysql.sql` script to set up the database.
    - Execute the following command in your MySQL environment:
      ```sql
      SOURCE path/to/mysql.sql;
      ```
    - Make sure to replace `path/to/mysql.sql` with the actual path to the `mysql.sql` file.

## Configuration

The configuration settings are located in the `.flaskenv` file. Key settings include:
- **Secret Key:** Update the `SECRET_KEY` for session management.
- **Debug Mode:** Set `DEBUG` to `True` for development.

```bash
   SECRET_KEY="SECRET_KEY_HERE"
   FLASK_DEBUG=True
   FLASK_ENV=development
   FLASK_APP=app.py
   FLASK_RUN_HOST=0.0.0.0
   FLASK_RUN_PORT=5000
   MYSQL_HOST="localhost"
   MYSQL_USER="your_username"
   MYSQL_PASSWORD="your_password"
   MYSQL_DB="your_database_name"
   MYSQL_PORT=3306
   ```
## Installation

### Local Installation
To set up the project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/consultomer/keeper.git
   cd keeper
2. **Create and activate a virtual environment::**
   ```bash
   python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. **Install the dependencies::**
   ```bash
   pip install -r requirements.txt
4. **Run the application:**
   ```bash
   flask run
### Docker Installation 
1. **Clone the repository:**
   ```bash
   git clone https://github.com/consultomer/keeper.git
   cd keeper
2. **Build Docker Image:**
   ```bash
   docker build -t keeper:0.0.1 .
   docker run -dit -p 5000:5000 --name anyname keeper:0.0.1
3. **Start the Docker container:**
   ```bash   
   docker start anyname
## Usage
After running the application, you can access it in your web browser at:

- **Access the application:** Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000).

### Credentials
- **Username:** admin
- **Password:** peWag0$efow17y6PrU

## Database Schema
The database schema includes the following tables:

- **Dispatchs:** Stores Dispatches details.
- **Customers:** Stores customer information.
- **Invoices:** Stores invoice data and links to products and customers.
- **Employees:** Stores employee data.

## API Endpoints
The project includes the following API endpoints:

### Authentication
- **Login:** `/auth/login`
- **Logout:** `/auth/logout`

### Customers
- **List Customers:** `/customer/list`
- **View Customer:** `/customer/view/<id>`
- **Add Customer:** `/customer/add`
- **Edit Customer:** `/customer/edit/<id>`
- **Delete Customer:** `/customer/delete/<id>`
- **Add Customers from CSV:** `/customer/add/csv`
- **Add Customers from XLSX:** `/customer/add/xlsx`

### Dispatch
- **List Dispatches:** `/dispatch/list`
- **View Dispatch:** `/dispatch/view/<id>`
- **Add Dispatch:** `/dispatch/add`
- **Edit Dispatch:** `/dispatch/edit/<id>`
- **Delete Dispatch:** `/dispatch/delete/<id>`

### Employees
- **List Employees:** `/employee/list`
- **View Employee:** `/employee/view/<id>`
- **Add Employee:** `/employee/add`
- **Edit Employee:** `/employee/edit/<id>`
- **Delete Employee:** `/employee/delete/<id>`

### Invoices
- **List Invoices:** `/invoice/list`
- **View Invoice:** `/invoice/view/<id>`
- **Add Invoice:** `/invoice/add`
- **Edit Invoice:** `/invoice/edit/<id>`
- **Delete Invoice:** `/invoice/delete/<id>`

### Users
- **List Users:** `/user/list`
- **View User:** `/user/view/<id>`
- **Add User:** `/user/add`
- **Edit User:** `/user/edit/<id>`
- **Delete User:** `/user/delete/<id>`

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code adheres to the project's coding standards and passes all tests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or support, please contact:

- **Omer Abdulrehman**
- **Email:** [consultomer@gmail.com](mailto:consultomer@gmail.com)
- **LinkedIn:** [Omer Abdulrehman](https://www.linkedin.com/in/omerarehman/)