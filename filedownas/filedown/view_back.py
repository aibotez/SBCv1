from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from urllib import parse
import shutil,json
import socket,os



user_info='user_info.txt'
wenj_all={}
files=[]
file_l=[]
wenj_all['name']=[]
wenj_all['luj']=[]
wenj_all['pf']=[]
# disk=(os.popen('fsutil fsinfo drives').read()).split()[1:]
# lujing=[]
# for i in disk:
#     try:
#         lujing=os.listdir(i+'cc')
#         for j in lujing:
#             print(j)
#             wenj_all['name'].append(j)
#             wenj_all['luj'].append(i+'cc'+'\\'+j)
#             wenj_all['pf'].append(i)
#     except Exception as e:
#         print('NULL',e)



wenj_all_zl=wenj_all
print(wenj_all)

user={'ss':[],'cs':[]}
resous=''
ss=0
dl_cishu=0
dl_cs_max=3
page=0

files=[]
curt_lj=''




def shouye(request):
    global user
    userinfo=check_user()
    user_agent= userinfo['user_agent']
    agent = request.META['HTTP_USER_AGENT']
    if agent in user_agent:
        ss = userinfo['user_id'][user_agent.index(agent)]
        if ss in user['ss']:
            idx = user['ss'].index(ss)
            user['cs'][idx] = user['cs'][idx] + 1
        else:
            user['ss'].append(ss)
            user['cs'].append(1)
        return HttpResponseRedirect('/start/')
    else:
        return render(request, "dlzc.html")



def check_user():
    global user_info
    with open(user_info, 'r') as f:
        res=f.read()
    if len(res)>0:
        res=res.split('\n')
        del res[-1]
    user_id=[]
    user_name=[]
    user_password=[]
    user_agent=[]
    user_name_pass=[]
    for i in res:
        user_id.append(i.split('#')[0])
        user_name.append(i.split('#')[1])
        user_password.append(i.split('#')[2])
        user_agent.append(i.split('#')[3])
        user_name_pass.append(i.split('#')[1]+'#'+i.split('#')[2])
    userinfo={'user_id':user_id,'user_name':user_name,'user_pass':user_password,'user_agent':user_agent,'user_name_pass':user_name_pass}
    return userinfo

def dengl(user_name, user_password):
    pass_user='0'
    if len(user_name) > 1 and len(user_password) == 0:
        pass_user = '0'
    elif len(user_name) == 1 and len(user_password) == 0:
        pass_user = '无效用户名'
    elif len(user_name) > 0 and len(user_password) > 0:
        if user_name + '#' + user_password in check_user()['user_name_pass']:
            pass_user = '1'
        else:
            pass_user = '0'
    # print(f,s)
    # return render(request, "dlzc.html")
    return pass_user
def zhuce(user_name, user_password,agent):
    zc_re='0'
    user_all = check_user()
    if len(user_name) > 1 and len(user_password) == 0:
        zc_re='0'
    elif len(user_name) == 1 and len(user_password) == 0:
        zc_re='0'
    elif len(user_name) > 0 and len(user_password) > 0 and agent not in user_all['user_agent']:
        user_name_all=user_all['user_name']
        user_id=user_all['user_id'][-1]
        new_user_id=int(user_id)+1
        zc_re=''
        for i in user_info:
            user_name_all.append(i.split(' ')[0])
        print(user_name_all,user_name)
        if user_name in user_name_all:
            zc_re='0'
            #return HttpResponse("no succ!")
        else:
            with open(user_info,'a') as f:
                f.write(str(new_user_id)+'#'+user_name+'#'+user_password+'#'+agent+'\n')
            zc_re='1'

    return zc_re



def dlzc(request):
    agent = request.META['HTTP_USER_AGENT']
    text = request.GET
    user_name = text['name']
    user_password = text['password']
    if 'dengl' in text:
        passuser = dengl(user_name, user_password)
        if passuser == '0':
            return HttpResponse("dl no succ!")
        else:
            return HttpResponseRedirect('/start/')
            # return render(request, "fehome.html")
            # return HttpResponse("dl succ!")
    elif 'zhuce' in text:
        zc_re = zhuce(user_name, user_password,agent)
        if zc_re == '0':
            return HttpResponse("zc no succ!")
        else:
            userinfo = check_user()
            ss = userinfo['user_id'][-1]
            user['ss'].append(ss)
            user['cs'].append(1)

            return HttpResponseRedirect('/start/')



def ho(request):
    global user_agent
    global ss
    global  page
    global files
    global resous
    global dl_cishu
    global user
    global wenj_all

    disk = (os.popen('fsutil fsinfo drives').read()).split()[1:]
    lujing = []
    wenj_all={}
    files=[]
    wenj_all['name'] = []
    wenj_all['luj'] = []
    wenj_all['pf'] = []
    for i in disk:
        try:
            lujing = os.listdir(i + 'cc')

            for j in lujing:

                wenj_all['name'].append(j)
                wenj_all['luj'].append(i + 'cc' + '\\' + j)
                wenj_all['pf'].append(i)
        except Exception as e:
            print('NULL', e)

    resous = 'yes'
    userinfo=check_user()
    user_agent= userinfo['user_agent']
    agent = request.META['HTTP_USER_AGENT']
    ss = userinfo['user_id'][user_agent.index(agent)]

    page =0

    idx = user['ss'].index(ss)
    dl_cishu=user['cs'][idx]
    file_l=[]
    return HttpResponseRedirect('/s')


def ct(request):
    global ss
    global files
    global file_l
    global resous
    global curt_lj

    if resous == 'no':
        resous = 'no'
        return HttpResponseRedirect('/start/')
    else:
        if page ==0:
            file_l=[]
            for i in wenj_all['name']:
                file = {}
                file['id']=str(ss) + '.'+str(dl_cishu)+'.' + str(page) + '.'+str(wenj_all['name'].index(i))
                file['name']=i
                file['luj']=wenj_all['luj'][wenj_all['name'].index(i)]
                ljj = file['luj'].split('\\')
                ljj1=''
                del ljj[-1]
                for s in ljj:
                    if s != ljj[-1]:
                        ljj1=ljj1+s+'/'
                    else:
                        ljj1 = ljj1 + s
                file['curt_lj']=ljj1
                try:
                    file['pf']=wenj_all['pf'][wenj_all['name'].index(i)]
                except:
                    pass
                files.append(file)
                file_l.append(file)
        files1=[]
        for i in files:
            if i not in files1:
                files1.append(i)
        files=[]
        files=files1
        file_all=file_l
        bkbl=file_l[0]['id']
        zh = 'aibo'
        lj=file_l[0]['curt_lj']
        resous = 'no'
        #cook_bl={'zh':json.dumps(['vf','ab'])}
        return render(request,"1.html",locals())



def xiaz(request,id):
    delafter_page(id, 'aft')
    value = request.COOKIES["cur_id"]
    print('cccccccccccccc',value)
    print('aaaaaa',request,request.GET)
    global page
    global files
    global file_l
    global resous
    global curt_lj
    id_info=id.split('.')
    curt_page=id_info[2]
    curt_use=id_info[0]
    curt_cs=id_info[1]
    resous = 'yes'
    file_l=[]
    felj=''
    for i in files:
        if id in i['id']:
            fename=i['name']
            felj=i['luj']
    curt_lj=felj
    if os.path.isdir(felj):
        page=int(curt_page)+1
        try:
            lujing = os.listdir(felj)
            if len(lujing)<1:
                lujing=['无文件夹']
            for j in lujing:
                file = {}
                file['id'] = curt_use + '.'+curt_cs+'.' + str(page) + '.' + str(lujing.index(j))
                file['name'] = j
                file['luj'] = felj+'\\'+j
                file['curt_lj']=felj
                files.append(file)
                file_l.append(file)
            file_all = files
        except:
            pass
        return HttpResponseRedirect('/s')
    else:
        resous = 'no'
        return HttpResponse(felj+'....'+id)

def delafter_page(id,aft_or_per):
    id_info=id.split('.')
    curt_page=id_info[2]
    curt_use=id_info[0]
    curt_cs=id_info[1]
    id_pag=int(curt_page)
    id_curt = curt_use + '.' + curt_cs + '.' + str(id_pag)
    if aft_or_per == 'aft':
        del_pag=id_pag+1
    elif aft_or_per == 'per':
        del_pag = id_pag - 1
    id_cut=curt_use+'.'+curt_cs+'.'+str(del_pag)

    for i in files:
        ids=i['id']
        ids_info = ids.split('.')
        cho_page = ids_info[2]
        cho_use = ids_info[0]
        cho_cs = ids_info[1]
        if id_cut == cho_use+'.'+cho_cs+'.'+cho_page:
            files.remove(i)


def per_page(request):
    global file_l
    global resous
    resous = 'yes'
    text = request.GET
    #print(text.keys())
    id=list(text.keys())[0]
    id_info=id.split('.')
    curt_page=id_info[2]
    curt_use=id_info[0]
    curt_cs=id_info[1]
    id_pag=int(curt_page)
    if id_pag ==0:
        return HttpResponseRedirect('/start/')
    id_curt = curt_use + '.' + curt_cs + '.' + str(id_pag)
    pre_pag=id_pag-1
    id_new=curt_use+'.'+curt_cs+'.'+str(pre_pag)
    file_l=[]
    for i in files:
        ids=i['id']
        ids_info = ids.split('.')
        cho_page = ids_info[2]
        cho_use = ids_info[0]
        cho_cs = ids_info[1]
        if id_new == cho_use+'.'+cho_cs+'.'+cho_page:
            file_l.append(i)


    for i in files:
        ids=i['id']
        ids_info = ids.split('.')
        cho_page = ids_info[2]
        cho_use = ids_info[0]
        cho_cs = ids_info[1]
        if id_curt == cho_use+'.'+cho_cs+'.'+cho_page:
            files.remove(i)
    return HttpResponseRedirect('/s')







import zipfile
def zip_ya(start_dir):
    start_dir = start_dir  # 要压缩的文件夹路径
    file_news = start_dir + '.zip'  # 压缩后文件夹的名字

    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        f_path = dir_path.replace(start_dir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        f_path = f_path and f_path + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), f_path + filename)
    z.close()
    return file_news

print('bbbbbbbbb',parse.quote('下载'))
import datetime
def wenjcl(request):




    res=request.GET

    print('resresres',res)
    rezd = list(res.keys())
    idx_newname=rezd.index('newname')
    if idx_newname ==0:
        idx_id=idx_newname+1
    else:
        idx_id = idx_newname - 1
    wjid=rezd[idx_id]
    xzorsh=res[wjid]
    cz=res[wjid]
    print(wjid,cz)
    wjname=''
    wjlj=''
    if xzorsh == 'sharedown':
        fxmy=[]
        fxfelj=[]
        fxfename=[]
        cz='下载'
        with open('sharefe.txt','r') as f:
            fxinfo=f.read()
        fxinfo=fxinfo.split('\n')
        del fxinfo[-1]
        for i in fxinfo:
            fxmy.append(i.split('~')[0])
            fxfelj.append(i.split('~')[1])
            fxfename.append(i.split('~')[-1])
        idx=fxmy.index(wjid)
        wjlj=fxfelj[idx]
        wjname=fxfename[idx]
        pass
    else:
        for i in files:
            if wjid == i['id']:
                wjlj=i['luj']
                wjname=i['name']

    wjlj=wjlj.replace('\\','/')
#http://127.0.0.1:9500/wenjcl/?20191020230908=sharedown    下载请求  url 编码  parse.quote(s)
    if cz =='下载':
        if os.path.isdir(wjlj):
            zip_ya(wjlj)
            wjlj=wjlj+'.zip'
            wjname=wjname+'.zip'
        def file_iterator(file_name, chunk_size=512):
            with open(file_name,'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        the_file_name = wjlj
        response = StreamingHttpResponse(file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(wjname)
        return response
    elif cz == '分享':
        now=datetime.datetime.now()
        wjmy=now.strftime("%Y-%m-%d-%H-%M-%S")
        url='http://127.0.0.1:9500/wenjcl/?'+wjmy+'='+'sharedown'
        with open('sharefe.txt','a') as f:
            f.write(wjmy+'~'+wjlj+'~'+wjname+'\n')
        return HttpResponse('分享链接为：'+url)

    elif cz == '重命名':
        oldlj=wjlj
        newname=res['newname']
        oldlj_d=oldlj.split('/')
        del oldlj_d[-1]
        newlj=''
        for i in oldlj_d:
            newlj=newlj+i+'/'
        newlj=newlj+newname
        zt='succes'

        try:
            os.rename(oldlj,newlj)
        except Exception as e:
            zt=e
            pass
        # #os.rename(src,new)
        return HttpResponse(zt)
    elif cz == '删除':
        zt='succes'
        try:
            if os.path.isdir(wjlj):

                shutil.rmtree(wjlj)
            else:
                os.remove(wjlj)
        except Exception as e:
            zt=e
        return HttpResponse(zt)
    pass

def netcz(request):
    if request.method == "POST":
        res = request.POST
        curlj=res['cur_lj']
        file_obj = request.FILES.get("filename")
        rezd = list(res.keys())
        if 'newfile' in rezd:
            newfilename=res['newfile']
            if os.path.exists(curlj+'/'+newfilename):
                now = datetime.datetime.now()
                wjmy = now.strftime("%Y-%m-%d-%H-%M-%S")
                os.makedirs(curlj+'/'+wjmy)
                return HttpResponse('已存在该文件夹，新建的文件夹为：'+wjmy)
            else:
                os.makedirs(curlj+'/'+newfilename)

                return HttpResponse('新建文件夹成功')

        elif file_obj != None:

            with open(curlj + '/'+file_obj.name, "wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            return HttpResponse("file upload success!")
        elif file_obj == None and 'newfile' not in rezd:
            return HttpResponse("未操作")











def my_image(request):
    d = os.path.dirname(__file__)
    #parent_path = path.dirname(d)
    print("d="+str(d))
    imagepath = os.path.join(d,"E:/微信图片_20200114094722.jpg")
    print("imagepath="+str(imagepath))
    image_data = open(imagepath,"rb").read()
    return HttpResponse(image_data,content_type="image/png") #注意旧版的资料使用mimetype,现在已经改为content_type