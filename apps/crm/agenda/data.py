from datetime import datetime

# Datos de "Próximos eventos" proporcionados por el usuario
# Formato y campos se respetan tal cual para 0% frontend.
EVENTOS = [
    # Noviembre 2025
    {"id": 1, "titulo": "Colegio San José", "fecha": "2025-11-02", "hora": "10:00", "tipo": "Sesión Fotográfica"},
    {"id": 2, "titulo": "Roberto Silva", "fecha": "2025-11-03", "hora": "11:30", "tipo": "Sesión Fotográfica"},
    {"id": 3, "titulo": "Carlos Mendoza", "fecha": "2025-11-07", "hora": "16:30", "tipo": "Entrega"},
    {"id": 4, "titulo": "Familia Torres", "fecha": "2025-11-09", "hora": "17:00", "tipo": "Entrega"},
    {"id": 5, "titulo": "LE. Libertador", "fecha": "2025-11-09", "hora": "14:30", "tipo": "Entrega"},
    {"id": 6, "titulo": "Familia García", "fecha": "2025-11-10", "hora": "11:00", "tipo": "Sesión Fotográfica"},
    {"id": 7, "titulo": "StartUp Digital", "fecha": "2025-11-10", "hora": "11:00", "tipo": "Recordatorio"},
    {"id": 8, "titulo": "Colegio Santa Rosa", "fecha": "2025-11-11", "hora": "17:30", "tipo": "Entrega"},
    {"id": 9, "titulo": "Familia Rodríguez", "fecha": "2025-11-11", "hora": "11:30", "tipo": "Sesión Fotográfica"},
    {"id": 10, "titulo": "Colegio Salesiano", "fecha": "2025-11-15", "hora": "12:00", "tipo": "Sesión Fotográfica"},
    {"id": 11, "titulo": "LE. Bolognesi", "fecha": "2025-11-17", "hora": "13:00", "tipo": "Entrega"},
    {"id": 12, "titulo": "LE. Libertador", "fecha": "2025-11-18", "hora": "08:30", "tipo": "Sesión Fotográfica"},
    {"id": 13, "titulo": "StartUp Digital", "fecha": "2025-11-18", "hora": "12:00", "tipo": "Recordatorio"},
    {"id": 14, "titulo": "Corporación ABC", "fecha": "2025-11-21", "hora": "18:30", "tipo": "Sesión Fotográfica"},
    {"id": 15, "titulo": "Empresa TechCorp", "fecha": "2025-11-23", "hora": "17:30", "tipo": "Recordatorio"},
    {"id": 16, "titulo": "Familia Rodríguez", "fecha": "2025-11-24", "hora": "14:30", "tipo": "Recordatorio"},
    {"id": 17, "titulo": "Colegio La Salle", "fecha": "2025-11-24", "hora": "18:30", "tipo": "Sesión Fotográfica"},
    {"id": 18, "titulo": "María González Rodríguez", "fecha": "2025-11-25", "hora": "10:30", "tipo": "Recordatorio"},
    {"id": 19, "titulo": "Corporación ABC", "fecha": "2025-11-28", "hora": "14:00", "tipo": "Sesión Fotográfica"},
    {"id": 20, "titulo": "I.E. Bolognesi", "fecha": "2025-11-29", "hora": "19:30", "tipo": "Recordatorio"},
    {"id": 21, "titulo": "L.E. Bolognesi", "fecha": "2025-11-30", "hora": "14:00", "tipo": "Recordatorio"},
    # Diciembre 2025
    {"id": 22, "titulo": "I.E. San Martín de Porres - Sto A", "fecha": "2025-12-01", "hora": "09:30", "tipo": "Recordatorio"},
    {"id": 23, "titulo": "Ana María López", "fecha": "2025-12-01", "hora": "12:00", "tipo": "Entrega"},
    {"id": 24, "titulo": "Colegio La Salle", "fecha": "2025-12-05", "hora": "13:00", "tipo": "Sesión Fotográfica"},
    {"id": 25, "titulo": "Empresa TechCorp", "fecha": "2025-12-06", "hora": "17:00", "tipo": "Recordatorio"},
    {"id": 26, "titulo": "Colegio San José", "fecha": "2025-12-06", "hora": "12:30", "tipo": "Entrega"},
    {"id": 27, "titulo": "Colegio La Salle", "fecha": "2025-12-07", "hora": "16:00", "tipo": "Entrega"},
    {"id": 28, "titulo": "Colegio Salesiano", "fecha": "2025-12-09", "hora": "12:30", "tipo": "Sesión Fotográfica"},
    {"id": 29, "titulo": "Colegio San José", "fecha": "2025-12-12", "hora": "16:30", "tipo": "Entrega"},
    {"id": 30, "titulo": "Colegio La Salle", "fecha": "2025-12-13", "hora": "14:00", "tipo": "Recordatorio"},
    {"id": 31, "titulo": "Empresa Global", "fecha": "2025-12-15", "hora": "17:00", "tipo": "Recordatorio"},
    {"id": 32, "titulo": "Patricia Vásquez", "fecha": "2025-12-19", "hora": "08:00", "tipo": "Recordatorio"},
    # Enero 2026
    {"id": 33, "titulo": "Familia Morales", "fecha": "2026-01-01", "hora": "19:30", "tipo": "Entrega"},
    {"id": 34, "titulo": "Carlos Mendoza", "fecha": "2026-01-01", "hora": "12:30", "tipo": "Recordatorio"},
    {"id": 35, "titulo": "LE. Bolognesi", "fecha": "2026-01-01", "hora": "12:30", "tipo": "Recordatorio"},
    {"id": 36, "titulo": "Roberto Silva", "fecha": "2026-01-02", "hora": "16:30", "tipo": "Sesión Fotográfica"},
    {"id": 37, "titulo": "LE. Bolognesi", "fecha": "2026-01-03", "hora": "14:30", "tipo": "Sesión Fotográfica"},
    {"id": 38, "titulo": "Colegio San José", "fecha": "2026-01-06", "hora": "16:00", "tipo": "Sesión Fotográfica"},
    {"id": 39, "titulo": "LE. San Martín de Porres - Sto A", "fecha": "2026-01-08", "hora": "11:30", "tipo": "Sesión Fotográfica"},
    {"id": 40, "titulo": "I.E. San Martín de Porres - 5to A", "fecha": "2026-01-09", "hora": "08:00", "tipo": "Sesión Fotográfica"},
    {"id": 41, "titulo": "I.E. San Martín de Porres - 5to A", "fecha": "2026-01-09", "hora": "15:00", "tipo": "Recordatorio"},
    {"id": 42, "titulo": "Colegio San José", "fecha": "2026-01-09", "hora": "09:30", "tipo": "Sesión Fotográfica"},
    {"id": 43, "titulo": "LE. Bolognesi", "fecha": "2026-01-08", "hora": "13:30", "tipo": "Sesión Fotográfica"},
    {"id": 44, "titulo": "StartUp Digital", "fecha": "2026-01-12", "hora": "12:00", "tipo": "Recordatorio"},
    {"id": 45, "titulo": "StartUp Digital", "fecha": "2026-01-14", "hora": "10:00", "tipo": "Recordatorio"},
    {"id": 46, "titulo": "Empresa Global", "fecha": "2026-01-15", "hora": "14:00", "tipo": "Sesión Fotográfica"},
    {"id": 47, "titulo": "Universidad Nacional", "fecha": "2026-01-15", "hora": "12:00", "tipo": "Recordatorio"},
    {"id": 48, "titulo": "Roberto Silva", "fecha": "2026-01-17", "hora": "08:00", "tipo": "Sesión Fotográfica"},
    {"id": 49, "titulo": "StartUp Digital", "fecha": "2026-01-18", "hora": "08:00", "tipo": "Entrega"},
    {"id": 50, "titulo": "Patricia Vásquez", "fecha": "2026-01-19", "hora": "10:00", "tipo": "Entrega"},
    {"id": 51, "titulo": "Colegio San José", "fecha": "2026-01-11", "hora": "17:30", "tipo": "Entrega"},
]


def _parse_dt(fecha: str, hora: str) -> datetime:
    """Parse helper para ordenar por fecha/hora."""
    return datetime.fromisoformat(f"{fecha}T{hora}:00")


def eventos_ordenados():
    """Retorna los eventos ordenados por fecha y hora ascendente."""
    return sorted(EVENTOS, key=lambda e: _parse_dt(e["fecha"], e["hora"]))