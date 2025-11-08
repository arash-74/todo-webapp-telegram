import json
import time
import math

from django.core.cache import cache
from django.core.serializers import serialize
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string

from todo.models import Todo, User


# Create your views here.
def Index(request,chat_id):
    if not chat_id:
        return Http404('bad request')
    if not User.objects.filter(chat_id=chat_id).exists():
        User.objects.create(chat_id = chat_id)
    if request.headers.get('Accept') == 'text/event-stream':
        response = loader(chat_id)
        return response

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        todos_list = cache.get(f'todos-{chat_id}')
        data = render_to_string('html/todos_list.html', context={'todos': todos_list})
        return HttpResponse(data)
    return render(request, 'html/index.html', {})

# def prepare_user(reqeust):
#     print(reqeust.POST)
#     return JsonResponse({})
def loader(chat_id):
    todos_filter = Todo.objects.filter(user__chat_id=chat_id).order_by('-created_at').values('id', 'title',
                                                                                             'is_completed')
    todo_count = todos_filter.count()
    chunking_limit = math.ceil(todo_count / 100 * 10)

    def chunking_data():
        todos_list = []
        start = 0
        end = chunking_limit
        for i in range(1, 11):
            todos_list = [*todos_list, *list(todos_filter[start:end])]
            start = end
            end += chunking_limit
            if i != 10:
                yield f'data: {json.dumps({'number': i})}\n\n'
            if i == 10:
                cache.set(f'todos-{chat_id}', todos_list)
                yield f'data: {json.dumps({'number': i})}\n\n'
            time.sleep(0.1)

    response = StreamingHttpResponse(chunking_data(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response


def remove_todo(request, id):
    try:
        Todo.objects.get(id=id).delete()
    except Todo.DoesNotExist:
        return JsonResponse({'status': 'error', 'msg': 'todo cannot delete'}, status=404)
    return JsonResponse({'status': 'ok'})


def complete_todo(request, id):
    try:
        Todo.objects.filter(id=id).update(is_completed=True)
    except Todo.DoesNotExist:
        return JsonResponse({'status': 'error', 'msg': 'todo cannot complete'}, status=404)
    return JsonResponse({'status': 'ok'})


def add_todo(request, chat_id):
    todo_title = request.POST.get('todo-title')
    print(type(chat_id))
    try:
        user = User.objects.get(chat_id=chat_id)
        todo = Todo.objects.create(user=user, title=todo_title)
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': 'todo cannot add'}, status=404)
    return JsonResponse({'status': 'ok', 'id': todo.id})
