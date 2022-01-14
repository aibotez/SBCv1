import requests,os,time,json
from pynput import keyboard
from pynput.keyboard import Key
import threading,tkinter
import pyperclip
from win32api import GetSystemMetrics
from .thread_up_fie import ThreadUpFie

def time_chuo():
    time_c=time.time()
    return str(time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time_c)))

def check_ipv6(ym):
    res=os.system('ping '+ym)
    #os.system('cls')
    return res

def check_romte_fies(name,lj):
    re_url=url+'?name='+name+'&luj='+lj
    try:
        res=requests.get(re_url).text
    except Exception as e:
        with open(error_log,'a') as f:
            f.write('line23  ',+str(e)+'\n')
        print(e)
    res=json.loads(res)
    return res


#check_romte_fies('z','D:/self')
def check_loca_fes1(loca_lj):
    local_fies_info = {}
    local_fies_info['fe_name'] = []
    local_fies_info['fe_xgtime'] = []
    local_fies_info['fe_lj'] = []
    local_fies_info['fe_falj'] = []
    fie_list = os.listdir(loca_lj)
    for i in fie_list:
        fename = i
        felj = loca_lj + '/' + i
        fefalj = loca_lj
        if os.path.isdir(loca_lj + '/' + i):
            fexgtime = '0'
        else:
            fexgtime = time.ctime(os.path.getmtime(user_conf_fe))
        local_fies_info['fe_name'].append(fename)
        local_fies_info['fe_xgtime'].append(fexgtime)
        local_fies_info['fe_lj'].append(felj)
        local_fies_info['fe_falj'].append(fefalj)
    return local_fies_info

def xiug_tb_info(user_lj):
    romte_lj = '服务器备份路径#'+'D:'+user_lj+'同步备份'+'\n'
    loca_lj = '本地备份路径#'+'D:\\bacuk'+'\n'
    tbxz = '备份选择(a 远端备份至本地 b 本地备份至远端 c 双向备份，只填如 a)#'+'b'+'\n'
    nt_sc = '粘贴上传路径#'+'D:'+user_lj+'粘贴保存'+'\n'
    fwym = '访问域名#'+'zhenz.club'
    info = romte_lj+loca_lj+tbxz+nt_sc+fwym
    with open(user_conf_fe,'w',encoding='utf-8') as f:
        f.write(info)
def check_user_conf():
    if os.path.exists(user_conf_fe):
        with open(user_conf_fe,'r',encoding='utf-8') as f:
            info=f.read()
    else:
        return 'No '+user_conf_fe
    info = info.split('\n')
    user_conf={}
    # user_conf['user']=info[0].split('#')[-1]
    # user_conf['password'] = info[1].split('#')[-1]
    user_conf['romote_loca'] = info[0].split('#')[-1]
    user_conf['loca_romote'] = info[1].split('#')[-1]
    user_conf['bak_chose'] = info[2].split('#')[-1]
    user_conf['zt_sc'] = info[3].split('#')[-1]
    user_conf['ym'] = info[4].split('#')[-1]
    return user_conf
def jiaoy_user_conf(user_name):
    if user_name == 'z':
        user_lj = '\\self\\'
    else:
        user_lj = '\\other_user\\'+user_name+'\\'
    if os.path.exists(user_conf_fe):
        ro_back_lj=''
        with open(user_conf_fe,'r',encoding='utf-8') as f:
            info=f.read()
            info = info.split('\n')
            ro_back_lj = info[0].split('#')[-1]
            if user_name == 'z':
                if user_lj in ro_back_lj[0:8]:
                    pass
                else:
                    xiug_tb_info(user_lj)
            else:
                if user_lj in ro_back_lj[0:15+len(user_name)]:
                    pass
                else:
                    xiug_tb_info(user_lj)
    else:
        xiug_tb_info(user_lj)
def local_ro_fe_tanser(localj):
    print('69',localj,lo_bacuk_lj,ro_bacuk_lj)
    return localj.replace(lo_bacuk_lj,ro_bacuk_lj)
def re_jl(lj):
    timee = str(time.strftime('%Y%m%d%H%M%S',time.localtime(os.path.getmtime(lj))))
    fe_size = str(os.path.getsize(lj))
    fes_zd = {'lj': lj, 'fe_size': fe_size, 'time': timee}
    return fes_zd
def read_jl():
    fexx = []
    with open(tongb_jl, 'r')as f:
        cont = f.read()
    if cont == '':
        return ''
    else:
        infols = cont.split('\n')
        del infols[-1]
        for i in infols:
            feinfo = i.split(fe_split_zf)
            lszd={'lj':feinfo[0],'fe_size':feinfo[1],'time':feinfo[2]}
            fexx.append(lszd)
        return fexx
def juge_del_fe(lofe_bj,lofe_ck):
    lsbl=[]
    for i in lofe_bj:
        if i not in lofe_ck:
            lsbl.append(i)
    for i in lsbl:
        del_jl(i)
def del_jl(lj_jl):
    JL = read_jl()
    for i in range(len(JL)):
        if JL[i] == lj_jl:
            JL[i]=''
    with open(tongb_jl, 'w')as f:
        for i in JL:
            if i != '':
                f.write(i['lj'] + fe_split_zf + i['fe_size'] + fe_split_zf + i['time'] + '\n')


def wrt_jl(lj):
    jug='0'
    JL = read_jl()
    timee = str(time.strftime('%Y%m%d%H%M%S',time.localtime(os.path.getmtime(lj))))
    print(timee)
    fe_size = str(os.path.getsize(lj))
    for i in JL:
        lj_jl=i['lj']
        fetime = i['time']
        jl_size = i['fe_size']
        if lj == lj_jl and int(timee) > int(fetime):
            JL[JL.index(i)]['time'] = timee
            JL[JL.index(i)]['fe_size'] = fe_size
            jug = '1'
    if jug =='1':
        with open(tongb_jl, 'w')as f:
            for i in JL:
                # f.write(i['lj'] + ' ')
                f.write(i['lj']+fe_split_zf+i['fe_size']+fe_split_zf+i['time']+'\n')
    else:
        with open(tongb_jl,'a')as f:
            f.write(lj+fe_split_zf+fe_size+fe_split_zf+timee+'\n')
def check_loca_fes11(loca_lj):
    fes_xx=[]
    for root, dirs, files in os.walk(loca_lj):
        files_ls=[]
        for i in files:
            if '~$' != i[0:2]:
                files_ls.append(i)
        files=[]
        files=files_ls

        for i in files:

            lj = root+'\\'+i
            timee=str(time.strftime('%Y%m%d%H%M%S',time.localtime(os.path.getmtime(lj))))
            fe_size=str(os.path.getsize(lj))
            # local_falj = root
            # ro_falj = local_falj.replace(loca_lj,ro_bacuk_lj)
            fename = i
            fes_zd={'lj':lj,'fe_size':fe_size,'time':timee}
            fes_xx.append(fes_zd)
        # for i in dirs:
        #     fes_xx = fes_xx + i
        #time.sleep(100)
    return fes_xx
def check_lofe_bt(lofe_bj,lofe_ck):#比较与参考
    lsbl=[]
    for i in lofe_bj:
        if i not in lofe_ck:
            lsbl.append(i)
    return lsbl
def check_loca_fes(loca_lj):
    print(ro_bacuk_lj,loca_lj)
    fes_xx=''
    for root, dirs, files in os.walk(loca_lj):
        print('1',root)
        print('2',dirs)
        print('3',files)
        for i in files:
            timee=time.ctime(os.path.getmtime(root+'\\'+i))
            fe_size=os.path.getsize(root+'\\'+i)
            fes_xx=fes_xx+i+timee
        for i in dirs:
            fes_xx = fes_xx + i
        #time.sleep(100)
    return fes_xx

def up_fe(file_name,chunk_size):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                print('stop')
                break
def up_fe_call(lj,ro_lj_fe):
    chunk_size=20*1024*1024
    data = {'luj': ro_lj_fe}
    data['cz'] = 's'
    res = requests.post(url, data=data)
    data['cz'] = ''
    for chuk in up_fe(lj,chunk_size):
        cs=1
        data['cz'] = ''
        fie_up = {'files':chuk}
        res = requests.post(url, files= fie_up, data=data).text
        while res == 'false':
            print(res)
            cs=cs+1
            time.sleep(3)
            res = requests.post(url, files=fie_up, data=data).text
            if cs > 3:
                break
        #print(res)
    return res
def thr_up_fe_call(lj,ro_lj_fe):
    fe_chunk_len = 1 * 1024 * 1024
    up = ThreadUpFie(lj,ro_lj_fe,url_root, fe_chunk_len)
    oplocalfe = up.openfie()
    if oplocalfe == 'erro':
        up_fe_call(lj, ro_lj_fe)
    else:

        up.creat_threads(8)
    return 'succ'


def del_kg(root,dirs,files):
    for i in dirs:
        if ' ' in i:
            new_name=i.replace(' ','_')
            os.rename(root+'\\'+i,root+'\\'+new_name)
            dirs[dirs.index(i)]=new_name
    for i in files:
        if ' ' in i:
            new_name=i.replace(' ','_')
            os.rename(root+'\\'+i,root+'\\'+new_name)
            files[files.index(i)]=new_name

def bijiao_l_r(loca_lj,ro_lj):
    # print('11111',loca_lj,ro_lj)
    fes_xx=''
    cur_fes_time=[]
    ro_fes=[]
    ro_fe=[]
    for root, dirs, files in os.walk(loca_lj):
        files_ls=[]
        for i in files:
            if '~$' != i[0:2]:
                files_ls.append(i)
        files=[]
        files=files_ls
        del_kg(root, dirs, files)

        cur_ro_wjj=root.replace(loca_lj,ro_lj)
        ro_info=check_romte_fies(name, cur_ro_wjj)
        # print(ro_info)
        if 'fes_name' in ro_info.keys():
            ro_fes=ro_info['fes_name']
        if 'fe_name' in ro_info.keys():
            ro_fe=ro_info['fe_name']
            ro_time=ro_info['fe_xgtime']
            ro_size = ro_info['fe_size']
        for i in files:

            timee=time.ctime(os.path.getmtime(root+'\\'+i))
            fe_size=os.path.getsize(root+'\\'+i)
            cur_fes_time.append(timee)
            fes_xx=fes_xx+i+timee
            #idx_ro=ro_fe.index(i)
            idx_lo=files.index(i)
            ro_lj_fe = cur_ro_wjj + '\\' + i
            if i not in ro_fe:
                print('up_fe')
                thr_up_fe_call(root+'\\'+i,ro_lj_fe)

            elif i in ro_fe and fe_size != ro_size[ro_fe.index(i)]:
                print('gengx_fe')
                thr_up_fe_call(root + '\\' + i, ro_lj_fe)
        for i in dirs:
            fes_xx = fes_xx + i
            if i not in ro_fes:
                data={'luj':cur_ro_wjj+'\\'+i}
                data['cz'] = 'N'
                # print('new_fes')
                res=requests.post(url,data=data)
    return fes_xx

import win32clipboard as wc
import win32con,io,base64
import operator
import win32api
from PIL import Image,ImageGrab
#copytxet = wc.GetClipboardData(win32con.CF_HDROP)
def get_zt_lx():
    try:
        wc.OpenClipboard()
        #wc.EmptyClipboard()
        if wc.IsClipboardFormatAvailable(win32con.CF_HDROP):
            wc.CloseClipboard()
            return 'wj'
        elif wc.IsClipboardFormatAvailable(win32con.CF_DIB):
            wc.CloseClipboard()
            return 'tp'
        elif wc.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
            wc.CloseClipboard()
            return 'txt'
        else:
            wc.CloseClipboard()
    except Exception as e:
        print(e)
        tc(e)
def zhbit64(im):
    output_buffer = io.BytesIO()
    im.save(output_buffer, format='JPEG')
    binary_data = output_buffer.getvalue()
    base64_data = base64.b64encode(binary_data)
    base64_data = base64.b64decode(base64_data)
    #print(type(base64_data))
    return base64_data
def getCopyTxet():
    global im_befor_64,text_befor,wj_befor
    fe_leix=get_zt_lx()
    if fe_leix == 'tp':
        im_after=ImageGrab.grabclipboard()
        im_after_64 = zhbit64(im_after)
        if im_befor_64 == '':
            print('粘贴板里有新的截图')
            im_befor = ImageGrab.grabclipboard()
            im_befor_64=zhbit64(im_befor)
            data={}
            data['cz'] = 's'
            data['luj'] = ro_nt_lj+'\\图片\\'+time_chuo()+'.jpg'
            #data['fe'] = im_after_64
            fie_up = {'files': im_after_64}
            res = requests.post(url, files=fie_up, data=data).text
            if res =='succ':
                tc('上传成功')
                print('新的截图上传成功')
            else:
                print('新的截图上传失败')
            #print(res)
            #im_befor.save('1.jpg')
        elif im_befor_64 != im_after_64:#
            im_befor = ImageGrab.grabclipboard()
            im_befor_64=zhbit64(im_befor)
            data={}
            data['cz'] = 's'
            data['luj'] = ro_nt_lj+'\\图片\\'+time_chuo()+'.jpg'
            #data['fe'] = im_after_64
            fie_up = {'files': im_after_64}
            res = requests.post(url, files=fie_up, data=data).text
            if res =='succ':
                tc('上传成功')
                print('新的截图上传成功')
            else:
                print('新的截图上传失败')
        else:
            pass
    elif fe_leix == 'txt':
        #print('txt')
        wc.OpenClipboard()
        text_after =wc.GetClipboardData(win32con.CF_UNICODETEXT)

        if text_befor != text_after:
            print('有新的粘贴文本')
            text_befor=text_after
            data={}
            data['cz'] = 'nt_txt'
            data['luj'] = ro_nt_lj+'\\粘贴文本\\'+'粘贴文本.txt'
            data['txt']=time_chuo()+'\n'+wc.GetClipboardData(win32con.CF_UNICODETEXT).replace('\r','')+'\n\n'
            try:
                res = requests.post(url, data=data).text
            except:
                res = requests.post(url, data=data).text
            if res =='succ':
                tc('上传成功')
                print('新的粘贴文本添加成功')
            else:
                print('新的粘贴文本添加失败')
            #print('befo',text_befor)
        wc.CloseClipboard()
    elif fe_leix == 'wj':
        wc.OpenClipboard()
        wj_after = wc.GetClipboardData(win32con.CF_HDROP)[0]
        if wj_befor != wj_after:
            print('粘贴板里有新的文件 ',wj_after)
            wj_befor=wj_after
            if os.path.isdir(wj_befor):
                pjwj=wj_befor.split('\\')[-1]
                pjwj = pjwj.replace(' ', '_')
                bijiao_l_r(wj_after,ro_nt_lj+'\\文件\\'+pjwj)
                tc('上传成功')
                print('文件夹上传成功')
            else:
                pjwj = wj_befor.split('\\')[-1]
                if ' ' in pjwj:
                    pjwj=pjwj.replace(' ','_')
                    # rename=wj_befor[:int('-'+str(len(pjwj)))]+pjwj
                    # #os.rename(wj_befor,rename)
                    # wj_befor=rename
                    # wj_after=rename
                res=thr_up_fe_call(wj_befor,ro_nt_lj+'\\文件\\'+pjwj)
                if res == 'succ':
                    tc('上传成功')
                    print('文件上传成功')
                else:
                    print('文件上传失败')
        wc.CloseClipboard()

def jtstart():
    global jt_start_stop
    s0=''
    while True:
        if jt_start_stop == 'start':
            #wc.CloseClipboard()
            getCopyTxet()
        else:
            pass
            #print('结束监听')
        time.sleep(2)
pd=0
timestamp_win=-1
key1='0'
key2='0'

def on_press(key):
    global timestamp_win,jt_start_stop,pd,ck,key1,key2
    if isinstance(key, keyboard.KeyCode):
        if key.char == 'z':
            key1 = '1'
            timestamp_win = time.time()
        if key.char == 'o':
            key2 = '1'
            #if time.time() - timestamp_win < 0.5:
            if key1 == '1' and key2 == '1':
                key1 = '0'
                if pd % 2 == 0:
                    wc.OpenClipboard()
                    wc.EmptyClipboard()
                    wc.CloseClipboard()
                    time.sleep(0.5)
                    # getCopyTxet()
                    jt_start_stop = 'start'
                    tc_con('开始监听')
                    print('开始监听')
                else:
                    jt_start_stop = 'stop'
                    tc_con('结束监听')
                    print('结束监听')
                pd = pd + 1
                if pd == 10:
                    pd = 0
def on_release(key):
    global key1,key2
    if isinstance(key, keyboard.KeyCode):
        if key.char == 'z':
            key1 = '0'
        elif key.char == 'o':
            key2 = '0'
def jtnt():
    while True:
        #keyboard.Listener(on_press=on_press)
        with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
            listener.join()

def dengl(user,password,urll):
    res='0'
    dl_url= urll +'check_user_bf/?'+'name='+user+'&pass='+password
    try:
        res=requests.get(dl_url).text
    except:
        res='f'
    return res
def tc_yc():
    global ck
    time.sleep(1)
    try:
        ck.destroy()
    except:
        pass
def tc(info):
    global ck,t1
    if t1.isAlive():
        ck.destroy()
    # try:
    #     wh = ck.winfo_width()
    #     ck.destroy()
    # except:
    #     pass
    w=GetSystemMetrics (0)
    h=GetSystemMetrics (1)
    ck_w=170
    ck_h=70
    ck_x=w-ck_w-50
    ck_y=h-ck_h-100
    set_ck=str(ck_w)+'x'+str(ck_h)+'+'+str(ck_x)+'+'+str(ck_y)
    ck = tkinter.Tk()
    ck=tkinter.Toplevel()
    #ck.overrideredirect(True)
    ck.geometry(set_ck)
    text=tkinter.Label(ck,width=ck_w,font = ("Arial, 30"),text = info,background="yellow", foreground="red")
    text.place(x=0,y=0,width=ck_w,height=ck_h)
    t1=threading.Thread(target=tc_yc)
    #t1.daemon = True
    t1.start()
    ck.wm_attributes('-topmost', 1)
    #ck.mainloop()
def tc_con(info):
    tc_th = threading.Thread(target=tc, args=(info,))
    #tc_th.daemon = True
    tc_th.start()

def judge_fe(felj):
    felj1=local_ro_fe_tanser(felj)
    print('felj1',felj1)
    url_j = url_root + 'get_fe_info_judge?luj='+felj1
    res = requests.get(url_j)
    return res



def tongbu(ccs):
    global im_befor_64,text_befor,wj_befor,jt_start_stop,pd,timestamp_win,user_conf_fe,ym,url_root,ro_nt_lj,url,name
    global t1,ro_bacuk_lj,tongb_jl,lo_bacuk_lj,error_log,fe_split_zf
    fe_split_zf='$'
    url_root = ccs[0]
    name = ccs[1]
    print(url_root, name)
    tongb_jl = 'TBJL.log'
    error_log = 'error.log'
    im_befor_64 = ''
    text_befor = ''
    wj_befor = ''
    jt_start_stop = 'stop'
    jt_start = threading.Thread(target=jtstart)
    # jt_start.setDaemon(True)
    jt_start.start()
    pd = 0
    timestamp_win = -1
    t1 = threading.Thread(target=tc_yc)
    user_conf_fe = 'auto_up.txt'
    jiaoy_user_conf(name)


    info = check_user_conf()

    ym = info['ym']
    # # ym='zhenz.club'
    # # ym='127.0.0.1'
    # if ym == '127.0.0.1':
    #     url_root = 'http://' + ym + ':9500/'
    # else:
    #     url_root = 'http://' + ym + '/'
    # url = url_root + 'check_romote_fes/'
    # # url='http://127.0.0.1:9500/check_romote_fes/'
    # name = info['user']
    # password = info['password']
    url = url_root + 'check_romote_fes/'
    bf_cz = info['bak_chose']
    loca_lj = info['loca_romote']
    lo_bacuk_lj=loca_lj
    # print(loca_lj)
    if os.path.isdir(loca_lj):
        pass
    else:
        os.mkdir(loca_lj)
    ro_lj = info['romote_loca']
    ro_bacuk_lj = ro_lj
    ro_nt_lj = info['zt_sc']
    judge = ''
    # check_user = dengl(name, password,url_root)
    # if check_user == '1':
    #     print('登录成功')
    # else:
    #     while check_user != '1':
    #         if check_user == '0':
    #             print('账号密码错误')
    #         elif check_user == 'f':
    #             print('连接失败')
    #         time.sleep(10)

    jtjp_th = threading.Thread(target=jtnt)
    # jtjp_th.setDaemon(True)
    jtjp_th.start()
    check_user = '1'
    if check_user == '1':
        # ipv6_net_sation = check_ipv6(ym)


        judge = []
        if os.path.exists(tongb_jl):
            with open(tongb_jl,'r')as f:
                tb_jl = f.read()
        else:
            with open(tongb_jl, 'w')as f:
                f.write('')
            tb_jl=''
        if tb_jl == '':
            for root, dirs, files in os.walk(loca_lj):
                files_ls = []
                for i in files:
                    if '~$' != i[0:2]:
                        files_ls.append(i)
                files = []
                files = files_ls
                for i in files:
                    felj =  root+'\\'+i
                    fe_size = str(os.path.getsize(felj))
                    # print('fesi',fe_size,felj)

                    judge_fe1 = judge_fe(felj).text
                    # print('judge', judge_fe1)
                    if fe_size != judge_fe1:
                        print('shangc')
                        res = thr_up_fe_call(felj,local_ro_fe_tanser(felj))
                        if res !='false':
                            re_jl_zd=re_jl(felj)
                            judge.append(re_jl_zd)
                            wrt_jl(felj)
                        else:
                            with open(error_log, 'a') as f:
                                f.write('594#文件上传错误  ', +felj+ '\n')
                    else:
                        re_jl_zd = re_jl(felj)
                        judge.append(re_jl_zd)
                        wrt_jl(felj)
        else:
            judge = read_jl()

        while True:
            loca_scan = check_loca_fes11(loca_lj)
            # print('641',loca_scan,judge)
            juge_del_fe(judge,loca_scan)
            fe_chage=check_lofe_bt(loca_scan,judge)
            # print('644',fe_chage)
            if fe_chage !=[]:
            # if judge != loca_scan:
                print('文件发生变动，同步中...')
                if bf_cz == 'b':
                    try:
                        for i in fe_chage:
                            felj1 = i['lj']
                            judge_fe1 = judge_fe(felj1).text
                            if judge_fe1 == 'nofile':
                                jugs = '1'
                            else:
                                fe_size = str(os.path.getsize(felj1))
                                if fe_size != judge_fe1:
                                    jugs = '1'
                                else:
                                    jugs = '0'
                                    wrt_jl(felj1)
                            if jugs =='1':
                                print('shangc',felj1,local_ro_fe_tanser(felj1))
                                res = thr_up_fe_call(felj1,local_ro_fe_tanser(felj1))
                                if res !='false':
                                    wrt_jl(felj1)
                                else:
                                    with open(error_log, 'a') as f:
                                        f.write('631#文件上传错误  ', +felj + '\n')
                        judge = read_jl()
                        # judge = bijiao_l_r(loca_lj, ro_lj)
                    except Exception as e:
                        with open(error_log, 'a') as f:
                            f.write('616  ', +str(e)+'\n')
                        print(e)
                        time.sleep(200)
                elif bf_cz == 'a':
                    print('暂未开通')
                elif bf_cz == 'c':
                    print('暂未开通')
                else:
                    print('error ！ 选择错误')
                print('完成..')
                tc('更新完成')
            else:
                pass
                # print('scan')
            time.sleep(1*60)

    elif check_user == '0':
        print('账户密码错误')
    elif check_user == 'f':
        print('网络错误')
#tongbu()