"""
URLs del Módulo Agenda - CRM
"""
from django.urls import path
from .views import UpcomingEventsView, CalendarView, agenda_ui, EventCreateView

app_name = 'agenda'

urlpatterns = [
    path('upcoming/', UpcomingEventsView.as_view(), name='upcoming'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('events/', EventCreateView.as_view(), name='events_create'),
    # UI ligera para visualizar la Agenda
    path('ui/', agenda_ui, name='ui'),
]