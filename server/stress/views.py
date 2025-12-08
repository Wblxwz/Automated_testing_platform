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

class StressHomeView(View):
    def get(self,request):
        curr_user = request.user
        logger.info(f'{curr_user.username} in home')
        project_count = Project.objects.filter(username=curr_user.username).count()
        context = {
            'project_count':project_count
        }
        return render(request,"stress/home.html",context)
    
class StressView(View):
    def get(self,request):
        return render(request,"stress/stress.html")