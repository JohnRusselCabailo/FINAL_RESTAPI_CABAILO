# GymDB REST API

A Flask-based CRUD REST API for managing gym members, memberships, and workouts. Supports both JSON and XML response formats with JWT authentication.

## Features

- ✅ Full CRUD operations for Members, Memberships, and Workouts
- ✅ JSON and XML response formats
- ✅ Search functionality for all tables
- ✅ JWT authentication
- ✅ Input validation and error handling
- ✅ Comprehensive test suite

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL
- **Authentication:** JWT (PyJWT)
- **Testing:** pytest

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/JohnRusselCabailo/FINAL_RESTAPI_CABAILO.git
cd FINAL_RESTAPI_CABAILO
```

### 2. Create and activate virtual environment
```bash
python -m venv RESTAPI
.\RESTAPI\Scripts\Activate.ps1  # Windows
# source RESTAPI/bin/activate   # Linux/Mac
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up MySQL database
Run the `init_db.sql` script in MySQL Workbench or command line:
```sql
source init_db.sql
```

### 5. Configure database connection
Edit `config.py` with your MySQL credentials:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'gymdb'
```

### 6. Run the application
```bash
python app.py
```
The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | Get JWT token |

**Login Example:**
```json
POST /login
{
    "username": "admin",
    "password": "admin123"
}
```

### Members
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/members` | Get all members |
| GET | `/members/<id>` | Get member by ID |
| GET | `/members/search?first_name=X` | Search by first name |
| GET | `/members/search?last_name=X` | Search by last name |
| POST | `/members` | Create new member |
| PUT | `/members/<id>` | Update member |
| DELETE | `/members/<id>` | Delete member |

### Memberships
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/memberships` | Get all memberships |
| GET | `/memberships/<id>` | Get membership by ID |
| GET | `/memberships/search?membership_type=X` | Search by type |
| POST | `/memberships` | Create new membership |
| PUT | `/memberships/<id>` | Update membership |
| DELETE | `/memberships/<id>` | Delete membership |

### Workouts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | Get all workouts |
| GET | `/workouts/<id>` | Get workout by ID |
| GET | `/workouts/search?workout_type=X` | Search by type |
| POST | `/workouts` | Create new workout |
| PUT | `/workouts/<id>` | Update workout |
| DELETE | `/workouts/<id>` | Delete workout |

## Response Formats

### JSON (Default)
```
GET http://localhost:5000/members
```

### XML
```
GET http://localhost:5000/members?format=xml
```

## Usage Examples

### Create a new member
```bash
curl -X POST http://localhost:5000/members \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Gymrat", "membership_id": 1}'
```

### Update a member
```bash
curl -X PUT http://localhost:5000/members/1 \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Garou", "last_name": "Saitama"}'
```

### Delete a member
```bash
curl -X DELETE http://localhost:5000/members/1
```

### Search for members
```
GET http://localhost:5000/members/search?first_name=John
```

## Running Tests

```bash
pytest test_app.py -v
```

## Project Structure

```
FINAL_RESTAPI_CABAILO/
├── app.py              # Main Flask application
├── config.py           # Database configuration
├── init_db.sql         # Database initialization script
├── requirements.txt    # Python dependencies
├── test_app.py         # Test suite
├── .gitignore          # Git ignore file
└── README.md           # Documentation
```

## Author

**John Russel P. Cabailo**
**BSCS3-B1**

## PROFESSOR

**PROF. VINCENT ABIAN**