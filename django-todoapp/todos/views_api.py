import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from todos.models import Todo


@csrf_exempt
@login_required
@require_http_methods(['PATCH'])
def update(request, id):
    # Get the params from the payload.
    data = json.loads(request.body.decode('utf-8'))

    print('Received update API request for todo id: ', id)
    print('Completed: ', data['completed'])

    # Update the model
    todo = Todo.objects.get(pk=id)
    todo.completed = data['completed']
    todo.save()

    print('Todo item updated')

    return JsonResponse({})

@csrf_exempt
@login_required
@require_http_methods(['DELETE'])
def remove(request, id):
    
    print('Received remove update API request for todo id: ', id)

    todo = Todo.objects.get(pk = id)
    todo.delete()

    return JsonResponse({})