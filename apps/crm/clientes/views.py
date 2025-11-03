from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .models import Cliente
from .forms import ClienteForm

# Listar todos los clientes
def listar_clientes(request):
    clientes = list(Cliente.objects.values('id', 'nombre_completo', 'tipo_cliente', 'dni', 'ruc', 'telefono_contacto', 'email', 'direccion'))
    return JsonResponse({'clientes': clientes}, safe=False)

# Ver detalles de un cliente
def detalle_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
        return JsonResponse({
            'id': cliente.id,
            'nombre_completo': cliente.nombre_completo,
            'tipo_cliente': cliente.tipo_cliente,
            'dni': cliente.dni,
            'ruc': cliente.ruc,
            'telefono_contacto': cliente.telefono_contacto,
            'email': cliente.email,
            'direccion': cliente.direccion,
            'institucion_educativa': cliente.institucion_educativa,
            'detalles_adicionales': cliente.detalles_adicionales,
            'pedidos': cliente.pedidos,
            'total_gastado': float(cliente.total_gastado) if cliente.total_gastado else 0.0,
            'ultima_fecha_pedido': cliente.ultima_fecha_pedido.isoformat() if cliente.ultima_fecha_pedido else None,
        })
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

# Crear un nuevo cliente
@csrf_exempt
@require_http_methods(["POST"])
def crear_cliente(request):
    try:
        data = json.loads(request.body)
        form = ClienteForm(data)
        if form.is_valid():
            cliente = form.save()
            return JsonResponse({
                'id': cliente.id,
                'message': 'Cliente creado exitosamente'
            }, status=201)
        return JsonResponse({'errors': form.errors}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)

# Editar un cliente existente
# Editar un cliente existente
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from decimal import Decimal # Importar Decimal
from datetime import date # Importar date

from .models import Cliente
from .forms import ClienteForm # Asegúrate de que ClienteForm esté importado

# Editar un cliente existente
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def editar_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
        data = json.loads(request.body)
        
        # 1. Recuperamos los datos actuales del cliente.
        #    Usamos un diccionario para poder manipular los valores.
        
        # ⚠️ Definimos los campos que SÍ pueden ser actualizados por el formulario
        updateable_fields = [
            'nombre_completo', 'tipo_cliente', 'dni', 'ruc', 'telefono_contacto', 
            'email', 'direccion', 'institucion_educativa', 'detalles_adicionales', 
            # Los campos 'pedidos', 'total_gastado', 'ultima_fecha_pedido'
            # suelen ser actualizados por lógica interna, pero los incluimos
            # por si se permite la edición manual.
            'pedidos', 'total_gastado', 'ultima_fecha_pedido'
        ]

        final_data = {}
        
        # 2. Cargar los datos existentes para simular un cuerpo de solicitud completo (PATCH/PUT).
        for field in updateable_fields:
             value = getattr(cliente, field)
             
             if value is None:
                 # Campos nulos (null=True) deben pasarse como '' para CharFields/Text
                 # en el form si no queremos que falle la validación.
                 final_data[field] = ''
             elif isinstance(value, Decimal):
                 # Convertir Decimal a float para que se pase correctamente en la data JSON
                 final_data[field] = float(value)
             elif isinstance(value, date):
                 # Convertir fecha a string ISO para el form
                 final_data[field] = value.isoformat()
             else:
                 final_data[field] = value
        
        # 3. Sobrescribimos los datos actuales SÓLO con lo que vino en el body (data).
        final_data.update(data)
        
        # 4. Pasamos todos los datos (actuales + nuevos) al formulario.
        #    Esto asegura que todos los campos requeridos por el modelo (nombre_completo,
        #    tipo_cliente, DNI/RUC condicionales) estén presentes en la validación.
        form = ClienteForm(final_data, instance=cliente)
        
        if form.is_valid():
            cliente = form.save()
            return JsonResponse({
                'id': cliente.id,
                'message': 'Cliente actualizado exitosamente'
            })
        
        # Si la validación falla, devuelve los errores
        return JsonResponse({'errors': form.errors}, status=400)
        
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)
    except Exception as e:
        # Captura cualquier otro error, útil para depuración
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
# Eliminar un cliente
@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
        cliente.delete()
        return JsonResponse({'message': 'Cliente eliminado exitosamente'}, status=200)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
