# GTD API Documentation

## Base URL
```
http://127.0.0.1:8000/api/
```

## Endpoints

### Groups

#### List all groups
- **GET** `/api/groups/`
- Returns an array of all groups

#### Create a new group
- **POST** `/api/groups/`
- Body: `{"name": "string", "description": "string (optional)"}`

#### Get a specific group
- **GET** `/api/groups/{id}/`

#### Update a group
- **PUT** `/api/groups/{id}/`
- **PATCH** `/api/groups/{id}/`

#### Delete a group
- **DELETE** `/api/groups/{id}/`

#### Get all tasks for a group
- **GET** `/api/groups/{id}/tasks/`

### Tasks

#### List all tasks
- **GET** `/api/tasks/`
- Returns an array of all tasks

#### Create a new task
- **POST** `/api/tasks/`
- Body: `{"title": "string", "description": "string", "due_date": "datetime (optional)", "group": "id (optional)"}`

#### Get a specific task
- **GET** `/api/tasks/{id}/`

#### Update a task
- **PUT** `/api/tasks/{id}/`
- **PATCH** `/api/tasks/{id}/`

#### Delete a task
- **DELETE** `/api/tasks/{id}/`

#### Toggle task completion status
- **POST** `/api/tasks/{id}/toggle_completed/`

#### Get all completed tasks
- **GET** `/api/tasks/completed/`

#### Get all pending tasks
- **GET** `/api/tasks/pending/`

## Example Usage

### Create a group:
```bash
curl -X POST http://127.0.0.1:8000/api/groups/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Work Tasks", "description": "Tasks related to work"}'
```

### Create a task:
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete project", "description": "Finish the GTD app", "group": 1}'
```

### Toggle task completion:
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/1/toggle_completed/
```

### Get completed tasks:
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/completed/
```

## Model Structure

### Task
- `id`: Auto-generated primary key
- `title`: CharField (max 200 chars)
- `description`: TextField
- `due_date`: DateTimeField (optional)
- `completed`: BooleanField (default: False)
- `created_at`: DateTimeField (auto-generated)
- `updated_at`: DateTimeField (auto-updated)
- `group`: ForeignKey to Group (optional)
- `group_name`: Read-only field showing group name

### Group
- `id`: Auto-generated primary key
- `name`: CharField (max 200 chars)
- `description`: TextField (optional)
- `created_at`: DateTimeField (auto-generated)
