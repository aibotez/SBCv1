from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import socket,os


def sharewifi():
    ssid=input('输入热点名 ')
    keypass=input('输入热点密码 ')
    #os.system('copy a b')
    #os.remove(a)
    try:
        os.remove('share_ls.bat')
    except:
        pass
    try:
        os.system('copy sharewifi.bat share_ls.bat')
    except:
        pass
    
    jlwk='netsh wlan set hostednetwork mod=allow ssid='+ssid+' key='+keypass+'\n'
    startwifi='netsh wlan start hostednetwork'+'\n'
    with open('share_ls.bat','a') as f:
        f.write(jlwk+startwifi)
    os.system('share_ls.bat')
sfwx=input('是否开启热点(y开启，其他键不开启，只有电脑有无线网卡才可用)可以将电脑作为路由器使用，\n连接该网络下的电脑都可以\
互相传输文件；')
if sfwx == 'y':
    sharewifi()

myname = socket.gethostname()
#获取本机ip
myaddr = socket.gethostbyname(myname)
web_ip=myaddr+':9500'
print('浏览器中输入此地址:  ',web_ip)
sfzy=input('是否开启账户模式(y开启，其他键不开启) ')
if sfzy == 'y':
    users = 'zz'
else:
    users='zy'
#users = 'zz'
user_fie='user/user.txt'
fie_down='file_d/'
file_js='file_d/jians.txt'
user_name=''
file_name={}
file_gl='~'
@csrf_exempt  # 让该页面不校验csrf_token
def upload(request):
    if request.method == "POST":
        file_obj = request.FILES.get("filename")
        with open(file_obj.name, "wb") as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
            return HttpResponse("file upload success!")
    return render(request, "upload.html")




from django.http import StreamingHttpResponse
def big_file_download(request):
  # do something...
  def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
      while True:
        c = f.read(chunk_size)
        if c:
          yield c
        else:
          break

  the_file_name = "f://big.txt"
  response = StreamingHttpResponse(file_iterator(the_file_name))
  response['Content-Type'] = 'application/octet-stream'
  response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
  return response




from django.shortcuts import render


def ct(request):
    name='bb'
    file_url='file_d/'
    file_name={}
    file_all=[]
    with open(file_url+'jians.txt','r') as f:
        fe=f.read()
    fe=fe.split('\n')
    del fe[-1]
    for i in fe:
        if name == i.split(' ')[3]:
            file_all.append({"id":int(i.split(' ')[0]),"title":i.split(' ')[1]+'::'+i.split(' ')[2]})
            file_name['id']=int(i.split(' ')[0])
            file_name['name']=i.split(' ')[2]

    return render(request,"1.html",locals())
def c(request,id):
    print(request,id)
    return HttpResponse("file upload success!")



def check_user():
    with open(user_fie, 'r') as f:
        res=f.read()
    res=res.split('\n')
    return res
def zhuce(user_name,user_password):
    #text=request.GET
    #print(text)
    #user_name=text['firstname']
    #user_password=text['lastname']
    user_info=check_user()
    user_name_all=[]
    zc_re=''
    for i in user_info:
        user_name_all.append(i.split(' ')[0])
    print(user_name_all,user_name)
    if user_name in user_name_all:
        zc_re='0'
        #return HttpResponse("no succ!")
    else:
        with open(user_fie,'a') as f:
            f.write(user_name+' '+user_password+'\n')
        zc_re='1'
        #return HttpResponse("zc succ!")
    return zc_re

def home(request):
    #check_user()
    if users == 'zy':
        return HttpResponseRedirect('/fehome/')
    else:

        return render(request, "dlzc.html")
def dengl(user_name,user_password):
    #text=request.GET
   # user_name=text['firstname']
   # user_password=text['lastname']
    pass_user='0'

    if users == 'zy':
        pass_user='1'
    else:
        if len(user_name) > 1 and len(user_password) ==0 :
            if user_name in check_user():
                pass_user = '1'
            else:
                with open(user_name,'a') as f:
                    f.write(str(user_name)+'\n')
        elif len(user_name) == 1 and len(user_password) ==0 :
            pass_user = '无效用户名'
        elif len(user_name) > 0 and len(user_password) > 0 :
            if user_name+' '+user_password in check_user():
                pass_user = '1'
            else:
                pass_user = '0'
        #print(f,s)
        #return render(request, "dlzc.html")
    return pass_user
def dlzc(request):
    global user_name
    if users != 'zy':
        text = request.GET
        user_name = text['name']
        user_password = text['password']
        if 'dengl' in text:
            passuser=dengl(user_name,user_password)
            if passuser == '0':
                return HttpResponse("dl no succ!")
            else:
                return HttpResponseRedirect('/fehome/')
                #return render(request, "fehome.html")
                #return HttpResponse("dl succ!")
        elif 'zhuce' in text:
            zc_re=zhuce(user_name,user_password)
            if zc_re == '0':
                return HttpResponse("zc no succ!")
            else:
                return HttpResponseRedirect('/fehome/')
                #return render(request, "fehome.html")
                #return HttpResponse("zc succ!")
    elif users == 'zy':
        return HttpResponseRedirect('/fehome/')
        #return render(request, "fehome.html")
    #return HttpResponseRedirect('/')


def fehome(request):
    global file_name
    file_url='file_d/'
    file_name={'id':[],'name':[]}
    file_all=[]
    with open(file_url+'jians.txt','r') as f:
        fe=f.read()
    fe=fe.split('\n')
    del fe[-1]
    if users != 'zy':
        for i in fe:
            if  user_name== i.split(file_gl)[3]:
                file_all.append({"id":int(i.split(file_gl)[0]),"title":i.split(file_gl)[1]+'::'+i.split(file_gl)[2]})
                file_name['id'].append(int(i.split(file_gl)[0]))
                file_name['name'].append(i.split(file_gl)[2])
    else:
        for i in fe:
            file_all.append({"id": int(i.split(file_gl)[0]), "title": i.split(file_gl)[1] + '::' + i.split(file_gl)[2]})
            file_name['id'].append(int(i.split(file_gl)[0]))
            file_name['name'].append(i.split(file_gl)[2])
    return render(request,"fehome.html",locals())

def shangc(request):
    global user_name
    if request.method == "POST":
        tow=request.POST['towho']
        if tow == '传输给谁':
            tow=user_name
        if tow == '':
            return HttpResponse("上传名单不能为空")
        file_obj = request.FILES.get("filename")
        if file_obj == None:
            return HttpResponse("上传文件不能为空")
        print(file_obj)
        with open(fie_down+file_obj.name, "wb") as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        with open(file_js,'r') as f:
            fe=f.read()
        fe=fe.split('\n')     #获取目前最大id
        fe=fe[-2]
        fe=fe.split(file_gl)
        idd=int(fe[0])
        if users =='zy':
            user_name='N'
            tow='N'
        fe_w=str(idd+1)+file_gl+user_name+'>'+tow+'~'+file_obj.name+'~'+tow+'\n'
        with open(file_js,"a") as f:
            f.write(fe_w)
            return HttpResponse("file upload success!")
        #return HttpResponse(str(request))
    return HttpResponseRedirect('/fehome/')

def xiaz(request,id):
    print(request,id,file_name)
    print('aaa',type(id),file_name['id'],type(file_name['id']))
    id=int(id)
    if id in file_name['id']:
        idx=file_name['id'].index(id)
        filename_ls=file_name['name'][idx]
        print(file_name['name'][idx])

    # do something...
    def file_iterator(file_name, chunk_size=512):
        #file_name=file_name.split('/')[-1]
        #print('fe',file_name)
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    # the_file_name = "file_d/big.txt"
    # the_file_name = "file_d/123.jpg"
    the_file_name = fie_down+filename_ls
    #print(the_file_name)
    the_file_name1 = the_file_name.split('/')[-1]
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    #response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    response['Content-Disposition'] ="attachment; filename*=utf-8''{}".format(the_file_name1)
    return response
    return HttpResponse("file upload success!")


fe_ntjt='ntjt/ntjt.txt'
def ntqq(request):
    text = request.GET
    a_user=text['a_user']
    b_user=text['b_user']
    totext=text['totext']
    head = a_user + '>' + b_user
    print('head',head)
    scs=[]
    cstxt=[]
    with open(fe_ntjt,'r') as f:
        txt=f.read()
    if len(txt) >0:
        txt=txt.split('\n')
        del txt[-1]
        for i in txt:
            scs.append(i.split('^')[0])
            cstxt.append(i.split('^')[1])
        if head in scs:
            if cstxt[scs.index(head)] != totext:
                cstxt[scs.index(head)] =totext
                with open(fe_ntjt,'w') as f:
                    for tet in range(len(scs)):
                        f.write(scs[tet]+'^'+cstxt[tet]+'\n')
        else:
            with open(fe_ntjt,'a') as f:
                f.write(head + '^' + totext + '\n')
    else:
        with open(fe_ntjt, 'a') as f:
            f.write(head + '^' + totext + '\n')
    #http://192.168.3.5:9000/ntjt/?a_user=hh&b_user=bb&totext=hhabb
    return HttpResponse("file upload success!")

def ntjt(request):
    text = request.GET
    b_user=text['a_user']
    text=''
    with open(fe_ntjt,'r') as f:
        txt=f.read()
    if len(txt) >0:
        txt=txt.split('\n')
        del txt[-1]
        for i in txt:
            te=i.split('^')[0]
            te=te.split('>')[1]
            if te==b_user:
                text = i.split('^')[1]
    return HttpResponse(text)
