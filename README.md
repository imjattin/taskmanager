# Task Manager API

This is a simple Task Manager build in Django with Django Rest Framework. It has basic CRUD features for task management and user authentication.

# Tech Stack

- Django
- Django Rest Framework
- Sqlite DB
- Swagger documentation for API

# Steps to run the application

1. **Clone the repository**

   ```
   git clone <repository-url>
   cd taskmanager
   ```

2. **Create and activate a virtual environment**

   ```
   # For Windows
   python -m venv venv
   venv\Scripts\activate

   # For macOS/Linux
   python -m venv venv
   source ./venv/bin/activate
   ```

3. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```
   python manage.py migrate
   ```

5. **Load initial data (optional)**

   ```
   python manage.py loaddata db.json
   ```

6. **Create a superuser (optional)**
   If you have already run the above command then a user admin is already loaded in the DB.

   ```
   username: admin
   password: admin
   ```

   Otherwise create another super user -

   ```
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```
   python manage.py runserver
   ```

8. **Access the application**

   - API Root: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/docs/

   Other Endpoints in the application -

   - Auth Endpoints

     - `http://localhost:8000/accounts/register`
     - `http://localhost:8000/accounts/login`
     - `http://localhost:8000/accounts/refresh`
     - `http://localhost:8000/accounts/verify`

   - Task CRUD endpoints
     - GET - `http://localhost:8000/tasks/`
     - POST - `http://localhost:8000/tasks/`
     - PUT - `http://localhost:8000/tasks/{id}`
     - DELETE - `http://localhost:8000/tasks/{id}`
     - PATCH - `http://localhost:8000/tasks/{id}`

# Authentication in Swagger UI

To use the authenticated endpoints in Swagger UI:

1. Go to http://localhost:8000/docs/
2. Click on the "Authorize" button
3. If you've run the loaddata command:
   - Use the pre-created account:
     - Username: user
     - Password: pa$$word4u
   - Or use any other user created during data loading
4. If you haven't loaded data, register a new user first at `/accounts/register` endpoint, then use those credentials
5. This will give you the access and refresh token for the user.
6. Copy the access token value without the quotes("")
7. Click on the "Authorize" button
8. Enter the access token to authenticate:
   - Enter `Bearer <copied-access-token>` in the value field
9. Click "Authorize" and close the popup
10. Now you can use all authenticated endpoints

# Features

- **User Authentication**

  - Registration, login and logout
  - JSON Web Token-based authentication

- **Task Management**

  - Create, read, update and delete tasks
  - Mark tasks as completed

- **Task Organization**

  - Filter tasks by completed by adding `completed=true/false` in query params
  - Pagination for task lists - use `page` query param to switch to next page or use the link in the first result.

- **API Documentation**
  - Interactive Swagger UI documentation
  - Endpoint details with request/response examples

# API Endpoints

## Authentication APIs

### Register - POST /auth/register/

**Request:**

```json
{
	"username": "newuser",
	"password": "securepassword123",
	"email": "newuser@gmail.com"
}
```

**Response:**

```json
{
	"access": "94659dbd28d61a11b5c0c7093f85e371fe2e5c9d",
	"refresh": "93f85e371fe2e5c9d94659dbd28d61a11b5c0c70"
}
```

### Login - POST /auth/login/

**Request:**

```json
{
	"username": "newuser",
	"password": "securepassword123"
}
```

**Response:**

```json
{
	"access": "94659dbd28d61a11b5c0c7093f85e371fe2e5c9d",
	"refresh": "93f85e371fe2e5c9d94659dbd28d61a11b5c0c70"
}
```

## Task APIs

### List Tasks - GET /tasks/

**Response:**

```json
{
	"count": 10,
	"next": "http://localhost:8000/tasks/?page=1",
	"previous": null,
	"results": [
		{
			"id": 1,
			"title": "Complete project documentation",
			"description": "Finish the API documentation for the Task Manager",
			"completed": true,
			"created_at": "2023-10-15T14:30:00Z",
			"updated_at": "2023-10-15T14:30:00Z"
		}
		// More tasks...
	]
}
```

### Create Task - POST /tasks/

**Request:**

```json
{
	"title": "New Task",
	"description": "Task description",
	"completed": false
}
```

**Response:**

```json
{
	"id": 11,
	"title": "New Task",
	"description": "Task description",
	"completed": false,
	"created_at": "2023-10-20T09:15:23Z",
	"updated_at": "2023-10-20T09:15:23Z"
}
```

# Other

## Tests

The application has 98% test coverage. The tests are written in tests.py file in tasks and accounts application.
Run the following commands to run test and get the coverage

```
# Running tests
python manage.py test

# Run coverage
coverage run manage.py test

# Build the html report for coverage
coverage html -d cov_report_html
```

## User Roles

The db.json file has three users, one(user) has admin access and can login to admin page. The other(user2) can not login to admin page.
When you load db.json(steps mentioned above) 3 users will be loaded -

1. admin - has admin access
2. user - has admin access and perissions to edit Task
3. user2 - no admin access and no permissions to edit Task in admin panel

## User Credentials

| Username | Password   |
| -------- | ---------- |
| admin    | admin      |
| user     | pa$$word4u |
| user2    | pa$$word4u |

# Other Details

- Tests are implemented using django's unittest.
- The project also has Environment based loading for env vars.
- The main app that handles all the other apps is settings. It has the main url and settings file.
- Utilizing the inmemory sqlite database.
- The db.json has around 20 sample tasks.
