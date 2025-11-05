from datetime import date, datetime, timedelta
from calendar import monthrange
from typing import List, Dict, Any


def build_month_calendar(year: int, month: int, events: List[Dict[str, Any]]):
    """
    Construye estructura de calendario mensual:
    {
      "year": 2025, "month": 11,
      "weeks": [ {"days": [ {"date": "2025-11-01", "events": [...] , "in_month": True } ] } ]
    }
    """
    # Primer y último día del mes
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])

    # Normaliza para iniciar el calendario en domingo (como la imagen de referencia)
    # Buscar el domingo anterior/al mismo al primer día
    start_delta = (first_day.weekday() + 1) % 7  # 6 = domingo -> delta 0
    calendar_start = first_day - timedelta(days=start_delta)

    # Termina el sábado de la última semana visible
    end_delta = (5 - last_day.weekday()) % 7  # 5 = sábado
    calendar_end = last_day + timedelta(days=end_delta)

    # Mapear eventos por fecha
    events_by_date: Dict[str, List[Dict[str, Any]]] = {}
    for e in events:
        events_by_date.setdefault(e["fecha"], []).append(e)

    # Ordenar los eventos por hora
    for d, lst in events_by_date.items():
        lst.sort(key=lambda e: datetime.fromisoformat(f"{e['fecha']}T{e['hora']}:00"))

    # Construir semanas
    weeks = []
    cursor = calendar_start
    while cursor <= calendar_end:
        week_days = []
        for _ in range(7):
            dstr = cursor.isoformat()
            week_days.append({
                "date": dstr,
                "in_month": (cursor.month == month),
                "events": events_by_date.get(dstr, []),
            })
            cursor += timedelta(days=1)
        weeks.append({"days": week_days})

    return {
        "year": year,
        "month": month,
        "weeks": weeks,
        "days_count": (calendar_end - calendar_start).days + 1,
    }


def build_week_view(year: int, month: int, day: int, events: List[Dict[str, Any]]):
    """
    Construye estructura de calendario semanal iniciando en lunes y finalizando en domingo.
    Respuesta:
    {
      "year": 2025, "month": 11, "week_start": "2025-11-03", "week_end": "2025-11-09",
      "days": [ {"date": "2025-11-03", "events": [...]} ]
    }
    """
    anchor = date(year, month, day)
    # domingo de la semana del anchor
    start_of_week = anchor - timedelta(days=(anchor.weekday() + 1) % 7)
    end_of_week = start_of_week + timedelta(days=6)

    # Mapear eventos por fecha
    events_by_date: Dict[str, List[Dict[str, Any]]] = {}
    for e in events:
        events_by_date.setdefault(e["fecha"], []).append(e)

    # Ordenar eventos por hora en cada día
    for d, lst in events_by_date.items():
        lst.sort(key=lambda e: datetime.fromisoformat(f"{e['fecha']}T{e['hora']}:00"))

    # Construir días
    days = []
    cursor = start_of_week
    while cursor <= end_of_week:
        dstr = cursor.isoformat()
        days.append({
            "date": dstr,
            "events": events_by_date.get(dstr, []),
            "in_week": True,
        })
        cursor += timedelta(days=1)

    return {
        "year": year,
        "month": month,
        "week_start": start_of_week.isoformat(),
        "week_end": end_of_week.isoformat(),
        "days": days,
    }


def build_day_view(year: int, month: int, day: int, events: List[Dict[str, Any]]):
    """
    Construye estructura para vista diaria.
    Respuesta:
    {
      "date": "2025-11-10",
      "events": [ { id, titulo, fecha, hora, tipo } ]
    }
    """
    current = date(year, month, day)
    dstr = current.isoformat()

    # Filtrar y ordenar eventos del día
    day_events = [e for e in events if e.get("fecha") == dstr]
    day_events.sort(key=lambda e: datetime.fromisoformat(f"{e['fecha']}T{e['hora']}:00"))

    return {
        "date": dstr,
        "events": day_events,
    }