# API de Gestión de Clientes - Arte Ideas

Documentación completa de los endpoints disponibles para la gestión de clientes en el sistema CRM de Arte Ideas.

## Autenticación

Todos los endpoints requieren autenticación. Incluir el token de autenticación en el header de la solicitud:
```
Authorization: Token tu_token_de_autenticación
```

## Base URL
```
http://127.0.0.1:8000
```

## Endpoints

### 1. Listar Clientes
Obtiene un listado de todos los clientes en el sistema.

**Método:** `GET`  
**URL:** `/api/clientes/`

#### Ejemplo de respuesta exitosa (200 OK):
```json
{
   [ 
{
    "clientes": [
        {
            "id": 1,
            "nombre_completo": "Rodolfo Anguñp",
            "tipo_cliente": "particular",
            "dni": "12345677",
            "ruc": null,
            "telefono_contacto": "789456123",
            "email": "pruebita1234@gmail.com",
            "direccion": "awdasd"
        },
        {
            "id": 2,
            "nombre_completo": "Sideral Carrion",
            "tipo_cliente": "colegio",
            "dni": null,
            "ruc": "12345678912",
            "telefono_contacto": "920920320",
            "email": "ie@gmaiil.com",
            "direccion": "kteimporata"
        },
        {
            "id": 3,
            "nombre_completo": "matachamos sac",
            "tipo_cliente": "empresa",
            "dni": null,
            "ruc": "22233311177",
            "telefono_contacto": "50588707",
            "email": "recursos@gmail.com",
            "direccion": "kteimporata"
        },
    ]
}
    ]
}
```

---

### 2. Obtener Detalles de un Cliente
Obtiene los detalles completos de un cliente específico.

**Método:** `GET`  
**URL:** `/api/clientes/{id}/`

#### Parámetros de ruta:
- `id`: ID numérico del cliente

#### Ejemplo de respuesta exitosa (200 OK):
```json
{
    "id": 2,
    "nombre_completo": "Sideral Carrion",
    "tipo_cliente": "colegio",
    "dni": null,
    "ruc": "12345678912",
    "telefono_contacto": "920920320",
    "email": "ie@gmaiil.com",
    "direccion": "kteimporata",
    "institucion_educativa": "ie tu mamaita sideral carrion",
    "detalles_adicionales": "asfgsegeseagawgagwagw",
    "pedidos": 40,
    "total_gastado": 500000.0,
    "ultima_fecha_pedido": "2025-11-03"
}
```

#### Posibles códigos de error:
- 404: Cliente no encontrado

---

### 3. Crear un Nuevo Cliente
Crea un nuevo registro de cliente en el sistema.

**Método:** `POST`  
**URL:** `/api/clientes/crear/`

#### Cuerpo de la solicitud (JSON):
```json
{
  "nombre_completo": "Nuevo Clientessssssssssssssssssssss",
  "tipo_cliente": "particular",
  "dni": "12345675",
  "telefono_contacto": "987654321",
  "email": "nuevo@cliente.com",
  "direccion": "Dirección del cliente",
  "pedidos" : "32",
  "total_gastado" : "8000"
}
```

#### Campos requeridos:
- `nombre`: Nombre completo o razón social del cliente
- `email`: Correo electrónico (debe tener formato válido)

#### Respuesta exitosa (201 Created):
```json
{
    "id": 5,
    "message": "Cliente creado exitosamente"
}
```

---

### 4. Actualizar un Cliente
Actualiza la información de un cliente existente.

**Método:** `PUT`  
**URL:** `/api/clientes/{id}/editar/`

#### Parámetros de ruta:
- `id`: ID numérico del cliente a actualizar

#### Cuerpo de la solicitud (JSON):
```json
{
    "nombre": "Cliente Actualizado S.A.S",
    "email": "nuevoemail@cliente.com",
    "telefono": "+573001234567",
    "direccion": "Avenida Actualizada #45-67"
}
```

#### Respuesta exitosa (200 OK):
```json
{
    "id": 3,
    "message": "Cliente actualizado exitosamente"
}
```

---

### 5. Eliminar un Cliente
Elimina permanentemente un cliente del sistema.

**Método:** `DELETE`  
**URL:** `/api/clientes/{id}/eliminar/`

#### Parámetros de ruta:
- `id`: ID numérico del cliente a eliminar

#### Respuesta exitosa (204 No Content):
```
Cuerpo de respuesta vacío
```

#### Posibles códigos de error:
- 404: Cliente no encontrado
- 403: No autorizado
- 400: No se puede eliminar el cliente (por ejemplo, si tiene registros relacionados)

## Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - La solicitud se completó correctamente |
| 201 | Creado - Recurso creado exitosamente |
| 204 | Sin Contenido - Operación exitosa sin contenido que devolver |
| 400 | Solicitud Incorrecta - La solicitud no pudo ser procesada |
| 401 | No Autorizado - Se requiere autenticación |
| 403 | Prohibido - No tiene permisos para realizar esta acción |
| 404 | No Encontrado - El recurso solicitado no existe |
| 500 | Error Interno del Servidor - Error inesperado en el servidor |

## Ejemplo de Uso con cURL

### Listar clientes:
```bash
curl -X GET \
  http://127.0.0.1:8000/api/clientes/ \
  -H 'Authorization: Token tu_token_de_autenticacion'
```

### Crear un nuevo cliente:
```bash
curl -X POST \
  http://127.0.0.1:8000/api/clientes/crear/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Token tu_token_de_autenticacion' \
  -d '{
    "nombre": "Ejemplo S.A.S",
    "email": "ejemplo@empresa.com",
    "telefono": "+573001234567",
    "direccion": "Carrera 15 #25-35"
  }'
```

## Notas Adicionales

- Todas las fechas y horas están en formato ISO 8601 (UTC).
- Los límites de tasa de solicitud están configurados para prevenir abusos.
- Se recomienda implementar paginación para listados que puedan contener muchos registros.
- Para soporte adicional, contacte al equipo de desarrollo en soporte@arteideas.com.