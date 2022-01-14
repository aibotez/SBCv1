from django.shortcuts import render
import json,threading
from django.http import HttpResponse
from pack.b_t_s import BaiDuPan
from bypy import ByPy
import threading,time,os
# 获取一个bypy对象，封装了所有百度云文件操作的方法

path=os.getcwd().replace('\\','/')
path=path+'/user/user.txt'
user_info=path
moren_loca_lj = '百度云分享链接下载'
fgf = '：'
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
    user_zgye=[]
    user_yyye=[]
    for i in res:
        user_id.append(i.split('#')[0])
        user_name.append(i.split('#')[1])
        user_password.append(i.split('#')[2])
        user_zgye.append(i.split('#')[3])
        user_yyye.append(i.split('#')[4])
        user_name_pass.append(i.split('#')[1]+'#'+i.split('#')[2])
    userinfo={'user_id':user_id,'user_name':user_name,'user_pass':user_password,'user_name_pass':user_name_pass,'user_zgye':user_zgye,'user_yyye':user_yyye}
    return userinfo
def get_cur_username(id):
    req_user_id=id.split('.')[0]
    all_user=check_user()
    loca_user_id=all_user['user_id']
    cur_name=all_user['user_name'][loca_user_id.index(req_user_id)]
    return cur_name
def baidu_net(request):
    user_get = request.GET
    user_id = list(user_get.keys())[0]
    return render(request, "baidu_net_home.html", locals())
def save_zz():
    global share_info,bp
    while True:
        if share_info == {}:
            break
        i = 0
        zd_key = list(share_info.keys())
        user_id = zd_key[i]
        share_info[user_id]['ts'] = '开始准备'
        user_name = get_cur_username(user_id+'.0.0.0')
        share_url = share_info[user_id]['share_url']
        url_pass = share_info[user_id]['url_pass']
        for j in range(len(share_url)):
            zc = BaiDuPan()
            zc_path = '/apps/bypy/'+user_name
            bp = ByPy('0%')
            # 百度网盘创建文件夹zhoulong
            ro_path_list = bp.list('/')
            if 'D-'+user_name in ro_path_list:
                pass
            else:
                bp.mkdir(user_name)
            save = zc.saveShare(share_url[j], pwd=url_pass[j], path=zc_path)
            zc_stion = save['err_msg']
            if zc_stion == '转存成功':
                share_info[user_id]['ts'] = '开始下载'
                zc_ro_path = save['extra']['list'][0]['to']
                zc_ro_fename = zc_ro_path.split('/')[-1]
                share_info[user_id]['ts'] = '开始下载：'+zc_ro_fename

                ro_path = user_name + '/'+zc_ro_fename
                if user_name == 'z':
                    lo_path = 'D:/self/'+moren_loca_lj+'/'+zc_ro_fename
                else:
                    lo_path = 'D:/other_user/'+moren_loca_lj+'/'+zc_ro_fename
                share_info[user_id]['zt'] = '1'
                a = bp.download(remotepath=ro_path, localpath=lo_path)
                share_info[user_id]['ts'] = '下载完成'
                share_info[user_id]['zt'] = '0'
                bp.delete(ro_path)
                del_info = user_id +fgf+share_url[j]
                del_xiaz_xl(del_info)
                read_share_info()
                time.sleep(3)
            else:
                share_info[user_id]['ts'] = '转存失败'


def del_xiaz_xl(del_info):
    with open('share_url_down_info.txt','r') as f:
        info = f.read()
    info = info.split('\n')
    del info[-1]
    x_info = []
    for i in info:
        j = i.split(fgf)
        if j[0]+fgf+j[1] == del_info:
            pass
        else:
            x_info.append(j[0]+fgf+j[1]+fgf+j[2]+'\n')
    with open('share_url_down_info.txt','wt') as f:
        for i in x_info:
            f.write(i)

t_net = threading.Thread(target=save_zz)
share_info={}
def read_share_info():
    global share_info
    share_infoo={}
    with open('share_url_down_info.txt','r') as f:
        info = f.read()
    info = info.split('\n')
    del info[-1]
    for i in info:
        user_id = i.split(fgf)[0]
        if user_id not in share_infoo.keys():
            share_infoo[user_id]={}
            share_infoo[user_id]['share_url'] = []
            share_infoo[user_id]['url_pass'] = []
        share_infoo[user_id]['share_url'].append(i.split(fgf)[1])
        share_infoo[user_id]['url_pass'].append(i.split(fgf)[2])
        if user_id in share_info.keys() and 'ts' in share_info[user_id].keys():
            share_infoo[user_id]['ts'] = share_info[user_id]['ts']
        else:
            share_infoo[user_id]['ts'] =''
        if user_id in share_info.keys() and 'zt' in share_info[user_id].keys():
            share_infoo[user_id]['zt'] = share_info[user_id]['zt']
        else:
            share_infoo[user_id]['zt'] ='0'
        if user_id in share_info.keys() and 'jd' in share_info[user_id].keys():
            share_infoo[user_id]['jd'] = share_info[user_id]['jd']
        else:
            share_infoo[user_id]['jd'] ='0%'
    share_info={}
    share_info = share_infoo



def baidu_net_ss(request):
    global t_net,bp
    info = request.GET
    user_id = info['user_id']
    share_url = info['url']
    share_pass = info['pass']
    read_share_info()
    if user_id[0] in share_info.keys() and share_url in share_info[user_id[0]]['share_url'] or share_url == '':
        pass

    else:
        with open('share_url_down_info.txt','at') as f:
            if share_pass == '':
                share_pass='nopass'
            f.write(user_id[0]+fgf+share_url+fgf+share_pass+fgf+'0%'+'\n')
        if user_id[0] in share_info.keys():
            share_info[user_id[0]]['share_url'].append(share_url)
        else:
            share_info[user_id[0]]={'jd':'0%','ts':'加入下载队列','zt':'0'}
            share_info[user_id[0]]['share_url']=[share_url]
        read_share_info()
        if t_net.isAlive():
            pass
        else:
            t_net = threading.Thread(target=save_zz)
            t_net.setDaemon(True)
            t_net.start()
    user_id_list = list(share_info.keys())
    for i in user_id_list:
        if share_info[i]['zt'] == '1':
            share_info[i]['jd'] = bp.jd
    if share_info != {}:
        if user_id[0] in user_id_list:
            re = json.dumps(share_info[user_id[0]])
        else:
            re = json.dumps({})
    else:
        re = json.dumps({})
    return HttpResponse(re)
