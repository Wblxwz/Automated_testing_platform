from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import logout
from django.http import HttpResponse
import logging
import json
from .models import *

# Create your views here.

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    filename="app.log")
logger = logging.getLogger(__name__)

def log_out(request):
    code = 5003
    user = request.user
    message = f'{user}登出失败'
    if request.user.is_authenticated: 
        logout(request)
        code = 2003
        message = f'{user}登出成功'
    data = {
        'code':code,
        'message':message
    }
    return_data = json.dumps(data)
    logging.info(return_data)
    return redirect('/users/signin')

def project_count(request):
    count = Project.objects.filter(username=request.user.username).count()
    data = {
        'count': count
    }
    json_data = json.dumps(data)
    return HttpResponse(json_data)

class StressHomeView(View):
    def get(self,request):
        curr_user = request.user
        if request.GET:
            page = int(request.GET['page'])
            limit = int(request.GET['limit'])
            start = (page - 1) * limit
            end = page * limit
            projects = Project.objects.filter(username=curr_user.username).order_by('-create_time')[start:end]
            count = Project.objects.filter(username=request.user.username).count()
            projects_list = []
            for project in projects:
                projects_list.append(
                    {
                        'id':project.id,
                        'username':project.username,
                        'project_name':project.project_name,
                        'create_time':project.create_time.strftime('%Y/%m/%d %H:%M:%S')
                    }
                )
            data = {
                'code': 0,
                'data': projects_list,
                'count':count
            }
            logger.info(f'curr_user.username 查询Projects {request.GET},{projects}')
            json_data = json.dumps(data)
            return HttpResponse(json_data)
        logger.info(f'{curr_user.username} in home')
        project_count = Project.objects.filter(username=curr_user.username).count()
        context = {
            'project_count':project_count
        }
        return render(request,"stress/home.html",context)
    def post(slef,request):
        curr_user = request.user
        data = json.loads(request.body)
        code = 2003
        message = '创建项目成功'
        try:
            if Project.objects.filter(project_name=data['project_name'],username=curr_user.username).exists():
                code = 5003
                message = '创建项目失败，已有该项目'
                logger.warning(f'{curr_user.username} 创建项目 {data['project_name']} 失败')
            else:
                Project.objects.create(username=curr_user.username,project_name=data['project_name'])
        except Exception as e:
            logger.error(e)
            code = 5003
            message = f'创建项目失败,{e}'
        return_data = {
            'code':code,
            'message':message
        }
        json_data = json.dumps(return_data)
        logger.info(f'{curr_user.username} 创建新项目 {data['project_name']}')
        return HttpResponse(json_data)
    
class StressView(View):
    def get(self,request):
        return render(request,"stress/stress.html")