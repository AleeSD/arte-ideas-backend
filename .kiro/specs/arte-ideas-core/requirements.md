# Requirements Document - Arte Ideas Core App

## Introduction

Sistema multi-tenant para estudios fotográficos que permite gestión de perfiles de usuario y configuración del sistema. El Core App maneja la autenticación, autorización, multi-tenancy y los módulos de Mi Perfil y Configuración.

## Glossary

- **Sistema**: Arte Ideas Core App
- **Tenant**: Instancia aislada del sistema para un estudio fotográfico específico
- **Usuario_Global**: Super administrador que puede acceder a múltiples tenants
- **Usuario_Tenant**: Usuario que solo puede acceder a su tenant específico
- **Datos_Globales**: Información compartida entre todos los tenants
- **Datos_Tenant**: Información aislada por tenant

## Requirements

### Requirement 1 - Multi-Tenancy

**User Story:** Como administrador del sistema, quiero que cada estudio fotográfico tenga sus datos completamente aislados, para que no puedan ver información de otros estudios.

#### Acceptance Criteria

1. WHEN el Sistema inicia, THE Sistema SHALL crear esquemas separados para cada tenant en MySQL
2. WHEN un Usuario_Tenant accede al sistema, THE Sistema SHALL mostrar únicamente datos de su tenant
3. WHEN un Usuario_Global accede al sistema, THE Sistema SHALL permitir seleccionar y gestionar cualquier tenant
4. THE Sistema SHALL mantener Datos_Globales compartidos entre todos los tenants
5. THE Sistema SHALL aislar completamente los Datos_Tenant entre diferentes tenants

### Requirement 2 - Gestión de Usuarios y Roles

**User Story:** Como administrador, quiero gestionar usuarios con roles específicos y permisos granulares, para controlar el acceso a diferentes funcionalidades del sistema.

#### Acceptance Criteria

1. THE Sistema SHALL soportar cinco roles: admin, manager, employee, photographer, assistant
2. WHEN se asigna un rol a un usuario, THE Sistema SHALL aplicar automáticamente los permisos correspondientes
3. THE Sistema SHALL permitir permisos granulares por módulo y acción sensible
4. WHEN un usuario intenta acceder a una funcionalidad, THE Sistema SHALL verificar sus permisos antes de permitir el acceso
5. THE Sistema SHALL mantener un registro de actividad de todos los usuarios

### Requirement 3 - Módulo Mi Perfil

**User Story:** Como usuario del sistema, quiero gestionar mi información personal y ver mis estadísticas de rendimiento, para mantener mi perfil actualizado y monitorear mi actividad.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar información personal completa del usuario (nombre, email, teléfono, rol, dirección, biografía)
2. THE Sistema SHALL permitir cambiar email con validación y confirmación
3. THE Sistema SHALL permitir cambiar contraseña con validaciones de seguridad
4. THE Sistema SHALL mostrar estadísticas mensuales (pedidos procesados, clientes atendidos, sesiones realizadas, horas trabajadas)
5. THE Sistema SHALL mostrar actividad reciente del usuario en orden cronológico

### Requirement 4 - Módulo Configuración

**User Story:** Como administrador, quiero configurar usuarios, datos del negocio y permisos del sistema, para personalizar la plataforma según las necesidades del estudio.

#### Acceptance Criteria

1. THE Sistema SHALL permitir gestionar usuarios (crear, editar, desactivar) dentro del tenant
2. THE Sistema SHALL permitir configurar datos del negocio (nombre, dirección, teléfono, email, RUC, moneda)
3. THE Sistema SHALL permitir configurar permisos por rol con toggles para módulos y acciones sensibles
4. THE Sistema SHALL mostrar advertencias de seguridad para acciones sensibles
5. THE Sistema SHALL permitir restablecer permisos por defecto para cada rol

### Requirement 5 - Base de Datos y Configuración

**User Story:** Como desarrollador, quiero una configuración robusta con MySQL y multi-tenancy, para asegurar escalabilidad y aislamiento de datos.

#### Acceptance Criteria

1. THE Sistema SHALL usar MySQL como base de datos principal
2. THE Sistema SHALL crear automáticamente tenants de prueba A y B durante la inicialización
3. THE Sistema SHALL configurar Django Admin para gestión sin interfaz gráfica
4. THE Sistema SHALL implementar middleware para manejo automático de tenants
5. THE Sistema SHALL proporcionar APIs REST compatibles con el frontend React existente

### Requirement 6 - Seguridad y Autenticación

**User Story:** Como usuario del sistema, quiero un sistema de autenticación seguro con JWT, para proteger mi información y la del estudio.

#### Acceptance Criteria

1. THE Sistema SHALL implementar autenticación JWT con tokens de acceso y refresh
2. THE Sistema SHALL validar permisos en cada endpoint de la API
3. THE Sistema SHALL registrar todas las acciones sensibles en logs de auditoría
4. THE Sistema SHALL implementar validaciones de seguridad para cambios de email y contraseña
5. THE Sistema SHALL manejar sesiones de usuario con expiración automática