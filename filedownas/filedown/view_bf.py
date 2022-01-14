
from django.http import HttpResponse,JsonResponse
import os,time

path=os.getcwd().replace('\\','/')
path=path+'/user/user.txt'
def check_user():
    user_info = path
    with open(user_info, 'r') as f:
        res=f.read()
    if len(res)>0:
        res=res.split('\n')
        del res[-1]
    user_name_pass=[]
    for i in res:
        user_name_pass.append(i.split('#')[1]+'#'+i.split('#')[2])
    userinfo={'user_name_pass':user_name_pass}
    return userinfo
def dengl(user_name, user_password):
    global name
    pass_user='0'
    if len(user_name) > 1 and len(user_password) == 0:
        pass_user = '0'
    elif len(user_name) == 1 and len(user_password) == 0:
        pass_user = '无效用户名'
    elif len(user_name) > 0 and len(user_password) > 0:
        if user_name + '#' + user_password in check_user()['user_name_pass']:
            pass_user = '1'
            name=user_name
        else:
            pass_user = '0'
    # print(f,s)
    # return render(request, "dlzc.html")
    return pass_user
def check_user_bf(request):
    info=request.GET
    user_name=info['name']
    user_pass=info['pass']
    passuser = dengl(user_name, user_pass)
    return HttpResponse(passuser)




def check_loca_fes(loca_lj):
    local_fies_info = {}
    local_fies_info['fe_name'] = []
    local_fies_info['fes_name'] = []
    local_fies_info['fe_xgtime'] = []
    local_fies_info['fe_lj'] = []
    local_fies_info['fe_falj'] = []
    local_fies_info['fe_size'] = []
    fie_list = os.listdir(loca_lj)
    for i in fie_list:
        felj = loca_lj + '\\' + i
        if os.path.isdir(loca_lj + '\\' + i):
            fesname=i
            local_fies_info['fes_name'].append(fesname)
        else:
            fename=i
            fexgtime = time.ctime(os.path.getmtime(loca_lj + '\\' + i))
            fe_size=os.path.getsize(loca_lj + '\\' + i)
            local_fies_info['fe_xgtime'].append(fexgtime)
            local_fies_info['fe_name'].append(fename)
            local_fies_info['fe_size'].append(fe_size)

    return local_fies_info


def check_romote_fes(request):
    if request.method == "GET":
        get_info=request.GET
        user=get_info['name']
        user_luj = get_info['luj']
        if os.path.isdir(user_luj):
            pass
        else:
            os.makedirs(user_luj)
        data=check_loca_fes(user_luj)
        return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
    else:
        res = request.POST
        lj=res['luj'].replace('\\','/')
        # fa_lj=lj.split('/')[-1]
        # c
        # if os.path.isdir(fa_lj):
        #     pass
        # else:
        #     print(fa_lj,'ljjj')
        #     os.makedirs(fa_lj)

        if request.FILES != {}:
            try:
                fename=lj.split('/')[-1]
                fa_lj = lj.replace('/'+fename,'')
                if not os.path.isdir(fa_lj):
                    os.makedirs(fa_lj)
                file_obj = request.FILES.get("files")
                with open(lj, "ab") as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)
                return HttpResponse('succ')
            except Exception as e:
                print('bf_101',e)
                return HttpResponse('false')
        else:
            if res['cz'] =='N':
                os.mkdir(lj)
            elif res['cz'] == 's' and os.path.exists(lj):
                os.remove(lj)
            elif res['cz'] == 's' and not os.path.exists(lj):
                fename=lj.split('/')[-1]
                fa_lj = lj.replace('/'+fename,'')
                if not os.path.isdir(fa_lj):
                    os.makedirs(fa_lj)
                
                
            elif res['cz'] == 'nt_txt':
                try:
                    falj = lj.replace('/粘贴文本.txt','')
                    print(falj,117)
                    print(lj,118)
                    if not os.path.isdir(falj):
                        os.makedirs(falj)
                    txt=res['txt']
                    with open(lj,'a',encoding='utf-8') as f:
                        f.write(txt)
                    return HttpResponse('succ')
                except Exception as e:
                    print('121,view_bf',e)
                    return HttpResponse('false')
            elif res['cz'] == '':
                with open(lj,'w') as f:
                    f.write('')


            return HttpResponse('')
