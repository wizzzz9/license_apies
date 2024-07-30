# License Management API Documentation

This project provides a simple API for managing licenses using FastAPI, PostgreSQL, and Docker.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [License](#license)

## Features

- Check license validity
- Create new users with licenses
- FastAPI for rapid development and high performance
- PostgreSQL for reliable database management
- Docker for easy deployment

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/license-management-api.git
   cd license-management-api
   ```

2. **Set up Docker**

   soon...

3. **Apply database migrations**

      soon...


## Usage

   soon...


## API Endpoints

### Check License

**Endpoint**: `/api/license/check_license`  
**Method**: `GET`

**Description**: Check the validity of a license.

**Query Parameters**:
- `license_key` (str): The license key to be checked.

**Response**:
- **200 OK**: License is valid.
- **400 Bad Request**: License is invalid or expired.

### Create User

**Endpoint**: `/api/license/create_user`  
**Method**: `POST`

**Description**: Create a new user with a license.

**Request Body**:
- `admin_key` (str): The admin key for authentication.
- `payload` (CreateUserPayload): The payload containing user details.

**Response**:
- **200 OK**: User created successfully.
- **400 Bad Request**: Username already exists.

## Models

### CreateUserPayload

```python
class CreateUserPayload(BaseModel):
    username: str
    license_time: Optional[datetime] = None
    user_info: Optional[str] = None
    role_id: int
```

### CheckLicenseResponseModel

```python
class CheckLicenseResponseModel(BaseModel):
    valid: bool
    expiry_date: Optional[datetime] = None
```

### CreateUserResponseModel

```python
class CreateUserResponseModel(BaseModel):
    username: str
    license_key: str
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to contribute to this project by creating issues or submitting pull requests. Your contributions are greatly appreciated!

For further details, refer to the [FastAPI documentation](https://fastapi.tiangolo.com/) and the [Docker documentation](https://docs.docker.com/).
