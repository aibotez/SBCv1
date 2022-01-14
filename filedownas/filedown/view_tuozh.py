from django.http import HttpResponse,JsonResponse
import os,datetime
from django.shortcuts import render




def get_user_ip_home(request):
    return render(request, "html_404_get_ip.html")
def get_ip(request):
    user_ip_txt = 'user_ip.txt'
    user_ip = request.GET['ip']
    ip_info = request.GET['info']
    ip_info = ip_info.replace('"','')
    # print(ip_info,type(ip_info))
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(user_ip_txt,'a') as f:
        f.write(now_time+'\t'+user_ip+'\t'+ip_info+'\n')
    return HttpResponse('')


def get_user_ip(request):
    user_ip = 'user_ip.txt'
    user_request_info = request.META
    #print(user_request_info)
    if 'HTTP_X_FORWARDED_FOR' in user_request_info.keys():
        user_real_ip = user_request_info['HTTP_X_FORWARDED_FOR']
    else:
        user_real_ip = user_request_info['REMOTE_ADDR']
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(user_ip,'a') as f:
        f.write(now_time+'\t'+user_real_ip+'\n')

