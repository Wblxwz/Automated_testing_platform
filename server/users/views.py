from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import json
import logging

User = get_user_model()
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    filename="app.log")
logger = logging.getLogger(__name__)

def sign_up(request):
    if request.method == 'GET':
        return render(request,"users/sign_up.html")
    elif request.method == 'POST':
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

def sign_in(request):
    return render(request,"users/sign_in.html")
