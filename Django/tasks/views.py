
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Tarea

def add_task(request, nombre, descripcion):
    tarea = Tarea(nombre=nombre, descripcion=descripcion)
    tarea.save()
    return HttpResponse(f"Tarea '{tarea.nombre}' añadida.")

def list_tasks(request):
    tareas = Tarea.objects.all()
    respuesta = "<h1>Lista de Tareas</h1>"
    for tarea in tareas:
        respuesta += f"<p>ID: {tarea.id} | {tarea.nombre} - {tarea.descripcion}</p>"
    return HttpResponse(respuesta)

def delete_task(request, id_task):
    tarea = get_object_or_404(Tarea, id=id_task)
    tarea.delete()
    return HttpResponse(f"Tarea con ID {id_task} eliminada.")
