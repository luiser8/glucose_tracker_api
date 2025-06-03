# API de Glucosa

## Endpoints

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