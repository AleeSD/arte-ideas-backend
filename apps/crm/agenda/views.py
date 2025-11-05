from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils.dateparse import parse_date
from django.shortcuts import render
from datetime import datetime

from .data import eventos_ordenados, EVENTOS
from .utils import build_month_calendar, build_week_view, build_day_view


class UpcomingEventsView(APIView):
    """Endpoint de Próximos Eventos (fuente oficial del calendario)."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        limit = request.query_params.get("limit")
        events = eventos_ordenados()
        if limit:
            try:
                l = int(limit)
                if l > 0:
                    events = events[:l]
            except ValueError:
                pass
        return Response(events)


class CalendarView(APIView):
    """Genera el calendario y ubica los eventos por día (vista mensual)."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        view = request.query_params.get("view", "month").lower()

        events = eventos_ordenados()

        if view == "month":
            # Año y mes requeridos
            try:
                year = int(request.query_params.get("year"))
                month = int(request.query_params.get("month"))
            except (TypeError, ValueError):
                return Response({
                    "detail": "Parámetros inválidos: year y month son requeridos"
                }, status=status.HTTP_400_BAD_REQUEST)

            calendar = build_month_calendar(year, month, events)
            return Response({
                "view": "month",
                **calendar,
                "upcoming_count": len(events),
            })

        elif view == "week":
            # Año, mes y día requeridos como ancla de la semana
            try:
                year = int(request.query_params.get("year"))
                month = int(request.query_params.get("month"))
                day = int(request.query_params.get("day"))
            except (TypeError, ValueError):
                return Response({
                    "detail": "Parámetros inválidos: year, month y day son requeridos"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = build_week_view(year, month, day, events)
            return Response({
                "view": "week",
                **data,
                "upcoming_count": len(events),
            })

        elif view == "day":
            try:
                year = int(request.query_params.get("year"))
                month = int(request.query_params.get("month"))
                day = int(request.query_params.get("day"))
            except (TypeError, ValueError):
                return Response({
                    "detail": "Parámetros inválidos: year, month y day son requeridos"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = build_day_view(year, month, day, events)
            return Response({
                "view": "day",
                **data,
                "upcoming_count": len(events),
            })

        else:
            return Response({
                "detail": "Vista inválida. Use view=month|week|day"
            }, status=status.HTTP_400_BAD_REQUEST)


def agenda_ui(request):
    """Vista ligera (sin frontend framework) para visualizar la Agenda."""
    # Valores por defecto alineados a la imagen: noviembre 2025
    ctx = {
        "default_year": 2025,
        "default_month": 11,
        "default_day": 10,
    }
    return render(request, "agenda/index.html", ctx)


class EventCreateView(APIView):
    """Crea un nuevo evento en memoria.
    Requiere JSON: { "titulo", "fecha" (YYYY-MM-DD), "hora" (HH:MM), "tipo" }
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # evitar CSRF por SessionAuthentication

    def post(self, request):
        data = request.data or {}
        titulo = (data.get("titulo") or "").strip()
        fecha = data.get("fecha")
        hora = data.get("hora")
        tipo = data.get("tipo")

        tipos_validos = {"Entrega", "Sesión Fotográfica", "Recordatorio"}

        # Validaciones básicas
        if not titulo:
            return Response({"detail": "titulo es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        if not fecha or not parse_date(fecha):
            return Response({"detail": "fecha inválida (YYYY-MM-DD)"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            datetime.strptime(hora or "", "%H:%M")
        except Exception:
            return Response({"detail": "hora inválida (HH:MM)"}, status=status.HTTP_400_BAD_REQUEST)
        if tipo not in tipos_validos:
            return Response({"detail": f"tipo inválido. Use uno de {sorted(tipos_validos)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Asignar id incremental
        next_id = (max([e.get("id", 0) for e in EVENTOS]) + 1) if EVENTOS else 1
        nuevo = {
            "id": next_id,
            "titulo": titulo,
            "fecha": fecha,
            "hora": hora,
            "tipo": tipo,
        }
        EVENTOS.append(nuevo)
        # Retornar creado
        return Response(nuevo, status=status.HTTP_201_CREATED)