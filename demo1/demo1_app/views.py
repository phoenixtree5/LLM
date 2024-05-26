import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import shutil
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse,FileResponse
from django.contrib.auth.decorators import login_required
from .models import Resource
import logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def index(request):
    if request.method == 'GET':
        return render(request, 'services.html')

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return JsonResponse({'success': False, 'message': '必须提供用户名和密码'})
        
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({'success': False, 'message': '用户不存在或者密码错误'}) 
        else:
            login(request, user)
            return JsonResponse({'success': True, 'message': '登陆成功'})

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')

def user_register(request):
    if request.method == 'GET':
         return render(request, 'register.html')
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            rpassword = request.POST.get('rpassword')
            
            if not username or not password:
                return JsonResponse({'success': False, 'message': '必须提供用户名和密码'})
            if not rpassword:
                return JsonResponse({'success': False, 'message': '必须确认密码'})
            if password != rpassword:
                return JsonResponse({'success': False, 'message': '密码不一致'})
            
            User.objects.create_user(username=username, password=password)

            return JsonResponse({'success': True, 'message': '注册成功，3秒后自动跳转'})
        
# 设置上传路径
UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'resources/')


# 设置日志
logging.basicConfig(level=logging.INFO)

# 使用csrf_exempt装饰器以允许不需要CSRF保护的请求（如果需要，谨慎使用）
@csrf_exempt
def upload_resource(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        file = request.FILES.get('file')

        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
            logging.info(f"Created upload directory at {UPLOAD_DIR}")

        file_path = os.path.join(UPLOAD_DIR, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            logging.info(f"File saved to {file_path}")

        Resource.objects.create(name=name, path=file.name)
        return JsonResponse({'success': True, 'message': 'Resource uploaded successfully'})
    return render(request, 'services.html')

def search_resources(request):
    query = request.GET.get('q', '')
    if query:
        results = Resource.objects.filter(name__icontains=query)
    else:
        results = Resource.objects.all()
    return render(request, 'services.html', {'results': results, 'query': query})

def download_resource(request, resource_id):
    resource = Resource.objects.get(id=resource_id)
    file_path = os.path.join(UPLOAD_DIR,resource.path)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response