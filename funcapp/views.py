from celery.result import AsyncResult

from django.contrib.auth import login
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http.response import JsonResponse
from django.shortcuts import redirect, render

from .forms import SignupForm
from .models import Funktion


def sign_up(request):
    context = {}
    form = SignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            content_type = ContentType.objects.get_for_model(Funktion)
            permissions = Permission.objects.filter(content_type=content_type)
            for item in permissions:
                user.user_permissions.add(item)
            login(request, user)
            return redirect('index')
    context['form'] = form
    return render(request, 'signup.html', context)


def index(request):
    return render(request, 'index.html')


def get_status(request, task_id):
    if task_id == 'None':
        return JsonResponse('No tasks', status=200)
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    print(result)
    print(task_result.status)
    if task_result.status in ('SUCCESS', 'FAILURE'):
        request.session['task_id'] = 'None'
    return JsonResponse(result, status=200)
