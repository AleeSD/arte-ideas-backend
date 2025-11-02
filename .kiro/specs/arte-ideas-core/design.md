# Design Document - Arte Ideas Core App

## Overview

El Core App de Arte Ideas implementa un sistema multi-tenant robusto para estudios fotográficos, proporcionando gestión de usuarios, perfiles y configuración del sistema. Basado en las HU específicas del documento y el análisis del frontend mostrado en las imágenes, el sistema maneja:

- **Mi Perfil (HU01, HU02)**: Visualización de perfil y rendimiento, autogestión de seguridad y datos personales
- **Configuración (HU01, HU02, HU03)**: Administración de usuarios, configuración del negocio, roles y permisos
- **Multi-tenancy**: 2 tenants de prueba (A y B) con aislamiento completo
- **Roles específicos**: admin, manager, employee, photographer, assistant con permisos granulares
- **Base de datos**: MySQL (usuario: root, contraseña: 12345)
- **Django Admin**: Para gestión sin interfaz gráfica
- **Compatibilidad**: APIs REST para el frontend React existente

## Architecture

### Multi-Tenancy Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Global Database                          │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │   Shared Data   │  │   Tenant Data   │                 │
│  │  - Tenants      │  │  - Users        │                 │
│  │  - Domains      │  │  - Profiles     │                 │
│  │  - Global Config│  │  - Activities   │                 │
│  └─────────────────┘  └─────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

### System Components

1. **Tenant Management**: django-tenants para aislamiento de esquemas
2. **Authentication**: JWT con django-rest-framework-simplejwt
3. **Database**: MySQL con esquemas separados por tenant
4. **API Layer**: Django REST Framework
5. **Admin Interface**: Django Admin personalizado

## Components and Interfaces

### 1. Models Structure

#### Shared Models (Global)
```python
# Modelos que existen en el esquema público
- Tenant: Información del estudio fotográfico
- Domain: Dominios asociados a cada tenant
- GlobalConfiguration: Configuraciones compartidas
```

#### Tenant Models (Per Tenant)
```python
# Modelos que existen en cada esquema de tenant
- User: Usuario personalizado con roles específicos
- UserProfile: Perfil extendido con estadísticas
- UserActivity: Registro de actividad del usuario
- SystemConfiguration: Configuraciones por tenant
- ConfigurationHistory: Historial de cambios
```

### 2. User Roles and Permissions

#### Role Hierarchy
```
Super Admin (Global)
├── Acceso a todos los tenants
├── Gestión de tenants
└── Configuraciones globales

Admin (Per Tenant)
├── Gestión completa del tenant
├── Todos los módulos y acciones
└── Gestión de usuarios

Manager (Per Tenant)
├── Gestión de CRM, Commerce, Operations
├── Acceso a reportes y costos
└── Edición de precios

Employee (Per Tenant)
├── Acceso básico a CRM y Commerce
├── Lectura de clientes e inventario
└── Escritura de pedidos

Photographer (Per Tenant)
├── Gestión de sesiones fotográficas
├── Acceso a operaciones
└── Gestión de producción

Assistant (Per Tenant)
├── Acceso básico a CRM
├── Gestión de agenda
└── Lectura de pedidos
```

### 3. API Endpoints Structure (Basado en Frontend Analizado)

#### Authentication Endpoints
```
POST /api/auth/login/          # Login con JWT
POST /api/auth/refresh/        # Refresh token
POST /api/auth/logout/         # Logout
POST /api/auth/change-password/ # Cambiar contraseña (botón en Mi Perfil)
POST /api/auth/change-email/    # Cambiar email (botón en Mi Perfil)
```

#### Profile Management (Pantalla "Mi Perfil")
```
GET    /api/profile/           # Datos personales completos
PUT    /api/profile/           # Editar perfil (botón "Editar Perfil")
GET    /api/profile/statistics/ # Estadísticas: Pedidos (234), Clientes (89), Sesiones (45), Horas (180)
GET    /api/profile/activity/   # Actividad reciente cronológica
GET    /api/profile/completion/ # Porcentaje de completitud del perfil
```

#### Configuration Management (Pantalla "Configuración")

##### Gestión de Usuarios (Sección 1)
```
GET    /api/config/users/      # Tabla: USUARIO, EMAIL, ROL, ESTADO, ACCIONES
POST   /api/config/users/      # Crear usuario (botón "Nuevo Usuario")
PUT    /api/config/users/{id}/ # Actualizar usuario
PATCH  /api/config/users/{id}/toggle/ # Activar/Desactivar usuario
```

##### Configuración del Negocio (Sección 2)
```
GET    /api/config/business/   # Datos: Nombre, Dirección, Teléfono, Email, RUC, Moneda
PUT    /api/config/business/   # Guardar configuración (botón "Guardar Configuración")
```

##### Roles y Permisos (Pantalla separada)
```
GET    /api/config/roles/      # Lista de roles disponibles
GET    /api/config/permissions/{role}/ # Permisos específicos por rol
PUT    /api/config/permissions/{role}/ # Guardar permisos (botón "Guardar Permisos")
POST   /api/config/permissions/{role}/reset/ # Restablecer por defecto

# Módulos con toggle: Dashboard, Pedidos, Inventario, Gastos, Contratos, 
#                    Agenda, Clientes, Activos, Producción, Reportes
# Acciones sensibles: Ver Costos, Ver Precios, Ver Márgenes, Ver Datos Clientes,
#                    Ver Datos Financieros, Editar Precios, Eliminar Registros
```

#### Super Admin Endpoints (Gestión Multi-Tenant)
```
GET    /api/admin/tenants/     # Lista de tenants A y B
POST   /api/admin/tenants/     # Crear nuevo tenant
GET    /api/admin/tenants/{id}/users/ # Usuarios de un tenant específico
POST   /api/admin/switch-tenant/{id}/ # Cambiar contexto de tenant
```

## Data Models

### Tenant Model (Shared)
```python
class Tenant(TenantMixin):
    name = CharField(max_length=100)
    business_name = CharField(max_length=200)
    business_address = TextField()
    business_phone = CharField(max_length=20)
    business_email = EmailField()
    business_ruc = CharField(max_length=20)
    currency = CharField(choices=CURRENCY_CHOICES)
    max_users = PositiveIntegerField(default=10)
    features_enabled = JSONField(default=dict)
    is_active = BooleanField(default=True)
```

### User Model (Per Tenant)
```python
class User(AbstractUser):
    id = UUIDField(primary_key=True)
    phone = CharField(max_length=20)
    address = TextField()
    biography = TextField()
    avatar = ImageField()
    role = CharField(choices=ROLE_CHOICES)
    is_verified = BooleanField(default=False)
    theme = CharField(default='light')
    language = CharField(default='es')
    notifications_enabled = BooleanField(default=True)
```

### UserProfile Model (Per Tenant)
```python
class UserProfile(Model):
    user = OneToOneField(User)
    orders_processed = PositiveIntegerField(default=0)
    clients_attended = PositiveIntegerField(default=0)
    sessions_completed = PositiveIntegerField(default=0)
    hours_worked = PositiveIntegerField(default=0)
    show_statistics = BooleanField(default=True)
    show_recent_activity = BooleanField(default=True)
```

### SystemConfiguration Model (Per Tenant)
```python
class SystemConfiguration(Model):
    module = CharField(choices=MODULE_CHOICES)
    key = CharField(max_length=100)
    value = TextField()
    data_type = CharField(choices=DATA_TYPE_CHOICES)
    is_editable = BooleanField(default=True)
```

## Error Handling

### API Error Responses
```python
# Estructura estándar de errores
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Los datos proporcionados no son válidos",
        "details": {
            "field_name": ["Error específico del campo"]
        }
    }
}
```

### Error Types
- `AUTHENTICATION_ERROR`: Errores de autenticación
- `PERMISSION_DENIED`: Sin permisos para la acción
- `VALIDATION_ERROR`: Errores de validación de datos
- `NOT_FOUND`: Recurso no encontrado
- `TENANT_ERROR`: Errores relacionados con multi-tenancy

## Testing Strategy

### Unit Tests
- Modelos: Validaciones y métodos personalizados
- Serializers: Validación de datos y transformaciones
- Services: Lógica de negocio
- Permissions: Sistema de permisos por rol

### Integration Tests
- APIs: Endpoints completos con autenticación
- Multi-tenancy: Aislamiento de datos entre tenants
- Workflows: Flujos completos de usuario

### Test Data (Configuración Específica)

#### Tenants de Prueba
- **Tenant A**: Estudio Fotográfico A
  - Dominio: tenant-a.localhost:8000
  - Ubicación: Lima, Perú
  - Restricciones: Acceso completo a datos globales
  - Configuración: Datos de prueba configurables
- **Tenant B**: Estudio Fotográfico B  
  - Dominio: tenant-b.localhost:8000
  - Ubicación: Provincia, Perú
  - Restricciones: Acceso limitado a ciertos datos globales
  - Configuración: Datos de prueba configurables

**Nota**: Los datos mostrados en las imágenes del frontend son solo ejemplos para demostración al cliente. Los datos reales serán configurables por cada tenant.

#### Usuarios de Prueba
**Super Admin (Global)**
- Username: superadmin
- Email: admin@arteideas.com
- Acceso: Ambos tenants A y B

**Tenant A - Usuarios**
- Admin: admin_a / admin@tenant-a.com (Administrador)
- User: user_a / user@tenant-a.com (Empleado)

**Tenant B - Usuarios**  
- Admin: admin_b / admin@tenant-b.com (Administrador)
- User: user_b / user@tenant-b.com (Empleado)

#### Configuración MySQL
- Host: localhost
- Puerto: 3306
- Usuario: root
- Contraseña: 12345
- Base de datos: arte_ideas_db

## Security Considerations

### Authentication & Authorization
- JWT tokens con expiración configurable
- Refresh tokens con rotación automática
- Validación de permisos en cada endpoint
- Rate limiting para endpoints sensibles

### Data Protection
- Aislamiento completo entre tenants
- Validación de entrada en todos los endpoints
- Sanitización de datos de salida
- Logs de auditoría para acciones sensibles

### Password Security
- Validación de complejidad de contraseñas
- Confirmación por email para cambios críticos
- Bloqueo temporal por intentos fallidos
- Historial de contraseñas para evitar reutilización

## Performance Optimization

### Database
- Índices optimizados para consultas frecuentes
- Conexiones de base de datos por tenant
- Cache de configuraciones frecuentes
- Paginación en listados grandes

### API Response
- Serialización optimizada
- Campos calculados en cache
- Compresión de respuestas
- Versionado de API para compatibilidad
## F
rontend Integration (Basado en Imágenes Analizadas)

### Mi Perfil - Layout Específico
```
┌─────────────────────────────────────────────────────────────┐
│ Mi Perfil - Gestiona tu información personal               │
│ [Cambiar Email] [Cambiar Contraseña] [Editar Perfil]      │
├─────────────────────────┬───────────────────────────────────┤
│ DATOS PERSONALES        │ ESTADÍSTICAS Y ACTIVIDAD         │
│                         │                                   │
│ 👤 Avatar + Nombre      │ 📊 Pedidos Procesados: 234       │
│ ✅ Cuenta Verificada    │ 👥 Clientes Atendidos: 89        │
│                         │ 📸 Sesiones Realizadas: 45       │
│ Nombre Completo: ___    │ ⏰ Horas Trabajadas: 180         │
│ Email: ___              │                                   │
│ Teléfono: ___           │ ACTIVIDAD RECIENTE               │
│ Rol: ___                │ • Acción 1 - Fecha               │
│ Dirección: ___          │ • Acción 2 - Fecha               │
│ Biografía: ___          │ • Acción 3 - Fecha               │
│                         │                                   │
│ Fecha registro: ___     │                                   │
│ Última conexión: ___    │                                   │
└─────────────────────────┴───────────────────────────────────┘
```

### Configuración - Layout Específico
```
┌─────────────────────────────────────────────────────────────┐
│ Configuración - Personaliza tu experiencia                 │
│                                    [Guardar Cambios]       │
├─────────────────────────────────────────────────────────────┤
│ GESTIÓN DE USUARIOS                    [Nuevo Usuario]     │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ USUARIO    │ EMAIL           │ ROL    │ ESTADO │ ACCIONES│ │
│ │ Admin      │ admin@email.com │ Admin  │ Activo │ [Edit]  │ │
│ │ Empleado   │ emp@email.com   │ Emp    │ Activo │ [Edit]  │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ CONFIGURACIÓN DEL NEGOCIO                                   │
│ Nombre de la Empresa: Arte Ideas Diseño Gráfico           │
│ Dirección: Av. Lima 123, San Juan de Lurigancho           │
│ Teléfono: 987654321                                        │
│ Email Corporativo: info@arte-ideas.com                     │
│ RUC: 20123456789                                           │
│ Moneda: [Soles (S/)] ▼                                     │
│                              [Guardar Configuración]       │
└─────────────────────────────────────────────────────────────┘
```

### Roles y Permisos - Layout Específico
```
┌─────────────────────────────────────────────────────────────┐
│ Roles y Permisos - Configura los permisos                  │
│ Seleccionar rol: [Administrador ▼] 10 módulos, 7 acciones │
├─────────────────────────────────────────────────────────────┤
│ ACCESO A MÓDULOS                                            │
│ ☑ Dashboard      ☑ Pedidos       ☑ Inventario             │
│ ☑ Gastos         ☑ Contratos     ☑ Agenda                 │
│ ☑ Clientes       ☑ Activos       ☑ Producción             │
│ ☑ Reportes                                                  │
├─────────────────────────────────────────────────────────────┤
│ ACCIONES SENSIBLES                                          │
│ ☑ Ver Costos           ☑ Ver Precios                      │
│ ☑ Ver Márgenes         ☑ Ver Datos de Clientes           │
│ ☑ Ver Datos Financieros ☑ Editar Precios                 │
│ ☑ Eliminar Registros                                       │
├─────────────────────────────────────────────────────────────┤
│ ⚠️ ADVERTENCIA DE SEGURIDAD                                │
│ Las acciones sensibles pueden afectar la seguridad y       │
│ funcionamiento del sistema. Asigna estos permisos solo     │
│ a usuarios de confianza.                                    │
│                                                             │
│ [Restablecer por Defecto]           [Guardar Permisos]     │
└─────────────────────────────────────────────────────────────┘
```

## Django Admin Customization (Vista Admin para Cliente)

### Admin Interface Requirements
La vista admin está diseñada para mostrar todas las funcionalidades al cliente, pero con permisos granulares según el rol:

#### Super Admin (Global)
- **Acceso**: Todos los tenants A y B
- **Funcionalidades**: Gestión completa de tenants, usuarios globales, configuraciones
- **Vista especial**: Selector de tenant para cambiar contexto
- **Datos globales**: Acceso completo a configuraciones compartidas

#### Admin por Tenant
- **Acceso**: Solo su tenant específico
- **Funcionalidades**: Gestión completa dentro de su tenant
- **Restricciones**: No puede ver datos de otros tenants
- **Datos globales**: Acceso según restricciones del tenant

#### Otros Roles (Manager, Employee, etc.)
- **Acceso**: Limitado según permisos del rol
- **Vista**: Solo módulos y acciones permitidas
- **Funcionalidades**: Basadas en la matriz de permisos definida

### Permisos Granulares por Ubicación/Tenant
```python
# Tenant A (Lima) - Acceso completo
TENANT_A_PERMISSIONS = {
    'global_data_access': True,
    'financial_modules': True,
    'analytics_advanced': True,
    'export_all_data': True
}

# Tenant B (Provincia) - Acceso limitado
TENANT_B_PERMISSIONS = {
    'global_data_access': False,  # Solo datos básicos
    'financial_modules': False,   # Sin módulos financieros avanzados
    'analytics_advanced': False,  # Analytics básico solamente
    'export_all_data': False     # Exportación limitada
}
```

### Admin URLs Structure
```
/admin/                    # Django Admin principal
/admin/switch-tenant/      # Cambiar contexto de tenant (super admin)
/admin/tenants/            # Gestión de tenants (solo super admin)
/admin/core/user/          # Gestión de usuarios (filtrado por tenant)
/admin/core/userprofile/   # Perfiles de usuario
/admin/core/systemconfig/  # Configuraciones del sistema
/admin/core/useractivity/  # Logs de actividad
/admin/global/config/      # Configuraciones globales (super admin)
```

### Datos Globales vs Tenant
#### Datos Compartidos (Global)
- Catálogos de productos base
- Configuraciones de sistema generales
- Templates de documentos
- Tipos de servicios estándar

#### Datos por Tenant
- Usuarios y perfiles
- Clientes específicos
- Pedidos y transacciones
- Configuraciones personalizadas
- Estadísticas y reportes

#### Restricciones por Ubicación
Los tenants pueden tener diferentes niveles de acceso a datos globales basados en:
- Ubicación geográfica
- Plan de suscripción
- Configuraciones específicas del negocio
- Regulaciones locales