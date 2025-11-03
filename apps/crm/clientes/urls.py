from django.urls import path
from . import views

urlpatterns = [
    path('api/clientes/', views.listar_clientes, name='listar_clientes'),
    path('api/clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('api/clientes/<int:pk>/', views.detalle_cliente, name='detalle_cliente'),
    path('api/clientes/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('api/clientes/<int:pk>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
]