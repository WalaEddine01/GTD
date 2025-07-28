# GTD API Documentation

## 📚 Interactive Documentation

Your GTD API now includes comprehensive Swagger/OpenAPI documentation! Access it through these URLs:

### 🔗 Documentation URLs

- **Swagger UI (Interactive)**: `http://127.0.0.1:8000/api/docs/`
- **ReDoc (Alternative)**: `http://127.0.0.1:8000/api/redoc/`
- **OpenAPI Schema (JSON)**: `http://127.0.0.1:8000/api/schema/`

## 🚀 Features

### Interactive API Testing
- **Try it out**: Test API endpoints directly from the browser
- **Authentication**: Built-in authentication support
- **Request/Response examples**: See real examples for each endpoint
- **Schema validation**: Automatic validation of request/response data

### Comprehensive Documentation
- **Endpoint descriptions**: Detailed explanations for each API endpoint
- **Parameter documentation**: Complete parameter descriptions and types
- **Response schemas**: Detailed response structure documentation
- **Authentication requirements**: Clear indication of auth requirements

## 🔧 Quick Start

1. **Start the development server**:
   ```bash
   python3 manage.py runserver
   ```

2. **Open Swagger UI**:
   Navigate to `http://127.0.0.1:8000/api/docs/`

3. **Authenticate** (if needed):
   - Click "Authorize" button in Swagger UI
   - Use basic authentication with your username/password
   - Or use session authentication by logging in via Django admin first

4. **Test endpoints**:
   - Click on any endpoint to expand it
   - Click "Try it out"
   - Fill in parameters
   - Click "Execute"

## 📖 API Overview

### Authentication Endpoints
- `POST /api/users/` - Register new user (no auth required)
- `GET /api/users/profile/` - Get current user profile

### User Management
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get specific user
- `PUT/PATCH /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Group Management
- `GET /api/groups/` - List all groups
- `POST /api/groups/` - Create new group
- `GET /api/groups/{id}/` - Get specific group
- `PUT/PATCH /api/groups/{id}/` - Update group
- `DELETE /api/groups/{id}/` - Delete group
- `GET /api/groups/{id}/tasks/` - Get tasks in group

### Task Management
- `GET /api/tasks/` - List user's tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get specific task
- `PUT/PATCH /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `POST /api/tasks/{id}/toggle_completed/` - Toggle completion
- `GET /api/tasks/completed/` - List completed tasks
- `GET /api/tasks/pending/` - List pending tasks

## 🔐 Authentication Examples

### Using curl with Basic Auth
```bash
# Register a new user
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123", "email": "test@example.com"}'

# Create a task (requires auth)
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -u "testuser:testpass123" \
  -d '{"title": "My Task", "description": "Task description"}'
```

### Using Swagger UI
1. Click the "Authorize" button
2. Enter your username and password
3. Click "Authorize"
4. Now you can test authenticated endpoints

## 📊 Schema Information

The API uses OpenAPI 3.0 specification with the following main data schemas:

### 🧑‍💼 User Schema
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_joined": "2025-07-28T10:30:00Z"
}
```

**Fields:**
- `id` (integer, read-only): Unique identifier
- `username` (string, required): Unique username (max 150 chars)
- `email` (string, optional): Email address
- `first_name` (string, optional): User's first name
- `last_name` (string, optional): User's last name
- `password` (string, write-only): Password for registration/updates
- `date_joined` (datetime, read-only): Registration timestamp

### 📁 Group Schema
```json
{
  "id": 1,
  "name": "Work Projects",
  "description": "Tasks related to work projects",
  "created_at": "2025-07-28T10:30:00Z",
  "owner": 1,
  "owner_username": "john_doe",
  "task_count": 5
}
```

**Fields:**
- `id` (integer, read-only): Unique identifier
- `name` (string, required): Group name (max 200 chars)
- `description` (string, optional): Group description
- `created_at` (datetime, read-only): Creation timestamp
- `owner` (integer, read-only): Owner's user ID
- `owner_username` (string, read-only): Owner's username
- `task_count` (integer, read-only): Number of tasks in group

### ✅ Task Schema
```json
{
  "id": 1,
  "title": "Complete API documentation",
  "description": "Write comprehensive API docs with examples",
  "due_date": "2025-08-01T12:00:00Z",
  "completed": false,
  "created_at": "2025-07-28T10:30:00Z",
  "updated_at": "2025-07-28T11:45:00Z",
  "group": 1,
  "group_name": "Work Projects",
  "owner": 1,
  "owner_username": "john_doe"
}
```

**Fields:**
- `id` (integer, read-only): Unique identifier
- `title` (string, required): Task title (max 200 chars)
- `description` (string, required): Task description
- `due_date` (datetime, optional): Due date and time
- `completed` (boolean): Completion status (default: false)
- `created_at` (datetime, read-only): Creation timestamp
- `updated_at` (datetime, read-only): Last update timestamp
- `group` (integer, optional): Group ID this task belongs to
- `group_name` (string, read-only): Group name
- `owner` (integer, read-only): Owner's user ID
- `owner_username` (string, read-only): Owner's username

## 🔄 API Response Formats

### Standard List Response (Paginated)
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/tasks/?page=2",
  "previous": null,
  "results": [
    {
      // ... task objects
    }
  ]
}
```

### Error Response Format
```json
{
  "detail": "Authentication credentials were not provided.",
  "error_code": "authentication_failed"
}
```

### Validation Error Response
```json
{
  "field_name": [
    "This field is required."
  ],
  "another_field": [
    "Ensure this value has at most 200 characters."
  ]
}
```

## 🎯 Permission Matrix

| User Type | Users | Groups | Tasks |
|-----------|-------|--------|-------|
| **Unauthenticated** | Register only | ❌ No access | ❌ No access |
| **Regular User** | 👀 View all<br/>✏️ Edit own profile | 👀 View all<br/>✏️ Edit own groups | 👀 View own only<br/>✏️ Edit own tasks |
| **Superuser** | 👀 View all<br/>✏️ Edit all | 👀 View all<br/>✏️ Edit all | 👀 View all<br/>✏️ Edit all |

**Legend:**
- 👀 View permissions
- ✏️ Create/Update/Delete permissions
- ❌ No access

## 🛠️ Advanced Usage

### Filtering and Searching
Currently supported filters:
- **Tasks by completion status**: `/api/tasks/completed/`, `/api/tasks/pending/`
- **Tasks by group**: `/api/groups/{id}/tasks/`

### Bulk Operations
For bulk operations, make multiple API calls or consider implementing custom endpoints.

### Rate Limiting
Currently no rate limiting is implemented. Consider adding it for production use.

## 📈 Status Codes

The API uses standard HTTP status codes:

| Code | Meaning | Usage |
|------|---------|-------|
| `200` | OK | Successful GET, PUT, PATCH requests |
| `201` | Created | Successful POST requests |
| `204` | No Content | Successful DELETE requests |
| `400` | Bad Request | Invalid request data/validation errors |
| `401` | Unauthorized | Authentication required |
| `403` | Forbidden | Permission denied |
| `404` | Not Found | Resource doesn't exist |
| `405` | Method Not Allowed | HTTP method not supported |
| `500` | Internal Server Error | Server error |

## 🔧 Development Tools

### Generate OpenAPI Schema File
```bash
python3 manage.py spectacular --color --file schema.yml
```

### Validate API Schema
```bash
python3 manage.py spectacular --validate
```

### Export Schema as JSON
```bash
curl http://127.0.0.1:8000/api/schema/ > api_schema.json
```

## 🚀 Production Considerations

### Security
- Enable HTTPS in production
- Use environment variables for sensitive settings
- Implement rate limiting
- Add CORS headers if needed for frontend integration

### Performance
- Add database indexing for frequently queried fields
- Implement caching for read-heavy operations
- Consider pagination limits for large datasets

### Monitoring
- Add logging for API requests
- Monitor response times
- Track error rates

## 📚 Additional Resources

- **Django REST Framework**: https://www.django-rest-framework.org/
- **drf-spectacular**: https://drf-spectacular.readthedocs.io/
- **OpenAPI Specification**: https://swagger.io/specification/
- **Postman Collection**: Import the schema URL into Postman for testing


---

**Happy coding! 🎉**

For support or questions, visit the documentation URLs above or check the interactive Swagger UI at `http://127.0.0.1:8000/api/docs/`