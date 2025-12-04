from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model,authenticate,login
from django.views import View
import json
import logging

User = get_user_model()
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    filename="app.log")
logger = logging.getLogger(__name__)

class SignUpView(View):
    def get(self,request):
        return render(request,"users/sign_up.html")
    def post(self,request):
        data = json.loads(request.body)
        logger.info(msg=f'sign up dict:{data}')
        code = 2001
        message = '用户注册成功'
        try:
            if User.objects.filter(username=data['nickname']).exists() == False:
                User.objects.create_user(username=data['nickname'],password=data['password'],email=data['email'])
            else:
                code = 5001
                message = '用户注册失败,用户已存在'
        except Exception as e:
            code = 5001
            message = f'用户注册失败,{e}'
            logger.error(e)
        response_data = {
            'code':code,
            'message':message
        }
        response_data_json = json.dumps(response_data)
        return HttpResponse(response_data_json)

class SignInView(View):
    def get(self,request):
        return render(request,"users/sign_in.html")
    def post(self,request):
        data = json.loads(request.body)
        get_username = data['username']
        get_password = data['password']
        code = 2002
        message = '登录成功'
        try:
            if User.objects.filter(username=get_username).exists():
                user = User.objects.get(username=get_username)
                auth_user = authenticate(request=request,username=user.username,password=get_password)
                logger.info(f"user_info:{user}")
                logger.info(f"auth_user_info:{auth_user}")
                if auth_user is None:
                    code = 5002
                    message = "登陆失败,用户密码错误"
                else:
                    login(request,auth_user)
            else:
                code = 5002
                message = "登陆失败,用户不存在"
        except Exception as e:
            logger.error(e)
            code = 5002
            message = f"登陆失败,{e}"
        response = {
            'code':code,
            'message':message
        }
        json_response = json.dumps(response)
        return HttpResponse(json_response)

class StressView(View):
    def get(self,request):
        return render(request,'stress/stress.html')