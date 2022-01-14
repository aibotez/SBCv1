import os,time,requests,threading
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk
import win32clipboard as wc
import win32con,io,base64
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
import tkinter.font as tkFont
import sys
falj = os.getcwd()
sys.path.append(falj)
from pck.aut_b import tongbu,dengl
from pck.get_computer_info import get_computer_info
from pck.thread_down_fie import ThreadDownFie
from pck.thread_up_fie import ThreadUpFie




ym1 = 'http://127.0.0.1:9500/'
#ym1 = 'http://zhenz.club/'
moren_lj = 'MRLJ.txt'
ym_wj='YM.txt'
khd_version = '1.0.2'



if os.path.exists(ym_wj):
    with open(ym_wj,'r') as f:
        ym = f.read()
else:
    with open(ym_wj,'wt') as f:
        f.write(ym1)
    ym = ym1

def khd_v_judge():
    global ym
    global khd_version
    if ym[-1] =='/':
        url_v = ym+ 'khd_version_judge/?khd_version_judge=' + khd_version
    else:
        url_v =  ym+'/khd_version_judge/?khd_version_judge=' + khd_version
    res = requests.get(url_v).text
    return res




def get_fa_lj(path,src_path):
    fe_lst = path.split('/')
    lsbl = ''
    for i in fe_lst:
        if fe_lst.index(i) < len(fe_lst)-2:
            lsbl = lsbl + i +'/'
    if lsbl == '':
        lsbl = fe_lst[0]
    else:
        lsbl = lsbl + fe_lst[-2]
    if src_path in lsbl:
        return lsbl
    else:
        return src_path
def get_format_time(t):
    pass
def up_fe(file_name,chunk_size):
    try:
        t0 = time.time()
        fe_size0 = int(os.path.getsize(file_name))
        fe_size = get_size(fe_size0)
        sc_qb.delete('0.0','end')
        sc_qb.insert('0.0',fe_size)
        yc=0
        sc_yy.delete('0.0','end')
        sc_yy.insert('0.0',str(yc))
    except Exception as e:
        print(e)
    with open(file_name, 'rb') as f:
        while True:
            use_time1 = time.time()
            c = f.read(chunk_size)
            if c:
                try:
                    yc = yc +len(c)
                    sc_yy.delete('0.0', 'end')
                    size_yy = get_size(yc)
                    sc_yy.insert('0.0', size_yy)
                    t_1 = time.time()-t0
                    if t_1 ==0:
                        t_1 = 0.000001

                    speed = yc/t_1
                    speed = get_size(speed)+'/S'
                    sc_spd_sc.delete('0.0','end')
                    sc_spd_sc.insert('0.0',speed)
                    but_wh = int((yc / fe_size0) * 10)
                    butto_sped_y_sc.config(width=but_wh)
                except Exception as e:
                    print(e)

                yield c
            else:
                pass
                #print('stop')
                break
def thr_up_fe_call(lj,ro_lj_fe,url):
    fe_chunk_len = 1 * 1024 * 1024
    up = ThreadUpFie(lj,ro_lj_fe, ym, fe_chunk_len)
    oplocalfe = up.openfie()
    def run():
        up.creat_threads(8)
    t1 = threading.Thread(target=run)
    t1.setDaemon(True)
    t1.start()
    # up.creat_threads(8)
    sc_qb.delete('0.0', 'end')
    sc_qb.insert('0.0', get_size(up.fe_size))
    yc = 0
    sc_yy.delete('0.0', 'end')
    sc_yy.insert('0.0', str(yc))
    while up.cur_up_size < up.fe_size:
        sc_yy.delete('0.0', 'end')
        sc_yy.insert('0.0',get_size(up.cur_up_size))
        speed = get_size(up.cur_speed*1024*1024) + '/S'
        sc_spd_sc.delete('0.0', 'end')
        sc_spd_sc.insert('0.0', speed)
        but_wh = int((up.cur_up_size/up.fe_size) * 10)
        butto_sped_y_sc.config(width=but_wh)
        time.sleep(0.3)
    sc_yy.delete('0.0', 'end')
    sc_yy.insert('0.0', get_size(up.cur_up_size))


def up_fe_call(lj,ro_lj_fe,url):
    chunk_size=1*1024*1024

    re_url =url +'?luj='+base64_bm(ro_lj_fe)+'&&cz=remove'
    data = {}
    data['luj'] = base64_bm(ro_lj_fe)
    # data['cz'] = 'remove'
    res = requests.get(re_url)
    # data['cz'] = ''
    # print(url)
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
def shangc(cs):#txt_sc,sc_yy,sc_qb,butto_sped_sc,sc_spd_sc,canvas_sc
    loca_lj = cs[0]
    romote_lj =cs[1]
    url = cs[2]
    loca_fa_lj = get_fa_lj(loca_lj,':')
    romote_fa_lj = get_fa_lj(romote_lj,user_lj)
    romote_lj_pj = loca_lj.replace(loca_fa_lj, romote_fa_lj)
    sc_ll=''
    fh_sc_ll=''
    if os.path.isdir(loca_lj):
        #print(romote_lj_pj)
        all_fes =[]
        fh_fes=[]
        sy_fes=[]
        for root, dirs, fies in os.walk(loca_lj):
            for i in fies:
                all_fes.append(i+'\n')
                sc_ll = sc_ll+i+'\n'
        sc_ll = sc_ll
        try:
            txt_sc.insert('0.0','正在上传'+'\n\n\n'+sc_ll)
        except Exception as e:
            print(e)
        for root,dirs,fies in os.walk(loca_lj):
            #res = requests.post(url, files={}, data=data).text
            root = root.replace('\\','/')
            romote_lj_pj = root.replace(loca_fa_lj, romote_fa_lj)
            data ={}
            data['luj'] = base64_bm(romote_lj_pj)
            res = requests.post(url, files={}, data=data).text
            for i in fies:
                loca_fe = root+'/'+i
                romte_fe = romote_lj_pj+'/'+i
                thr_up_fe_call(loca_fe, romte_fe, url)

                try:
                    fh_fes.append(i)
                    fh_sc_ll =fh_sc_ll+i+'\n'
                    scll = sc_ll.replace(fh_sc_ll,'')
                    lsbl = scll+'\n\n\n'+'完成上传：'+'\n'+sc_ll
                    txt_sc.delete('0.0','end')
                    txt_sc.insert('0.0','正在上传'+'\n\n\n'+lsbl)
                except Exception as e:
                    print(e)

            # print(romote_lj_pj)
            #print(root)
            # print(dirs)
            # print(fies)
    else:
        data = {}
        data['luj'] = romote_lj_pj
        try:
            txt_sc.insert('0.0', '正在上传' + '\n\n\n' + romote_lj_pj.split('/')[-1])
        except Exception as e:
            print(e)
        #res = requests.post(url, files={}, data=data).text
        thr_up_fe_call(loca_lj, romote_lj_pj, url)
        try:
            txt_sc.delete('0.0','end')
            txt_sc.insert('0.0', '上传完成' + '\n\n\n' + romote_lj_pj.split('/')[-1])
        except Exception as e:
            print(e)

    shuax(romote_fa_lj,canvas,'no')


def get_zt_lx():
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
# def xShowMenu(event):
#     menu = Menu(root, tearoff=0)
#     menu.add_command(label="复制", command=lambda: right_cz('ffffff'))
#     menu.add_separator()
#     menu.add_command(label="下载", command=lambda: right_cz('xxxxxxxxx'))
#     menu.add_separator()
#     menu.post(event.x_root, event.y_root)
huakuai_pos = 0
def processWheel(event):
    global huakuai_pos
    #canvas.create_window((90, 1000), window=frame)
    if event.delta > 0:
        if huakuai_pos <= 0:
            huakuai_pos=0
        else:
            huakuai_pos=huakuai_pos-0.03
        # 滚轮往上滚动，放大
        canvas.yview_moveto(huakuai_pos)
    else:
        if vbar.get()[1] == 1:
            huakuai_pos = huakuai_pos
        else:
            huakuai_pos = huakuai_pos + 0.03
        canvas.yview_moveto(huakuai_pos)
            # 滚轮往下滚动，缩小
# def an_ax(an_name):
#     print(an_name)
#     canvas.delete('all')
#     creat_fram()
#     for i in range(10):
#         cs = []
#         cs.append(i)
#         cs.append('f' + str(i))
#         creat_an(frame, cs)
#
#     globals()[an_name].destroy()

def choosepic(lj,an_name):
    #globals()[an_name]
    # path_=askopenfilename()
    path = an_name
    #canvas.yview_moveto(0.5)


    # path.set(path_)
    # img_open = Image.open(e1.get())
    img_open = Image.open(lj)
    img = ImageTk.PhotoImage(img_open)
    globals()[an_name].config(image=img)
    globals()[an_name].image = img  # keep a reference

    # l1.destroy()

def pos_info(info):
    global wj_info
    try:
        wj_info = Toplevel()
        #wj_info.overrideredirect(1)
        #wj_info.attributes("-alpha", 0.7)
        x=str(info[0])
        y=str(info[1])
        anname=info[2]
        print('1',anname)
        wj_info.geometry('+'+x+'+'+y)
        txt = Label(wj_info,text=anname+'ijuihuig',compound='center',font = ("Arial, 30"))
        #txt.place()
        txt.pack(fill=BOTH, expand=True)
        time.sleep(0.5)
        wj_info.destroy()
    except:
        pass
t1 = threading.Thread(target=pos_info)
mose_pos_x_befor=0
def an_mouse_move(event,mouse_cz):
    an_name = mouse_cz[0]
    judge = mouse_cz[1]
    if judge == 'no':
        txt_lj_t.set(an_name)
    else:
        txt_lj_share.set(an_name)
def frm_mouse_move(event):
    frm_mose_ab_pos_x=event.x_root
    frm_mose_ab_pos_y=event.y_root
    print('root',frm_mose_ab_pos_x,frm_mose_ab_pos_y)


def handlerAdaptor(fun, **kwds):
	'''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''
	return lambda event,fun=fun,kwds=kwds: fun(event, **kwds)
def creat_an(root_c,cs,judge):
    an_col = 5
    an_name=cs[2]
    if judge == 'no':
        mouse_cz=[]
        mouse_cz.append(an_name)
        mouse_cz.append('no')
        txt_lj_t.set(an_name)
    else:
        mouse_cz=[]
        mouse_cz.append(an_name)
        mouse_cz.append('share')
        txt_lj_share.set(an_name)
    xl=cs[0]
    cur_lj=cs[2]
    fie_name = cs[3]
    fe_type = cs[4]
    row1 = (int(xl/an_col)+1)*1
    row = row1*2-1
    row_txt = 2*row1
    column= xl - (row1-1)*an_col
    globals()[an_name] = Button(root_c,width=100,height=100,command=lambda: left_cz(cur_lj,judge))
    if fe_type == 'dirs':
        lj='w.jpg'
    else:
        lj='wj.jfif'
    choosepic(lj,an_name)
    globals()[an_name].grid(row=row,column=column,columnspan = 1)
    b = fie_name.encode('gbk')
    if len(b) >= 14:
        txt = Label(root_c, text=fie_name,width=15,anchor = 'w')
    else:
        txt = Label(root_c, text=fie_name, width=15)
    txt.grid(row=row_txt, column=column)
    col_count, row_count = root_c.grid_size()
    #print(col_count, row_count)
    root_c.grid_columnconfigure(column, minsize=150)
    root_c.grid_rowconfigure(row, minsize=130)
    txt.grid_rowconfigure(row, minsize=20)

    globals()[an_name].bind("<Enter>", handlerAdaptor(an_mouse_move,mouse_cz=mouse_cz))
    #globals()[an_name].bind("<Enter>", lambda event:mouse_move(an_name))

    def xShowMenu(event):
        menu1 = Menu(root_c, tearoff=0)
        fe = []
        fe.append(an_name)
        fe.append(fe_type)
        if judge =='share':
            menu1.add_command(label="复制", command=lambda: right_cz_copy(fe))
            menu1.add_separator()
            menu1.add_command(label="下载", command=lambda: right_cz_xz(fe))
            menu1.add_separator()
            menu1.add_command(label="查看信息", command=lambda: right_cz_get_fe_info(fe))
            menu1.add_separator()
            menu1.post(event.x_root, event.y_root)

        else:
            menu1.add_command(label="复制", command=lambda: right_cz_copy(fe))
            menu1.add_separator()
            menu1.add_command(label="下载", command=lambda: right_cz_xz(fe))
            menu1.add_separator()
            menu1.add_command(label="删除", command=lambda: right_cz_delfe(fe))
            menu1.add_separator()
            menu1.add_command(label="分享", command=lambda: right_cz_share(fe))
            menu1.add_separator()
            menu1.add_command(label="重命名", command=lambda: right_cz_rename(fe))
            menu1.add_separator()
            menu1.add_command(label="查看信息", command=lambda: right_cz_get_fe_info(fe))
            menu1.add_separator()
            menu1.post(event.x_root, event.y_root)
    globals()[an_name].bind("<Button-3>", xShowMenu)
def rename(fe):
    fe_lj = fe[0]
    fe_type = fe[1]
    rename1 = rename_txt.get()

    if fe_type == 'fie' and '.' in fe_lj:
        re_lj = get_fa_lj(fe_lj,user_lj) + '/' + rename1+'.'+fe_lj.split('.')[-1]
    else:
        re_lj = get_fa_lj(fe_lj,user_lj) + '/' + rename1
    url = ym+'khd_rename/?luj_src='+base64_bm(fe_lj)+'&&luj_lat='+base64_bm(re_lj)
    try:
        res = requests.get(url,timeout=2)
    except Exception as e:
        print(e)
    rename_tok.destroy()
    fa_lj = get_fa_lj(fe_lj,user_lj)
    shuax(fa_lj,canvas,'no')

def right_cz_share(fe):
    def share_to_q():
        url = ym+'share/?'
        time_lt = share_time.get('0.0','end')
        if time_lt.split('\n')[0] =='时间限制':
            time_lt = ''
        pass_lt = share_pass.get('0.0','end')
        if pass_lt.split('\n')[0] =='查看密码':
            pass_lt = '**'
        to_w = share_to_w.get('0.0','end')
        if to_w.split('\n')[0] == '指定用户':
            to_w = '00'
        url = url+'share_time_limt='+time_lt+'&&share_pass='+pass_lt+'&&share_user_limt='+to_w+'&&share_lj='+fe[0]+'&&user='+user_id
        res = requests.get(url).text
        share_url = Text(share_to,height=1)
        share_url.place(x=0, y=150)
        share_url.insert('0.0', res[6:])
    share_to = Toplevel()
    share_to.geometry('430x320')
    share_name = fe[0].split('/')[-1]
    share_name='你要分享的文件: '+share_name
    share_ti = Label(share_to,text=share_name)
    share_ti.place(x=100,y=5)
    share_time = Text(share_to,width=30,height=1)
    share_time.place(x=100,y=40)
    share_time.insert('0.0','时间限制')
    share_pass = Text(share_to,width=30,height=1)
    share_pass.place(x=100,y=80)
    share_pass.insert('0.0','查看密码')
    share_to_w = Text(share_to,width=30,height=1)
    share_to_w.place(x=100,y=120)
    share_qd=Button(share_to,text='确定',command=share_to_q,width=15).place(x=100,y=170)
    share_to_w.insert('0.0','指定用户')
    txt_sm='时间限制如果直接填入数字，则会以小时为单位，如 0.5为半小时后过期，如果\n限制到某一天或某一时刻，时间用 "-" 分割,如： 14-20，为当天2点20后过期;\n3-1-14-20，为当年3月1号2点20过期 或者 2020-2-9-14-20；不可写成\n 2020-2-9；也可以直接写 2天或2月或2年，即2天、2月、2年后的这个时刻过期\n不填默认为不限制时间;\n密码为分享后查看该分享的密码；不填默认无密码'
    txt_sh = Label(share_to,text=txt_sm,justify=LEFT)
    txt_sh.place(x=0,y=200)
def right_cz_rename(fe):
    global rename_tok,rename_txt
    # print(fe)
    fe_lj = fe[0]
    fe_type=fe[1]
    rename_tok = Toplevel()
    #rename_tok.geometry("300x20+0+0")
    xiugname =''
    txt_fename = '文件名： '+fe_lj.split('/')[-1]
    txt1 = Label(rename_tok,text = txt_fename)
    txt1.pack()
    rename_txt = Entry(rename_tok)
    rename_txt.pack()
    lsbl=[]
    lsbl.append(fe_lj)
    lsbl.append(fe_type)
    buton1 = Button(rename_tok,text='确定',command=lambda:rename(lsbl)).pack()
def right_cz_get_fe_info(fe):
    fe_lj=fe[0]
    url = ym+'get_fe_info/?luj='+base64_bm(fe_lj)
    res='0'
    try:
        res = requests.get(url,timeout=2).text
    except Exception as e:
        print(e)
    pass
    if res[0] == '{':
        res = eval(res)
        fe_size = '文件大小： '+ str(get_size(res['fe_size']))
        fe_build_time = '文件创建时间： '+str(res['fe_build_time'])
        fe_xiug_time = '文件修改时间： '+str(res['fe_xiug_time'])
        fe_fangw_time = '文件访问时间： '+str(res['fe_fangw_time'])
        get_fe_tok = Toplevel()
        get_fe_tok.geometry('300x150')
        txt1 = Label(get_fe_tok, text=fe_size,anchor='w')
        txt1.place(x=0,y=0)
        txt2 = Label(get_fe_tok, text=fe_build_time)
        txt2.place(x=0,y=30)
        txt3 = Label(get_fe_tok, text=fe_xiug_time)
        txt3.place(x=0,y=60)
        txt4 = Label(get_fe_tok, text=fe_fangw_time)
        txt4.place(x=0,y=90)



def creat_fram(gd_len,cnas_c):
    global vbar#canvas,
    frame = Frame(cnas_c)  # 把frame放在canvas里
    frame.place()  # frame的长宽，和canvas差不多的
    # l1 = Button(frame ,command = lambda: choosepic(lj))
    # choosepic(lj)
    # l1.pack()
    vbar = Scrollbar(cnas_c, orient=VERTICAL)  # 竖直滚动条
    vbar.place(x=730, width=20, height=500)
    vbar.configure(command=cnas_c.yview)
    cnas_c.config(yscrollcommand=vbar.set)  # 设置
    cnas_c.create_window((0, 0), window=frame, anchor='nw')  # create_window
    cnas_c.config(scrollregion=(0,0,0,gd_len))
    return frame
def back_cz(judge):
    if judge == 'no':
        cur_lj = txt_lj_t.get()
        fa_lj = get_fa_lj(cur_lj,user_lj)
        fa_lj = get_fa_lj(fa_lj, user_lj)
        # print(fa_lj)
        shuax(fa_lj, canvas, 'no')
    else:
        cur_lj = txt_lj_share.get()
        fa_lj = get_fa_lj(cur_lj,share_lj)
        shuax(fa_lj, share_canvas, 'share')
    #
    #
    # cur_lj=txt_lj_t.get()
    # ls_bl = cur_lj.split(luj)
    # print(ls_bl,ls_bl[-1].split('/'))
    # if len(ls_bl[-1].split('/')) == 2:
    #     if judge == 'no':
    #         shuax(luj,canvas,'no')
    #     else:
    #         shuax(luj, share_canvas, 'share')
    # else:
    #     falj1 = cur_lj.split('/')
    #     ljj1 = falj1[-1]
    #     ljj2 = falj1[-2]
    #     ljj = '/' + ljj2 + '/' + ljj1
    #     print(ljj)
    #     falj = cur_lj.replace(ljj, '')
    #     if falj[-1] == ':':
    #         falj = falj + '/'
    #     if judge == 'no':
    #         shuax(falj,canvas,'no')
    #     else:
    #         shuax(falj, share_canvas, 'share')
def get_size(size):
    if size/1024/1024/1024 >=1:
        return str(round(size/1024/1024/1024,2))+'G'
    elif size/1024/1024 >=1:
        return str(round(size/1024/1024, 2)) + 'M'
    elif size/1024 >=1:
        return str(round(size/1024, 2)) + 'K'
    elif size >=1:
        return str(round(size, 2)) + 'B'
    elif size == 0:
        return str(0)
def del_xiaz_xl(fo):
    del fo[0]
    with open(xiaz_info,'w',encoding='utf-8') as f:
        for i in fo:
            f.write(i+'\n')
def del_xiaz_fh_xl(fo):
    while len(fo)>10:
        del fo[0]
    with open(xiaz_fh,'w',encoding='utf-8') as f:
        for i in fo:
            f.write(i+'\n')
def shuax_xiaz_txt_info():
    with open(xiaz_info, 'r', encoding='utf-8') as f:
        xiaz_fo = f.read()
    xiaz_lst = []
    xiaz_fh_lst=[]
    if '\n' in xiaz_fo:
        xiaz_xl = xiaz_fo.split('\n')
        del xiaz_xl[-1]
        for i in xiaz_xl:
            xiaz_lst.append(i.split('#')[0].split('/')[-1])
    with open(xiaz_fh, 'r', encoding='utf-8') as f:
        xiaz_fh_fo = f.read()
    if '\n' in xiaz_fh_fo:
        xiaz_fh_xl = xiaz_fh_fo.split('\n')
        del xiaz_fh_xl[-1]
        xiaz_fh_xl.reverse()
        for i in xiaz_fh_xl:
            xiaz_fh_lst.append(i.split('#')[0].split('/')[-1])
    re_info = '下载队列\n\n\n'
    for i in xiaz_lst:
        re_info = re_info +i+'\n'
    re_info = re_info+'\n\n\n'+'下载完成'+'\n'
    for i in xiaz_fh_lst:
        re_info = re_info + i+'\n'
    lbcd = len(xiaz_lst)+len(xiaz_fh_lst)
    canvas_1.config(scrollregion=(0, 0, 0, 10*lbcd))
    if len(xiaz_fh_lst) > 10:
        xiaz_fh_lst.reverse()
        del_xiaz_fh_xl(xiaz_fh_lst)
    #txt_xia.config(height=10*lbcd)
    return re_info
def xiaz_thr(lsbl):
    fe_chunk_len= 1*1024*1024
    show_xiaz_ck()
    # DownFie = ThreadDownFie
    # def run():
    #     DownFie.creat_threads(4)
    # t1 = threading.Thread(target=run)
    # t1.setDaemon(True)
    # t1.start()
    while True:
        with open(xiaz_info,'r',encoding='utf-8') as f:
            xiaz_xl = f.read()
        if '\n' in xiaz_xl:
            butto_sped_y.config(width=0)
            xiaz_spd.delete('0.0','end')
            xiaz_spd.insert('0.0','正在连接')
            print('有下载队列')
            xiaz_fo = xiaz_xl.split('\n')
            del xiaz_fo[-1]
            lj = xiaz_fo[0].split('#')[0]
            loca_lj = xiaz_fo[0].split('#')[1]
            if loca_lj == '00':
                fe_lj = lj.replace('\\', '/')
                fe_lj = fe_lj.split('/')[-1]
                loca_fe_lj = moren_xiaz_lj + '/' + fe_lj
            else:
                loca_fe_lj = loca_lj

            # print(lj,loca_lj)
            # lj = lsbl[0]
            # loca_lj=lsbl[1]
            fename = lj.split('/')[-1]
            url = ym +'khd_xz/?lj='+base64_bm(lj)+'&&name='+fename
            txt_xia.delete('0.0','end')
            txt_xia.insert('0.0',shuax_xiaz_txt_info())
            DownFie = ThreadDownFie(loca_fe_lj,lj, ym, fe_chunk_len)
            def run():
                DownFie.creat_threads(1)
            t1 = threading.Thread(target=run)
            t1.setDaemon(True)
            t1.start()
            while DownFie.cur_dow_size < DownFie.fe_size:
                fe_size = DownFie.fe_size
                xiaz_qb.delete('0.0','end')
                xiaz_qb.insert('0.0',get_size(fe_size))
                xiaz_yy.delete('0.0', 'end')
                fh_size = DownFie.cur_dow_size
                # print(fh_size, get_size(fh_size))
                xiaz_yy.insert('0.0', get_size(fh_size))

                but_wh = int((fh_size / fe_size) * 10)
                butto_sped_y.config(width=but_wh)
                xiaz_spd.delete('0.0', 'end')
                # xiaz_spd.insert('0.0', get_size(fh_size/use_time)+'/S')
                speed = DownFie.cur_speed*1024*1024
                xiaz_spd.insert('0.0', get_size(speed) + '/S')
                time.sleep(0.5)
            # print(fh_size, get_size(fh_size))
            xiaz_yy.delete('0.0', 'end')
            xiaz_yy.insert('0.0', get_size(DownFie.cur_dow_size))
            del_xiaz_xl(xiaz_fo)
            add_xiaz_fh(lj, loca_lj)
            time.sleep(1)
            txt_xia.delete('0.0', 'end')
            txt_xia.insert('0.0', shuax_xiaz_txt_info())
            time.sleep(1)
        else:
            print('下载完成')
            break

def xiaz(lsbl):
    show_xiaz_ck()

    while True:
        with open(xiaz_info,'r',encoding='utf-8') as f:
            xiaz_xl = f.read()
        if '\n' in xiaz_xl:
            butto_sped_y.config(width=0)
            xiaz_spd.delete('0.0','end')
            xiaz_spd.insert('0.0','正在连接')
            print('有下载队列')
            xiaz_fo = xiaz_xl.split('\n')
            del xiaz_fo[-1]
            lj = xiaz_fo[0].split('#')[0]
            loca_lj = xiaz_fo[0].split('#')[1]
            # print(lj,loca_lj)
            # lj = lsbl[0]
            # loca_lj=lsbl[1]
            fename = lj.split('/')[-1]
            url = ym +'khd_xz/?lj='+base64_bm(lj)+'&&name='+fename
            txt_xia.delete('0.0','end')
            txt_xia.insert('0.0',shuax_xiaz_txt_info())
            #txt_xia.insert('0.0',lj)

            try:
                r = requests.get(url, stream=True)
                #print(r.text)
                use_time1 = time.time()
                fe_size_int=int(r.headers['content-length'])
                fe_size = get_size(fe_size_int)
                xiaz_qb.delete('0.0','end')
                xiaz_qb.insert('0.0',fe_size)
                if loca_lj == '00':
                    fe_lj = lj.replace('\\', '/')
                    fe_lj = fe_lj.split('/')[-1]
                    loca_fe_lj = moren_xiaz_lj + '/'+fe_lj
                else:
                    loca_fe_lj = loca_lj
                with open(loca_fe_lj, 'wb') as f:
                    fh_size = 0
                    use_time = 0.1
                    for bl in r.iter_content(chunk_size=1 * 1024 * 1024):
                        if bl:
                            #print('xieru', len(bl) / 1024 / 1024)
                            f.write(bl)

                            use_time2 = time.time()
                            if use_time2 == use_time1:
                                use_time2 = 0.0001
                            speed = len(bl) / (use_time2-use_time1)
                            use_time1 = time.time()

                            fh_size = fh_size + len(bl)
                            use_time = time.time() - use_time1
                            xiaz_yy.delete('0.0','end')
                            xiaz_yy.insert('0.0',get_size(fh_size))
                            but_wh = int((fh_size/fe_size_int)*10)
                            butto_sped_y.config(width=but_wh)
                            xiaz_spd.delete('0.0', 'end')
                            #xiaz_spd.insert('0.0', get_size(fh_size/use_time)+'/S')
                            xiaz_spd.insert('0.0', get_size(speed) + '/S')
                            # print('已下载 ', fh_size / 1024 / 1024, '.....', '网速为： ', fh_size / 1024 / 1024 / use_time, '....用时为： ',
                            #       use_time)
                        else:
                            print('error')
                del_xiaz_xl(xiaz_fo)
                add_xiaz_fh(lj,loca_lj)
                time.sleep(1)
                txt_xia.delete('0.0', 'end')
                txt_xia.insert('0.0', shuax_xiaz_txt_info())
                time.sleep(1)
            except Exception as e:
                print(e)
        else:
            print('下载完成')
            break

def show_xiaz_ck():
    global xia_show,txt_xia,xiaz_yy,xiaz_qb,butto_sped_y,xiaz_spd,canvas_1
    try:
        xia_show.winfo_geometry()
    except:
        print('为创建')
        xia_show = Toplevel()
        xia_show.geometry("600x320+0+0")
        canvas_1 = Canvas(xia_show, width=600, height=320,scrollregion=(0, 0, 0, 1100))  # 创建canvas
        canvas_1.place(x=0, y=0)  # 放置canvas的位置
        frame_1 = Frame(xia_show, width=600, height=320)  # 把frame放在canvas里
        frame_1.place(x=0, y=0)  # frame的长宽，和canvas差不多的
        vbar_1 = Scrollbar(canvas_1, orient=VERTICAL)  # 竖直滚动条
        vbar_1.place(x=0, width=2, height=320)
        vbar_1.configure(command=canvas_1.yview)
        canvas_1.config(yscrollcommand=vbar_1.set)  # 设置
        canvas_1.create_window((0, 0), window=frame_1, anchor='nw')  # create_window
        canvas_1.config(scrollregion=(0, 0, 0, gd_len))
        txt_xia = Text(frame_1,width=600)
        txt_xia.place(x=0,y=0)
        canvas_speed = Canvas(xia_show,bg = 'white',width=300, height=20,scrollregion=(0, 0, 0, 1100))  # 创建canvas  bg = 'red'
        canvas_speed.place(x=300, y=0)
        xiaz_yy = Text(canvas_speed,width = 10,height = 2)
        xiaz_yy.place(x=0,y=0)
        xiaz_qb = Text(canvas_speed,width = 9,height = 2)
        xiaz_qb.place(x=150,y=0)
        xiaz_spd = Text(canvas_speed,width = 11,height = 2)
        xiaz_spd.place(x=215,y=0)
        butto_sped_q = Button(canvas_speed,bg = 'white',width = 10,height = 1)
        butto_sped_q.place(x=70,y=0)
        butto_sped_y = Button(canvas_speed,bg = 'green',width = 0,height = 1)
        butto_sped_y.place(x=70,y=0)
        butto_sped_y.config(width=0)

# import sys
# falj = os.getcwd()
# sys.path.append(falj)
# from pck.aut_b import tongbu,dengl
# from pck.get_computer_info import get_computer_info

xiaz_T = threading.Thread()
xiaz_info = 'xiaz_info.txt'
xiaz_fh = 'xiaz_fh.txt'
def add_xiaz(romte_lj,local_lj):
    with open(xiaz_info,'a',encoding='utf-8') as f:
        f.write(romte_lj+'#'+local_lj+'\n')
def add_xiaz_fh(romte_lj,local_lj):
    with open(xiaz_fh,'a',encoding='utf-8') as f:
        f.write(romte_lj+'#'+local_lj+'\n')
# def get_fa_lj(path):
#     fe_lst = path.split('/')
#     lsbl = ''
#     for i in fe_lst:
#         if fe_lst.index(i) < len(fe_lst)-2:
#             lsbl = lsbl + i +'/'
#     if lsbl == '':
#         lsbl = fe_lst[0] + '/'
#     else:
#         lsbl = lsbl + fe_lst[-2]
#     print(lsbl,path)
#     return lsbl
def right_cz_delfe(fe):
    url = ym+'khd_del_fe/?fe='+base64_bm(fe[0])
    del_sure=tk.messagebox.askokcancel('小黑云删除提示','是否要删除'+fe[0].split('/')[-1])
    if del_sure == True:
        res = requests.get(url)
        fa_lj = get_fa_lj(fe[0],user_lj)
        # print(fa_lj,'faa')
        txt_lj_t.set(fa_lj)
        shuax(fa_lj,canvas,'no')
def right_cz_xz(cz):
    global xiaz_T
    #if xiaz_T.isAlive():
    if cz[1] == 'dirs':
        fe_lj = cz[0]
        url = ym + 'khd_xz/?lj=' + base64_bm(fe_lj) + '&&name=' + 'abc'
        res = requests.get(url, stream=True).text
        # print('ress', res)
        res = eval(res)
        for i in res['root']:
            idx = res['root'].index(i)
            dirs1 = i.replace('\\', '/')
            dirs = dirs1.split('/')[-1]
            loca_dirs = moren_xiaz_lj + '/'+dirs
            if os.path.isdir(loca_dirs):
                pass
            else:
                os.makedirs(loca_dirs)
            fie = res['file']
            for j in fie[idx]:
                if j != '':
                    lsbl = []
                    lsbl.append(dirs1 + '/' + j)
                    lsbl.append(loca_dirs + '/' + j)
                    if xiaz_T.isAlive():
                        add_xiaz(dirs1 + '/' + j, loca_dirs + '/' + j)
                    else:
                        add_xiaz(dirs1 + '/' + j, loca_dirs + '/' + j)
                        xiaz_T = threading.Thread(target=xiaz,args=(lsbl,))
                        xiaz_T.setDaemon(True)
                        xiaz_T.start()
                    #xiaz(dirs1 + '/' + j, loca_dirs + '/' + j)
    else:
        fe_lj = cz[0]
        lsbl = []
        lsbl.append(fe_lj)
        lsbl.append('00')
        if xiaz_T.isAlive():
            add_xiaz(fe_lj,'00')
        else:
            add_xiaz(fe_lj, '00')
            xiaz_T = threading.Thread(target=xiaz_thr, args=(lsbl,))
            xiaz_T.start()
        # fe_lj = cz[0]
        # xiaz(fe_lj, '')

def right_cz_copy(cz):
    copy_src = cz[0]
    with open(right_zt_info,'w') as f:
        f.write(copy_src+'\n')
    #show_xiaz_ck()
    # print('ff',copy_src)
def left_cz(cz,judge):
    if judge == 'no':
        shuax(cz,canvas,'no')
    else:
        shuax(cz, share_canvas,'no')
def view_pdf(path):
    global image,im
    url = ym + 'pdf_c_jpg/?luj=' + path + '&&first=n&&page='+'0'
    url = ym+'khd_yl/?luj='+path+'&&user='+user
    res = requests.get(url).text
    res = eval(res)
    # print(res['data'])
    if res['station'] =='ok':
        with open('12.jpg','wb') as f:
            f.write(base64.b64decode(res['data']))

    # image = Image.open("img.jpg")
    # im = ImageTk.PhotoImage(image)
    # canvas.create_image(300, 50, image=im)
    image = Image.open("12.jpg")
    bl = 1
    wt = image.size[0]
    if wt > 800:
        bl = wt/800
    ht = image.size[1]
    wt_y = int(wt/bl)
    ht_y = int(ht/bl)
    image1 = image.resize((wt_y,ht_y),Image.ANTIALIAS)
    image = image1

    pdf_v = Toplevel()
    pdf_v.geometry('900x600')
    pdf_cans = Canvas(pdf_v,bg='white',width=800,height=600,scrollregion=(0,0,0,1100))
    pdf_cans.pack()
    vbar_p = Scrollbar(pdf_cans, orient=VERTICAL)  # 竖直滚动条
    vbar_p.place(x=800, width=8, height=600)
    vbar_p.configure(command=pdf_cans.yview)
    pdf_cans.config(yscrollcommand=vbar_p.set)  # 设置
    #image = Image.open("12.jpg")
    im = ImageTk.PhotoImage(image)
    pdf_cans.create_image(0, 0, anchor=NW,image=im)
from urllib import parse
import webbrowser as web
# browser = web.open('http://zhenz.club',new=0,autoraise=True)
def base64_bm(wb):
    # s = str(base64.b64encode(wb.encode()))
    s=base64.b64encode(wb.encode('utf-8')).decode()
    return s
    #return s.replace('b','').replace("'",'')
def shuax(path,canvas_c,judge):

    url =ym+'khd_fe_re/?lj='+base64_bm(path)
    # print(url)
    res = requests.get(url).text
    res=eval(res)
    data_type = res['data_type']
    # print(judge,'judge')
    if judge == 'no':
        if data_type == 'dirs':
            canvas_c.delete('all')
            fe_info = res['data']
            if fe_info == []:
                if '.!toplevel' in str(canvas_c):
                    lsbl = txt_lj_share.get()
                    txt_lj_share.set(lsbl + '/..')
                else:
                    lsbl = txt_lj_t.get()
                    txt_lj_t.set(lsbl + '/..')
            gd_len = (int(len(fe_info) / 5) + 1) * 180
            frame = creat_fram(gd_len,canvas_c)
            for i in fe_info:
                cs = []
                cs.append(fe_info.index(i))
                cs.append('f' + str(fe_info.index(i)))
                cs.append(i['fe_lj'])
                cs.append(i['fe_name'])
                cs.append(i['fe_type'])
                if '.!toplevel' in str(canvas_c):
                    creat_an(frame, cs,'share')
                else:
                    creat_an(frame, cs, 'no')
        else:
            # url = ym+'pdf_c_jpg/?luj='+path+'&&first=y'
            # res = requests.get(url).text
            # if res == 'pdf':
            #     view_pdf(path)
            url = ym + 'khd_yl/?luj=' + path + '&&user=' + user
            browser = web.open(url, new=0, autoraise=True)

    else:
        frame = creat_fram(300, share_canvas)
        cs = []
        cs.append(1)
        cs.append('f1')
        cs.append(path)
        cs.append(path.split('/')[-1])
        cs.append(data_type)
        creat_an(frame, cs,'share')
       # url = 'http://127.0.0.1:9500/khd_fe_re/?lj=D:/1'
def creat_shangc_ck():
    global shangc_show,txt_sc,sc_yy,sc_qb,butto_sped_y_sc,sc_spd_sc,canvas_sc
    try:
        shangc_show.winfo_geometry()
    except:
        print('为创建')
        shangc_show = Toplevel()
        shangc_show.geometry("600x320+0+0")
        canvas_sc = Canvas(shangc_show, width=600, height=320,scrollregion=(0, 0, 0, 1100))  # 创建canvas
        canvas_sc.place(x=0, y=0)  # 放置canvas的位置
        frame_1 = Frame(shangc_show, width=600, height=320)  # 把frame放在canvas里
        frame_1.place(x=0, y=0)  # frame的长宽，和canvas差不多的
        vbar_1 = Scrollbar(canvas_sc, orient=VERTICAL)  # 竖直滚动条
        vbar_1.place(x=0, width=2, height=320)
        vbar_1.configure(command=canvas_sc.yview)
        canvas_sc.config(yscrollcommand=vbar_1.set)  # 设置
        canvas_sc.create_window((0, 0), window=frame_1, anchor='nw')  # create_window
        canvas_sc.config(scrollregion=(0, 0, 0, gd_len))
        txt_sc = Text(frame_1,width=600)
        txt_sc.place(x=0,y=0)
        canvas_speed = Canvas(shangc_show,bg = 'white',width=300, height=20,scrollregion=(0, 0, 0, 1100))  # 创建canvas  bg = 'red'
        canvas_speed.place(x=300, y=0)
        sc_yy = Text(canvas_speed,width = 10,height = 2)
        sc_yy.place(x=0,y=0)
        sc_qb = Text(canvas_speed,width = 9,height = 2)
        sc_qb.place(x=150,y=0)
        sc_spd_sc = Text(canvas_speed,width = 11,height = 2)
        sc_spd_sc.place(x=215,y=0)
        butto_sped_q = Button(canvas_speed,bg = 'white',width = 10,height = 1)
        butto_sped_q.place(x=70,y=0)
        butto_sped_y_sc = Button(canvas_speed,bg = 'green',width = 0,height = 1)
        butto_sped_y_sc.place(x=70,y=0)
        butto_sped_y_sc.config(width=0)
def right_zhant():
    with open(right_zt_info,'r') as f:
        info = f.read()
    if '\n' in info:
        info=info.split('\n')[0]
        copy_src = info
        lsbl = txt_lj_t.get()
        lsbl1 = lsbl.split('/')[-1]
        lsbl1 = '/'+lsbl1
        paste_lj_father = lsbl.replace(lsbl1,'')
        paste_lj = paste_lj_father+'/'+copy_src.split('/')[-1]
        # print('paste',paste_lj)
        copy_type='romte-romte'
        url = ym+'khd_copy_pste/' +'?copy_src='+copy_src+'&&paste_lj='+paste_lj
        res = requests.get(url)
        shuax(paste_lj_father,canvas,'no')
        with open(right_zt_info,'w') as f:
            f.write('')
    else:
        copy_type = 'local-romte'
        zt_type =get_zt_lx()
        if zt_type == 'wj':
            wc.OpenClipboard()
            copy_src = wc.GetClipboardData(win32con.CF_HDROP)[0].replace('\\','/')
            wc.CloseClipboard()
            creat_shangc_ck()
            cx=[]
            cx.append(copy_src)
            cx.append(txt_lj_t.get())
            cx.append(ym+'khd_upfe/')
            shangc_t=threading.Thread(target=shangc,args=(cx,))
            shangc_t.start()
            fa_lj = get_fa_lj(txt_lj_t.get(),user_lj)
def right_newfes():
    re_url = ym+'khd_upfe/'
    data={}
    new_lj = txt_lj_t.get()
    new_lj = new_lj.replace('\\','/')
    new_lj = get_fa_lj(new_lj,user_lj)
    data['luj'] = base64_bm(new_lj+'/新建文件夹')
    data['new'] = 'new'
    res = requests.post(re_url,files={},data=data)
    shuax(new_lj,canvas,'no')
from tkinter import filedialog
def right_scfes(te):
    mubiao_dirs = txt_lj_t.get()
    mubiao_dirs = get_fa_lj(mubiao_dirs,user_lj)
    if te == 'fie':
        fe_path = askopenfilename()
    else:
        fe_path = filedialog.askdirectory()
    cx = []
    cx.append(fe_path)
    cx.append(txt_lj_t.get())
    cx.append(ym + 'khd_upfe/')
    creat_shangc_ck()
    shangc_t = threading.Thread(target=shangc, args=(cx,))
    shangc_t.start()
def root_xShowMenu(event):
    a=str(event.widget)
    if 'button' not in a:
        menu = Menu(root, tearoff=0)
        menu.add_command(label="粘贴", command=lambda: right_zhant())
        menu.add_separator()
        menu.add_command(label="新建文件夹", command=lambda: right_newfes())
        menu.add_separator()
        menu.add_command(label="上传文件", command=lambda: right_scfes('fie'))
        menu.add_separator()
        menu.add_command(label="上传文件夹", command=lambda: right_scfes('dirs'))
        menu.add_separator()
        menu.add_command(label="注销", command=lambda: zhuxiao())
        menu.add_separator()
        menu.post(event.x_root, event.y_root)
def zhuxiao():
    if os.path.exists(user_dengl):
        os.remove(user_dengl)
    root.destroy()
    #denglu_zc()
def get_tb_info():
    with open(tongbu_txt,'r',encoding='utf-8') as f:
        info = f.read()
    info = info.split('\n')
    info_all={}
    info_all['romote_lj'] = info[0].split('#')[1]
    info_all['local_lj'] = info[1].split('#')[1]
    info_all['chose'] = info[2].split('#')[1]
    info_all['zt_sc_lj'] = info[3].split('#')[1]
    info_all['ym'] = info[4].split('#')[1]
    return info_all
def tongb_ck():
    def xiug_tb_info():
        romte_lj = '服务器备份路径#'+lab2.get('0.0','end')
        loca_lj = '本地备份路径#'+lab1.get('0.0','end')
        tbxz = '备份选择(a 远端备份至本地 b 本地备份至远端 c 双向备份，只填如 a)#'+lab4.get('0.0', 'end')
        nt_sc = '粘贴上传路径#'+lab3.get('0.0','end')
        fwym = '访问域名#'+lab5.get('0.0', 'end').split('\n')[0]
        info = romte_lj+loca_lj+tbxz+nt_sc+fwym
        with open(tongbu_txt,'w',encoding='utf-8') as f:
            f.write(info)
        tongb_c.destroy()
    def chose_wjj():
        fe_path = filedialog.askdirectory()
        fe_path=fe_path.replace('/','\\')
        lab1.delete('0.0','end')
        lab1.insert('0.0',fe_path)
    tongb_info = get_tb_info()
    tongb_c = Toplevel()
    tongb_c.geometry("700x400+0+0")
    lab1 = Text(tongb_c,height=1)
    lab1.place(x=120,y=50)
    lab1.insert('0.0',tongb_info['local_lj'])
    b1 = Button(tongb_c,text='修改本地同步路径',command=chose_wjj).place(x=0,y=42)
    lab2 = Text(tongb_c,height=1)
    lab2.place(x=120,y=90)
    lab2.insert('0.0',tongb_info['romote_lj'])
    txt2 = Label(tongb_c,text = '小黑云同步路径').place(x=0,y=90)
    lab3 = Text(tongb_c,height=1)
    lab3.place(x=120,y=130)
    lab3.insert('0.0',tongb_info['zt_sc_lj'])
    txt3 = Label(tongb_c,text = '粘贴上传路径').place(x=0,y=130)

    lab4 = Text(tongb_c,height=1)
    lab4.place(x=120,y=170)
    lab4.insert('0.0',tongb_info['chose'])
    txt4 = Label(tongb_c,text = '备份选择').place(x=0,y=170)
    txt4_1 = Label(tongb_c, text='(a 远端备份至本地 b 本地备份至远端 c 双向备份，只填如 a)').place(x=120, y=190)

    lab5 = Text(tongb_c,height=1)
    lab5.place(x=120,y=220)
    lab5.insert('0.0',tongb_info['ym'])
    txt5 = Label(tongb_c,text = '访问域名').place(x=0,y=220)

    but = Button(tongb_c,text='保存设置',command=xiug_tb_info).place(x=120,y=260)
def xiaz_look_a():
    show_xiaz_ck()
    txt_xia.delete('0.0', 'end')
    txt_xia.insert('0.0', shuax_xiaz_txt_info())
def share_ck():
    global share_canvas,txt_lj_share,back_an_share
    share_root = Toplevel()
    share_root.title('小黑云')
    share_root.geometry("800x600+200+0")
    share_canvas = Canvas(share_root, width=800, height=600, scrollregion=(0, 0, 0, 1100))  # 创建canvas
    share_canvas.place(x=50, y=100)  # 放置canvas的位置

    frame_m = Frame(share_root, width=50, height=600, background="#7B7B7B")  # 把frame放在canvas里
    frame_m.place(x=0, y=78)  # frame的长宽，和canvas差不多的
    txt_lj_share = StringVar()
    txt_lj = Label(share_root, textvariable=txt_lj_share, width=106, wraplength=740, foreground="#5CADAD")
    txt_lj.place(x=51, y=78)
    back_an_share = Button(frame_m, command=lambda:back_cz('share'))
    back_an_share.place(x=0, y=0)
    choosepic('bk.jpg', 'back_an_share')
    frame_bt = Frame(share_root, width=800, height=75)  # 把frame放在canvas里
    frame_bt.place(x=0, y=2)  # frame的长宽，和canvas差不多的
    lb1 = Label(frame_bt, text='小 黑 云 文 件 分 享', width=35, height=2, background="#5CADAD", font=('Arial', 30))
    lb1.place(x=0, y=0)
def share_look():
    global share_lj
    url_share=''
    def get_url():
        global share_lj
        url_share=share_url.get()
        re_url=url_share+'&&khd_share=1'
        res = requests.get(re_url).text
        if res == '资源已过期':
            result = tk.messagebox.showinfo(title='信息提示！', message='内容：资源已过期！')
        elif res == '无该资源':
            result = tk.messagebox.showinfo(title='信息提示！', message='内容：无该资源！')
        else:
            share_get.destroy()
            res =eval(res)
            # print(res)
            fa_lj = res['luj']
            share_lj = fa_lj
            if res['pass'] == '**':
                share_ck()
                shuax(fa_lj, share_canvas, 'share')

            elif res['pass'] != '**':
                def pass_get():
                    word = pass_word.get()
                    if word == res['pass']:
                        share_ck()
                        shuax(fa_lj, share_canvas, 'share')
                        get_pass.destroy()
                    else:
                        pass_re.set('密码错误')
                get_pass = Toplevel()
                get_pass.geometry('300x100')
                pass_ti=Label(get_pass,text = '提取密码: ')
                pass_ti.place(x=40,y=10)
                pass_word = Entry(get_pass, width=13)
                pass_word.place(x=100, y=10)
                pass_re = StringVar()
                pass_relb = Label(get_pass, textvariable=pass_re,foreground="#5CADAD")
                pass_relb.place(x=200, y=10)
                bt = Button(get_pass, width=7, text='确定', command=pass_get)
                bt.place(x=100, y=50)
    #share_ck()
    share_get = Toplevel()
    share_get.geometry('500x100')
    share_ti = Label(share_get,text = '分享链接: ')
    share_ti.place(x=40,y=10)
    share_url = Entry(share_get,width=50)
    share_url.place(x=100,y=10)
    share_get_url = Button(share_get,width=20,text='确定',command=get_url)
    share_get_url.place(x=200,y=60)

def denglu_zc():
    global ym,user
    def dengl_z():
        global user
        errMessage=""
        if len(userName.get())==0:
            errMessage=errMessage+"用户名不能为空！\r"
        if len(passWord.get())==0:
            errMessage=errMessage+"密码不能为空！"
        if errMessage!="":
            messagebox.showinfo('提示', errMessage)
        if len(userName.get()) != 0 and len(passWord.get())!=0:
            user = userName.get()
            password = passWord.get()


        # user = txt1.get('0.0','end').split('\n')[0]
        # password = txt2.get('0.0','end').split('\n')[0]
        res = dengl(user,password,ym)
        if res == '1':
            with open(user_dengl, 'wt', encoding='utf-8') as f:
                f.write(user+'#'+password)
            with open(c_info, 'wt', encoding='utf-8') as f:
                info1 = get_computer_info()
                f.write(info1)
            user = user
            dl.destroy()
        else:
            user = '00'
            ts = Label(dl, text='登陆失败',bg = 'red').place(x=150, y=220)
    def zhuc(event):

        errMessage=""
        if len(userName.get())==0:
            errMessage=errMessage+"用户名不能为空！\r"
        if len(passWord.get())==0:
            errMessage=errMessage+"密码不能为空！"
        if errMessage!="":
            messagebox.showinfo('提示', errMessage)
        if len(userName.get()) != 0 and len(passWord.get())!=0:
            user = userName.get()
            password = passWord.get()

        # user = txt1.get('0.0','end').split('\n')[0]
        # # print(user)
        # password = txt2.get('0.0','end').split('\n')[0]
        res = dengl(user,password,ym)
        url_zc = ym+'dlzc/?name='+user+'&&password='+password+'&&zhuce=1'
        res = requests.get(url_zc).text

        if str(type(res))=="<class 'str'>":
            ts = Label(dl, text='注册失败(可能已有该用户)', bg='red').place(x=150, y=220)
        else:
            with open(user_dengl, 'wt', encoding='utf-8') as f:
                f.write(user+'#'+password)
            user = user
            dl.destroy()


    dl = Tk()
    background_color = "white"
    dl.configure(background=background_color)
    dl.title('小黑云登录')
    ft = tkFont.Font(family='Fixdsys', size=30, weight=tkFont.BOLD)
    tk.Label(dl, text="小 黑 云", font=ft, bg=background_color).place(x=100, y=44)
    # 标签 用户名密码 #F3F3F4
    entryBackGroundColor = "#F3F3F4"
    userNameFont = tkFont.Font(family='Fixdsys', size=10)
    tk.Label(dl, text='请输入用户名:', font=userNameFont, bg=background_color).place(x=20, y=150)
    userName = tk.StringVar()
    tk.Entry(dl, highlightthickness=1, bg=entryBackGroundColor, textvariable=userName).place(x=20, y=180,
                                                                                                      width=320,
                                                                                                      height=30)
    passWordFont = tkFont.Font(family='Fixdsys', size=10)
    passWord = tk.StringVar()  #
    tk.Label(dl, text='请输入密码:', font=passWordFont, bg=background_color).place(x=20, y=220)
    tk.Entry(dl, highlightthickness=1, bg=entryBackGroundColor, textvariable=passWord, show='*').place(x=20,y=250,width=320, height=30)
    # remeberMeFont=tkFont.Font(family='Fixdsys', size=12)
    # tk.Checkbutton(self.window, text="记住我",fg="#0081FF",variable="0",font=remeberMeFont, bg=background_color).place(x=20, y=300)
    tk.Button(dl, text='立即登录', font=('Fixdsys', 14, 'bold'), width=29, fg='white', bg="#0081FF",command=dengl_z).place(x=20, y=330)

    regester_info = tkFont.Font(family='Fixdsys', size=10)
    tk.Label(dl, text='还没有账号？:', font=regester_info, bg=background_color).place(x=102, y=375)
    link = tk.Label(dl, text='立即注册', font=regester_info, bg=background_color, fg="#FFA500")
    link.bind("<1>",zhuc)
    link.place(x=185, y=375)
    w = 370
    h = 480
    sw = dl.winfo_screenwidth()
    # 得到屏幕宽度
    sh = dl.winfo_screenheight()
    # 得到屏幕高度
    # 窗口宽高为100
    x = (sw - w) / 2
    y = (sh - h) / 2
    dl.geometry("%dx%d+%d+%d" % (w, h, x, y))







    # dl.geometry('400x300')
    # txt1 = Text(dl,height=1,width=20)
    # txt1.place(x=130,y=100)
    # txt1.insert('0.0','用户名')
    #
    # txt2 = Text(dl,height=1,width=20)
    # txt2.place(x=130,y=150)
    # txt2.insert('0.0','密码')
    #
    #
    # qr = Button(dl,text='登 录',width=7,command=dengl_z).place(x=130,y=180)
    # zc = Button(dl, text='注 册', width=7,command=zhuc).place(x=215, y=180)
    dl.mainloop()


def disk_scan(luj):
    def chose_mo_lj():
        fe_path = filedialog.askdirectory()
        Txt.delete('0.0','end')
        Txt.insert('0.0',fe_path)
        with open(moren_lj,'wt',encoding='utf-8') as f:
            f.write(fe_path)
    url = ym+'get_size/?luj='+luj
    res = requests.get(url).text
    res = eval(res)
    yy  = res['size']
    zg = res['sum_size']

    yy_fm = get_size(yy)
    zg_fm =get_size(zg)

    yy_b = yy*360/zg
    windows = Toplevel()
    windows.geometry('400x350')
    windows.title("硬盘容量")
    canvas_bt = Canvas(windows, height=300, width=300)
    canvas_bt.place(x=0,y=0)
    # 利用画布的create_arc画饼形，(400,400)和(100,100)为饼形外围的矩形,
    # start=角度起始，extent=旋转的度数，fill=填充的颜色
    canvas_bt.create_arc(200, 200, 10, 10, start=0, extent=yy_b, fill="green")
    canvas_bt.create_arc(200, 200, 10, 10, start=yy_b, extent=360-yy_b, fill="white")

    canvas_bt.create_text(250, 30, text=yy_fm, font=("华文新魏", 20))
    canvas_bt.create_text(100, 230, text=zg_fm, font=("华文新魏", 20))
    #
    # frame_m = Frame(root,width=50,height=600,background="#7B7B7B")  # 把frame放在canvas里
    # frame_m.place(x=0,y=78)  # frame的长宽，和canvas差不多的
    Txt = Text(windows,height=1)
    Txt.place(x=0,y=300)
    with open(moren_lj, 'r', encoding='utf-8') as f:
        lj = f.read()
    Txt.insert('0.0',lj)
    but = Button(windows,text = '选择默认本地路径',command=chose_mo_lj).place(x=0,y=320)






user = '00'
user_dengl='user_dengl.txt'
c_info='c_info.txt'
moren_xiaz_lj = os.getcwd().split('\\')[0]+'/小黑云下载'
xiaz_info = 'xiaz_info.txt'
xiaz_fh = 'xiaz_fh.txt'


def clean_xia_info():
    if os.path.exists(xiaz_fh):
        with open(xiaz_fh, 'w') as f:
            f.write('')
    if os.path.exists(xiaz_info):
        with open(xiaz_info, 'w') as f:
            f.write('')

# if os.path.isdir(moren_xiaz_lj):
#     pass
# else:
#     try:
#         print('105',moren_xiaz_lj)
#         os.mkdir(moren_xiaz_lj)
#         clean_xia_info()
#     except:
#         pass


if os.path.exists(user_dengl) and os.path.exists(c_info):
    with open(c_info,'r',encoding='utf-8') as f:
        info_c=f.read()
    if info_c == get_computer_info():
        with open(user_dengl,'r',encoding='utf-8') as f:
            info=f.read()
        name = info.split('#')[0]
        password = info.split('#')[1]
        res = dengl(name, password, ym)
        if res == '1':
            user = name
            pass
        else:
            clean_xia_info()
            denglu_zc()
    else:
        clean_xia_info()
        denglu_zc()
else:
    clean_xia_info()

    denglu_zc()



if khd_v_judge() == '0':
    root = tk.Tk()
    root.withdraw()
    erro=tk.messagebox.showinfo('小黑云错误提示','由于有些地方做了更新，无法支持当前版本，需更新')
    user='00'
    if erro == 'ok':
        root.destroy()
    root.mainloop()

if user !='00':
    lj='w.jpg'
    leg=16
    if user =='z':
        user_lj ='D:/self'
    else:
        user_lj = 'D:/other_user/'+user
    luj=user_lj

    user_id = requests.get(ym+'get_user_info/?user='+user).text

    moren_xiaz_lj = os.getcwd().split('\\')[0]+'/小黑云下载'
    if os.path.exists(moren_lj):
        with open(moren_lj,'r',encoding='utf-8') as f:
            moren_xiaz_lj=f.read()
        if '/' in moren_xiaz_lj or '\\' in moren_xiaz_lj:
            print('101',moren_xiaz_lj)
            if os.path.isdir(moren_xiaz_lj):
                pass
            else:
                try:
                    print('102', moren_xiaz_lj)
                    os.mkdir(moren_xiaz_lj)
                except:
                    print('103', moren_xiaz_lj)
                    moren_xiaz_lj = os.getcwd().split('\\')[0] + '/小黑云下载'
                    if not os.path.isdir(moren_xiaz_lj):
                        os.mkdir(moren_xiaz_lj)
        else:
            with open(moren_lj, 'wt', encoding='utf-8') as w:
                w.write(moren_xiaz_lj)
    else:
        with open(moren_lj, 'wt', encoding='utf-8') as w:
            w.write(moren_xiaz_lj)
    right_zt_info='right_zt_info.txt'
    tongbu_txt = 'auto_up.txt'


    root = tk.Tk()
    root.title('小黑云')
    root.geometry("800x600+200+0")
    root.resizable(0,0)
    canvas=Canvas(root,width=800,height=600,scrollregion=(0,0,0,1100)) #创建canvas
    canvas.place(x = 50, y = 100) #放置canvas的位置
    frame_m = Frame(root,width=50,height=600,background="#7B7B7B")  # 把frame放在canvas里
    frame_m.place(x=0,y=78)  # frame的长宽，和canvas差不多的
    txt_lj_t=StringVar()
    txt_lj = Label(root, textvariable=txt_lj_t, width=106, wraplength = 740,foreground="#5CADAD")
    txt_lj.place(x = 51, y = 78)
    back_an= Button(frame_m,command=lambda:back_cz('no'))
    back_an.place(x = 0, y = 0)
    choosepic('bk.jpg','back_an')
    share_an= Button(frame_m,command=share_look)
    share_an.place(x = 0, y = 110)
    choosepic('share.jpg','share_an')
    xiaz_look= Button(frame_m,command=xiaz_look_a)
    xiaz_look.place(x = 0, y = 450)
    choosepic('xiaz1.jpg','xiaz_look')

    def TB():
        ccs=[]
        ccs.append(ym)
        ccs.append(user)
        tb = threading.Thread(target=tongbu,args=(ccs,))
        tb.setDaemon(True)
        tb.start()
    TB()

    tongb= Button(frame_m,command=tongb_ck)
    tongb.place(x = 0, y = 220)
    choosepic('tb1.jpg','tongb')

    yp= Button(frame_m,command=lambda:disk_scan(luj))
    yp.place(x = 0, y = 330)
    choosepic('yp.jpg','yp')


    frame_bt = Frame(root,width=800,height=75)  # 把frame放在canvas里
    frame_bt.place(x=0,y=2)  # frame的长宽，和canvas差不多的
    lb1 = Label(frame_bt,text ='小 黑 云',width =35,height = 2,background="#5CADAD",font=('Arial', 30))
    lb1.place(x=0,y=0)

    lb2 = Label(frame_bt)
    lb2.place(x=0,y=0)
    choosepic('xhy.jpg','lb2')




    wenjlst=os.listdir('D:/')
    gd_len = (int(len(wenjlst)/1)+1)*100
    print(len(wenjlst),gd_len)

    #frame=creat_fram(gd_len)
    shuax(luj,canvas,'no')
    root.bind("<MouseWheel>", processWheel)
    root.bind("<Button-3>", root_xShowMenu)
    # frame.bind("<Enter>", mouse_move)
    #root.bind("<Enter>", frm_mouse_move)

    root.mainloop()


