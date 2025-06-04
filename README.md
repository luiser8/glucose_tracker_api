# API de Glucosa
## up / down app docker
### docker compose down glucose_tracker_db
### docker compose up -d glucose_tracker_db
## Endpoints

### HBA1C
### GET `/hba1c/get/start_date/<fecha>/end_date/<fecha>`
Calcula el HbA1c basado en mediciones de glucosa.

**Parámetros:**
- `start_date`: Fecha de inicio (formato YYYY-MM-DD).
- `end_date`: Fecha de fin (formato YYYY-MM-DD).

**Respuesta exitosa (200):**
```json
{
    "data": {
        "hba1c": 5.82
    },
    "message": "HBA1c calculated successfully",
    "status": 200
}
```

### GET `/api/users/get`
Obtiene la lista de todos los usuarios.
**Requiere autenticación.**

**Respuesta exitosa (200):**
```json
{
    "message": "Users successfully",
    "status": 200,
    "data": [
        {
            "email": "user1@gmail.com",
            "firstname": "First Name",
            "id": 1,
            "lastname": "Last Name",
            "password": "gghththt",
            "status": true
        },
        {
            "email": "user2@gmail.com",
            "firstname": "First Name",
            "id": 2,
            "lastname": "Last Name",
            "password": "thhthththth",
            "status": true
        }
    ],
}
```

#### GET `/api/users/get/<id>`
Obtiene la información de un usuario por su ID.
**Requiere autenticación.**

#### POST `/api/users/post`
Crea un nuevo usuario.
**Body:**
```json
{
    "firstname": "Nombre",
    "lastname": "Apellido",
    "email": "correo@ejemplo.com",
    "password": "contraseña"
}
```

#### PUT `/api/users/put/<id>`
Actualiza los datos de un usuario por su ID.
**Requiere autenticación.**

#### DELETE `/api/users/delete/<id>`
Elimina un usuario por su ID.
**Requiere autenticación.**

#### GET `/api/users/forgot_password/<email>`
Solicita el envío de un código de recuperación de contraseña al correo.

#### POST `/api/users/change_password`
Cambia la contraseña usando un código de recuperación.
**Body:**
```json
{
    "code": "ABC12",
    "email": "correo@ejemplo.com",
    "newpassword": "nuevaContraseña"
}
```

---

### Autenticación

#### POST `/api/auth/login`
Inicia sesión y retorna tokens de acceso y refresh.
**Body:**
```json
{
    "email": "correo@ejemplo.com",
    "password": "contraseña"
}
```

#### POST `/api/auth/logout`
Cierra la sesión del usuario (invalida el token).
**Requiere autenticación.**

#### POST `/api/auth/refresh`
Renueva los tokens de autenticación.
**Requiere autenticación.**

---

### Medidas de Glucosa

#### GET `/api/measurements/get`
Obtiene todas las mediciones del usuario autenticado.
**Requiere autenticación.**

#### GET `/api/measurements/get/<id>`
Obtiene una medición específica por ID.
**Requiere autenticación.**

#### GET `/api/measurements/get/start_date/<start_date>/end_date/<end_date>`
Obtiene mediciones en un rango de fechas.
**Requiere autenticación.**

#### POST `/api/measurements/post`
Agrega una nueva medición.
**Requiere autenticación.**
**Body:**
```json
{
    "date": "2024-06-01",
    "hour": "08:00",
    "value": 110
}
```

#### PUT `/api/measurements/put/<id>`
Actualiza una medición existente.
**Requiere autenticación.**

#### DELETE `/api/measurements/delete/<id>`
Elimina una medición por ID.
**Requiere autenticación.**

---

### HBA1C

#### GET `/api/hba1c/get`
Calcula el HBA1c de los últimos 3 meses del usuario autenticado.
**Requiere autenticación.**

#### GET `/api/hba1c/get/start_date/<start_date>/end_date/<end_date>`
Calcula el HBA1c en un rango de fechas.
**Requiere autenticación.**

#### POST `/api/hba1c/post/calculate_dosis`
Calcula la dosis de insulina recomendada.
**Requiere autenticación.**
**Body:**
```json
{
    "actual_glucose": 150,
    "objective_glucose": 100,
    "carbohydrates": 60
}
```