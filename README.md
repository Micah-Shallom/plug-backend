# advert-backend
This repository contains the backend code for the advertising application in my software engineering project this semester.

# JWT Authentication Endpoints

This group of endpoints contains the authentication and authorization logic of our app.

### `POST /auth/register`

Register a new user.

- URL: `localhost:5000/auth/register`
- Body (raw JSON):
    ```json
    {
        "username": "micahshallom",
        "password": "testPassword",
        "role": "buyer",
        "email": "micashallom@gmail.com"
    }
    ```

### `POST /auth/login`

Log in a user.

- URL: `localhost:5000/auth/login`
- Body (raw JSON):
    ```json
    {
        "username": "micahshallom",
        "password": "testPassword"
    }
    ```

### `GET /users/all`

Retrieve all users.

- URL: `localhost:5000/users/all`
- Authorization: Bearer Token
    - Token: `<token>`

### `GET /auth/whoami`

Get information about the currently authenticated user.

- URL: `localhost:5000/auth/whoami`
- Authorization: Bearer Token
    - Token: `<token>`
