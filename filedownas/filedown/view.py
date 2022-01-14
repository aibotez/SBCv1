from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse,FileResponse
from urllib import parse
import shutil,json,np,io
import socket,os,time,threading
import ffmpeg,base64
from ffmpy3 import FFmpeg
from PIL import Image

path=os.getcwd().replace('\\','/')
path=path+'/user/user.txt'
user_info=path
ym='http://zhenz.club'
#ym='http://127.0.0.1:9500'
lj_suos='self'
lj_guest='D:/other_user/'



wenj_all={}
files=[]
file_l=[]
wenj_all['name']=[]
wenj_all['luj']=[]
wenj_all['pf']=[]


wenj_all_zl=wenj_all
user={'ss':[],'cs':[]}
resous=''
ss=0
dl_cishu=0
dl_cs_max=3
page=0
admin='z'
files=[]
curt_lj=''
zh=''

def get_video_frm(lj):
    cap=cv2.VideoCapture(lj)
    succes, data = cap.read()
    succes, data = cap.read()
    if succes:
        im = Image.fromarray(data)
        output_buffer = io.BytesIO()
        im.save(output_buffer, format='JPEG')
        binary_data = output_buffer.getvalue()
        base64_data = base64.b64encode(binary_data).decode()
        #return base64_data
        cap.release()
        return 'data:image/png;base64,'+base64_data
def xiug(fe,fgf,biaos,dijigg,gaiwei):
    with open(fe,'r') as f:
        info=f.read()
    info=info.split('\n')
    del info[-1]
    pd='0'
    ggxx=[]
    lsc=''
    ls=0
    for i in info:
        j=i.split(fgf)
        ls=0
        lsc=''
        for s in j:
            ls=ls+1
            idx=j.index(s)
            if s == biaos and idx == 1:
                if j[dijigg] != gaiwei:
                    j[dijigg]=gaiwei
                    pd='1'
            if ls == len(j):
                lsc = lsc + j[idx]
            else:
                lsc=lsc+ j[idx]+fgf
        lsc=lsc+'\n'
        ggxx.append(lsc)
    if pd == '1':
        with open(fe,'w') as f:
            for i in ggxx:
                f.write(i)

#xiug(user_info,'#','z',4,'0')

def scansize(id):
    username=get_cur_username(id)
    lj=[]
    yyrl=0
    if username == admin:
        disk = (os.popen('fsutil fsinfo drives').read()).split()[1:]
        for i in disk:
            lj.append(i+lj_suos)
    else:
        lj.append('D:/nas/others/'+username)
    for i in lj:
        try:
            yyrl=yyrl+getdirsize(i)
        except Exception as e:
            print(e)

    xiug(user_info, '#', username, 4, str(yyrl))
    return yyrl

def get_cur_username(id):
    req_user_id=id.split('.')[0]
    all_user=check_user()
    loca_user_id=all_user['user_id']
    cur_name=all_user['user_name'][loca_user_id.index(req_user_id)]
    return cur_name
t_check_rl = threading.Thread(target=scansize)
def startT(id):
    global t_check_rl
    #t_check_rl = threading.Thread(target=scansize, args=(id,))
    if t_check_rl.is_alive():
        pass
    else:
        t_check_rl = threading.Thread(target=scansize, args=(id,))
        t_check_rl.start()


def shouye(request):
    global user,files
    #files=[]
    value = request.COOKIES
    if 'cur_id' in value.keys():
        startT(value['cur_id'])
    if 'cur_id' in value.keys():
        #scansize(value['cur_id'])
        ss= value['cur_id'].split('.')[0]
        if ss in user['ss']:
            idx = user['ss'].index(ss)


            if user['cs'][idx] >= 20:
                user['cs'][idx]=1
            else:
                user['cs'][idx] = user['cs'][idx] + 1


        else:
            user['ss'].append(ss)
            user['cs'].append(1)
        return HttpResponseRedirect('/start/')
    else:
        return render(request, "dlzc.html")

def check_file(luj):
    wjname=[]
    try:
        lujing = os.listdir(luj)
        for j in lujing:
            wjname.append(j)
    except Exception as e:
        print('NULL', e)
    return wjname


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


def getFileFolderSize(fileOrFolderPath):
    """get size for file or folder"""
    totalSize = 0

    if not os.path.exists(fileOrFolderPath):
        return totalSize

    if os.path.isfile(fileOrFolderPath):
        totalSize = os.path.getsize(fileOrFolderPath)  # 5041481
        return totalSize

    if os.path.isdir(fileOrFolderPath):
        with os.scandir(fileOrFolderPath) as dirEntryList:
            for curSubEntry in dirEntryList:
                curSubEntryFullPath = os.path.join(fileOrFolderPath, curSubEntry.name)
                if curSubEntry.is_dir():
                    curSubFolderSize = getFileFolderSize(curSubEntryFullPath)  # 5800007
                    totalSize += curSubFolderSize
                elif curSubEntry.is_file():
                    curSubFileSize = os.path.getsize(curSubEntryFullPath)  # 1891
                    totalSize += curSubFileSize

            return totalSize
#
# userFolder = "D:/cc"
# userFolderSize = getFileFolderSize(userFolder)
# print("userFolderSize=%s" % userFolderSize)


def getdirsize(dir):
   size = 0
   size = 0.0
   for root, dirs, files in os.walk(dir):
       size += sum([os.path.getsize(os.path.join(root, file)) for file in files])
   size = round(size / 1024 / 1024 / 1024, 2)
   return size
#print('rrrrrr',getdirsize('D:/'))
def get_user_rl(name):
    user_infoo=check_user()
    user_name=user_infoo['user_name']
    user_zgye=user_infoo['user_zgye']
    user_yyye = user_infoo['user_yyye']
    idx=user_name.index(name)
    zgye=user_zgye[idx]
    if zgye =='00':
        zgye = 1024
    yyye=user_yyye[idx]
    u_rl=[]
    u_rl.append(zgye)
    u_rl.append(yyye)
    return u_rl




def dengl(user_name, user_password):
    global name

    pass_user='用户名错误'
    if len(user_name) >= 1 and len(user_password) == 0:
        pass_user = '密码错误(密码不能为空)'
    # elif len(user_name) == 1 and len(user_password) == 0:
    #     pass_user = '无效用户名'
    elif len(user_name) > 0 and len(user_password) > 0:
        if user_name + '#' + user_password in check_user()['user_name_pass']:
            pass_user = '1'
            name=user_name
        else:
            pass_user = '密码错误'
    # print(f,s)
    # return render(request, "dlzc.html")
    return pass_user
def zhuce(user_name, user_password):
    zc_re='用户名不得为空'
    user_all = check_user()
    if len(user_name) >= 1 and len(user_password) == 0:
        zc_re='密码不能为空'
    # elif len(user_name) == 1 and len(user_password) == 0:
    #     zc_re='用户名或密码不符合规范'
    elif len(user_name) > 0 and len(user_password) > 0 :
        user_name_all=user_all['user_name']
        user_id=user_all['user_id'][-1]
        new_user_id=int(user_id)+1
        zc_re=''
        for i in user_info:
            user_name_all.append(i.split(' ')[0])
        if user_name in user_name_all:
            zc_re='已存在该用户，请更换用户名'
            #return HttpResponse("no succ!")
        else:
            with open(user_info,'a') as f:
                f.write(str(new_user_id)+'#'+user_name+'#'+user_password+'#'+'100'+'#'+'0'+'\n')
            zc_re='1'
            new_lj=lj_guest+'/'+user_name
            if os.path.exists(new_lj):
                pass
            else:
                try:
                    os.makedirs(new_lj)
                    shutil.copy('static/小黑云客户端.7z',new_lj+'/小黑云客户端.7z')
                    shutil.copy('static/小黑云说明.pdf', new_lj + '/小黑云说明.pdf')
                    #os.mknod(new_lj+'/'+user_name+'.hnet')
                    # with open(new_lj+'/'+user_name+'.hnet', 'w') as f:
                    #     pass
                    # #with open()
                except Exception as e:
                    print(e)
    return zc_re



def dlzc(request):
    global ss
    text = request.GET
    user_name = text['name']
    # idx=check_user()['user_name'].index(user_name)
    # ss=check_user()['user_id'][idx]
    user_password = text['password']
    if 'dengl' in text:
        idx = check_user()['user_name'].index(user_name)
        ss = check_user()['user_id'][idx]
        passuser = dengl(user_name, user_password)
        # if passuser == '0':
        #     return HttpResponse("dl no succ!")
        if passuser == '1':
            if ss in user['ss']:
                idx = user['ss'].index(ss)
                user['cs'][idx] = user['cs'][idx] + 1
            else:
                user['ss'].append(ss)
                user['cs'].append(1)
            #startT(ss + '.1.1')
            #startT(ss + '.1.1')
            return HttpResponseRedirect('/start/')
            # return render(request, "fehome.html")
            # return HttpResponse("dl succ!")
        else:
            return HttpResponse(passuser)
    elif 'zhuce' in text:
        zc_re = zhuce(user_name, user_password)
        # if zc_re == '0':
        #     return HttpResponse("zc no succ!")
        # elif zc_re == '2':
        #     return HttpResponse("用户名或密码不符合规范")
        if zc_re == '1':
            userinfo = check_user()
            ss = userinfo['user_id'][-1]
            user['ss'].append(ss)
            user['cs'].append(1)
            #startT(ss+'.1.1')
            return HttpResponseRedirect('/start/')
        else:
            return HttpResponse(zc_re)

def get_father_lj(id):
    global files
    lj_list=[]
    clj=[]
    use=[]
    for i in files:
        use.append(i['id'])
        clj.append(i['curt_lj'])
    idx=use.index(id)
    return clj[idx]
def del_lj_kg(lj_lst,fa_lj):
    for i in lj_lst:
        loca_lj = fa_lj+'/'+i
        if ' ' in i :
            del_kg_ne=i.replace(' ','.')
            del_kg_lj=fa_lj+'/'+del_kg_ne
            os.rename(loca_lj,del_kg_lj)
            lj_lst[lj_lst.index(i)]=del_kg_ne
    return lj_lst
name=''
def ho(request):
    global user_agent
    global ss,files
    global page
    global files,file_l
    global resous,name
    global dl_cishu
    global user,lj_suos
    global wenj_all


    lj0=[]
    lj1=''

    value = request.COOKIES
    if 'cur_id' in value.keys():
        ss= value['cur_id'].split('.')[0]
        name=get_cur_username(value['cur_id'])
    else:
        name = get_cur_username(ss + '.1.1.1')
    if ss == '1':
        disk = (os.popen('fsutil fsinfo drives').read()).split()[1:]
        lj0=disk
        lj1=lj_suos
    else:
        lj0=[]
        lj0.append(lj_guest)
        #lj0=[lj_guest]
        lj1=name
    #disk = (os.popen('fsutil fsinfo drives').read()).split()[1:]
    lujing = []
    wenj_all={}
    #files=[]
    wenj_all['name'] = []
    wenj_all['luj'] = []
    wenj_all['pf'] = []
    for i in lj0:
        i=i.replace('\\','/')
        try:
            lujing = os.listdir(i + lj1)
            lujing=del_lj_kg(lujing,i + lj1)

            for j in lujing:
                wenj_all['name'].append(j)
                wenj_all['luj'].append(i + lj1 + '/' + j)
                wenj_all['pf'].append(i)
        except Exception as e:
            print('NULL', e)

    resous = 'yes'
    # userinfo=check_user()
    # user_agent= userinfo['user_agent']
    # agent = request.META['HTTP_USER_AGENT']
    # ss = userinfo['user_id'][user_agent.index(agent)]
    page =0
    idx = user['ss'].index(ss)
    dl_cishu=user['cs'][idx]

    file_l = []
    for i in wenj_all['name']:
        file = {}
        file['id'] = str(ss) + '.' + str(dl_cishu) + '.' + str(page) + '.' + str(wenj_all['name'].index(i))
        file['name'] = i
        file['luj'] = wenj_all['luj'][wenj_all['name'].index(i)]
        if os.path.isdir(wenj_all['luj'][wenj_all['name'].index(i)]):
            file['wjtb'] = '/static/images/w.jfif'
        else:
            file['wjtb'] = '/static/images/wj.jfif'
        ljj = file['luj'].split('/')
        ljj1 = ''
        del ljj[-1]
        for s in ljj:
            if s != ljj[-1]:
                ljj1 = ljj1 + s + '/'
            else:
                ljj1 = ljj1 + s
        file['curt_lj'] = ljj1
        try:
            file['pf'] = wenj_all['pf'][wenj_all['name'].index(i)]
        except:
            pass
        files.append(file)

        file_l.append(file)


    return HttpResponseRedirect('/s')


def ct(request):
    global ss
    global files
    global file_l
    global resous
    global curt_lj

    user_request_info = request.META
    if 'HTTP_X_FORWARDED_FOR' in user_request_info.keys():
        user_real_ip = user_request_info['HTTP_X_FORWARDED_FOR']
    else:
        user_real_ip = user_request_info['REMOTE_ADDR']
    #print(request.META)
    print(user_real_ip)
    if resous != 'yes':
        resous = 'no'
        value = request.COOKIES
        print('idididid',value)
        if 'cur_id' in value.keys() and value['cur_id'].split('.')[2] != '0':
            father_lj=get_father_lj(value['cur_id'])
            shuaxin(father_lj,value['cur_id'])
            resous = 'yes'
            return HttpResponseRedirect('/s')
        else:
            return HttpResponseRedirect('/')
    else:

        files1=[]
        for i in files:
            if i not in files1:
                files1.append(i)
        files=[]
        files=files1
        file_all=file_l
        bkbl=file_l[0]['id']
        print('id',bkbl)
        zh = get_cur_username(bkbl)
        lj=file_l[0]['curt_lj']
        resous = 'no'
        rl=get_user_rl(zh)
        rl_view=float(rl[1])*130/float(rl[0])
        rl_view = str(rl_view)

        return render(request,"1.html",locals())

def get_fie_lx(lj):
    lj1=lj.lower()
    if '.jpg' in lj1 or '.png' in lj1 or '.bmp' in lj1 or '.jpeg' in lj1:
        return 'tp'
    elif '.doc' in lj1 or 'docx' in lj1 or 'pptx' in lj1 or 'ppt' in lj1 or 'xlsx' in lj1:
        return 'pdf_z'
    elif '.pdf' in lj1:
        return 'pdf'
    elif '.mp4' in lj1 or '.webm' in lj1 or '.ogg' in lj1 or '.avi' in lj1 or 'rmvp' in lj1 or '3jp' in lj1 or 'mpg' in lj1:
        return 'video'
    elif '.html' in lj1:
        return 'html'
    elif '.txt' in lj1:
        return 'txt'
def txt2html(txtlj,htmlji):
    cont = ''
    with open(txtlj, "r", encoding='utf-8') as f:
        cont = f.read()
    cont1 = cont.replace('<', "'<'").replace('\n', '<br>').replace(' ', '&nbsp').replace('\t', '&emsp;')

    with open(htmlji, "w", encoding='utf-8') as f:
        f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'+'\n')
        f.write(cont1)
def get_wb(lj):
    pass
from win32com.client import gencache
from win32com.client import constants, gencache
import pythoncom
from win32com import client
def createpdf(wordPath, pdfPath):
    pythoncom.CoInitialize()
    """
    word转pdf
    :param wordPath: word文件路径
    :param pdfPath:  生成pdf文件路径
    """
    lj = wordPath.lower()
    if '.pptx' in lj or '.ppt' in lj:
        p = client.Dispatch("PowerPoint.Application")
        ppt = p.Presentations.Open(wordPath, False, False, False)
        ppt.ExportAsFixedFormat(pdfPath, 2, PrintRange=None)
        p.Quit()
    elif '.xlsx' in lj:
        xlApp = client.Dispatch("Excel.Application")
        books = xlApp.Workbooks.Open(wordPath,ReadOnly=1)
        books.ExportAsFixedFormat(0, pdfPath)
        xlApp.Quit()
    else:
        w = client.Dispatch("Word.Application")
        doc = w.Documents.Open(wordPath,ReadOnly=1)
        doc.ExportAsFixedFormat(pdfPath, client.constants.wdExportFormatPDF)
        w.Quit()
        # word = gencache.EnsureDispatch("Word.Application")
        # doc = word.Documents.Open(wordPath, ReadOnly=1)
        # doc.ExportAsFixedFormat(pdfPath,
        #                         constants.wdExportFormatPDF,
        #                         Item=constants.wdExportDocumentWithMarkup,
        #                         CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
        # word.Quit(constants.wdDoNotSaveChanges)
#createpdf('D:/self/123.docx', '/static/zhongz/1.pdf')
#createpdf('D:/self/123.docx', 'D:/filedownas/templates/zhongz/1.pdf')
def moov_tq(cllj,cllj_aft,cllj_th):
    if os.path.exists(cllj_aft):
        os.remove(cllj_aft)
    ff = FFmpeg(inputs={cllj: None}, outputs={cllj_aft: ' -movflags faststart -acodec copy -vcodec copy'}).run()
    os.remove(cllj)
    os.rename(cllj_aft,cllj_th)
def zm():
    global th_chuanc
    cz=th_chuanc
    #print('czcz',cz)
    while len(cz) >=1 :
        #print('11111111111')
        cl=cz[0]
        clzm=cl[0]
        cllj=cl[1]
        cllj_aft=cl[2]
        cllj_th = cl[3]

        if os.path.exists(cllj_aft):
            os.remove(cllj_aft)
        ff = FFmpeg(inputs={cllj: None},outputs={cllj_aft: '-vcodec h264 -acodec aac -strict -2'}).run()
        #print(ff.cmd)
        #ff.run()
        #a=os.system(clzm)
        time.sleep(1)
        #os.system("rd/s/q  "+cllj)
        #print(cllj[-4:])
        os.remove(cllj)
        time.sleep(1)
        os.rename(cllj_aft, cllj_th)
        #ff = FFmpeg(inputs={cllj_aft: None}, outputs={cllj_th: ' -movflags faststart -acodec copy -vcodec copy'}).run()
        time.sleep(1)
        #os.remove(cllj_aft)
        del th_chuanc[0]
        cz = th_chuanc
    #print('czcz', cz)

zm_t=threading.Thread(target=zm)
th_chuanc=[]
def xhy_web_video_bf(path):

    #path = request.GET['lj']
    #print(path,'pathhhhh')
    def file_iterat(chunk_size=2 * 1024 * 1024):
        with open(path, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    content_type = 'video/mp4'
    size = os.path.getsize(path)
    resp = StreamingHttpResponse(file_iterat(chunk_size=2 * 1024 * 1024), content_type=content_type)
        #resp = StreamingHttpResponse(file_iterat(path))
    resp['Content-Length'] = str(size)
    #resp['Content-Type'] = 'application/x-mpegURL'
    resp['Accept-Ranges'] = 'bytes'
    return resp

def xiaz(request,id):
    global page
    global files
    global file_l
    global resous,zm_t,th_chuanc
    global curt_lj

    delafter_page(id, 'aft')
    value = request.COOKIES["cur_id"]
    id_info=id.split('.')
    curt_page=id_info[2]
    curt_use=id_info[0]
    curt_cs=id_info[1]
    resous = 'yes'
    file_l=[]
    felj=''
    for i in files:
        if id == i['id']:
            fename=i['name']
            felj=i['luj']
            fej_fa=i['curt_lj']
    curt_lj=felj
    if os.path.isdir(felj):
        page=int(curt_page)+1
        try:
            lujing = os.listdir(felj)
            lujing = del_lj_kg(lujing,felj)
            if len(lujing)<1:
                lujing=['无文件夹']
            for j in lujing:
                file = {}
                file['id'] = curt_use + '.'+curt_cs+'.' + str(page) + '.' + str(lujing.index(j))
                file['name'] = j
                file['luj'] = felj+'/'+j
                file['curt_lj']=felj
                if os.path.isdir(felj+'/'+j):
                    file['wjtb'] = '/static/images/w.jfif'
                else:
                    file['wjtb'] = '/static/images/wj.jfif'
                files.append(file)
                file_l.append(file)
            file_all = files
        except:
            pass
        return HttpResponseRedirect('/s')
    else:
        resous = 'no'
        fe_lx=get_fie_lx(felj)
        if fe_lx == 'tp':
            d = os.path.dirname(__file__)
            imagepath = os.path.join(d, felj)
            image_data = open(imagepath, "rb").read()
            return HttpResponse(image_data, content_type="image/png")  # 注意旧版的资料使用mimetype,现在已经改为content_type
        elif fe_lx == 'pdf_z':
            lj=os.getcwd()
            lj=lj.replace('\\','/')
            lj=lj+'/static/zhongz/'+curt_use+'.pdf'
            gaih_fe=lj
            gaih_fe1='/static/zhongz/'+curt_use+'.pdf'
            if os.path.exists(gaih_fe):
                os.remove(gaih_fe)
            createpdf(felj, gaih_fe)
            reurl = "/static/js/pdf.js/web/viewer.html?file=" + gaih_fe1
            return HttpResponseRedirect(reurl)
            #return render(request, "show_pdf.html", locals())
        elif fe_lx == 'txt':
            lj=os.getcwd()
            lj=lj.replace('\\','/')
            lj=lj+'/static/zhongz/'+curt_use+'.html'
            gaih_fe=lj
            gaih_fe1='/static/zhongz/'+curt_use+'.html'
            if os.path.exists(gaih_fe):
                os.remove(gaih_fe)
            txt2html(felj, gaih_fe)
            return HttpResponseRedirect(gaih_fe1)


        elif fe_lx == 'pdf':
            gaih_fe1=curt_lj[3:]
            gaih_fe1='/static/'+gaih_fe1
            # shutil.copyfile(felj,'static/zhongz/'+curt_use+'.pdf')
            # gaih_fe1 = '/static/zhongz/'+curt_use+'.pdf'
            #url="/static/js/pdf.js/web/viewer.html?file=/static/zhongz/1.pdf"
            reurl="/static/js/pdf.js/web/viewer.html?file="+gaih_fe1
            return HttpResponseRedirect(reurl)
        elif fe_lx == 'video':
            gaih_fe=curt_lj[3:]
            gaih_fe1='/static/'+gaih_fe
            print(curt_lj)
            info = ffmpeg.probe(curt_lj)['streams'][0]['codec_name']
            info=str(info)
            info=info.lower()
            fename_aft=fename.split('.')
            fename_aft=fename_aft[-1]
            fename_aft=fename.replace(fename_aft,'mp4')


            zm_aft=fej_fa+'/zm_'+fename_aft
            zm_th=fej_fa+'/'+fename_aft
            # spsz=curt_lj+'.jpg'
            # rehtspsz=gaih_fe1+'.jpg'
            wjl=os.listdir(fej_fa)
            # if fename+'.jpg' in wjl:
            #     pass
            # else:
            #     ff = FFmpeg(inputs={curt_lj: None}, outputs={spsz: '-y -f mjpeg -ss 0 -t 1'}).run()
            if info == 'h264' or info == 'vp8' or info == 'theora':
                #moov_tq(curt_lj, zm_aft, zm_th)
                # if '.mp4' == curt_lj[-4:]:
                #     moov_tq(curt_lj, zm_aft,zm_th)
                #rehtspsz=get_video_frm(curt_lj)
                #print(rehtspsz)
                cur_url = request.META['HTTP_HOST']
                cur_url = 'http://' + cur_url + '/'
                bf_url = cur_url + 'xhy_web_video_bf/?lj=' + curt_lj
                return xhy_web_video_bf(curt_lj)
                return render(request, "show_video.html", locals())
            else:
                if zm_t.isAlive():
                    thcc=[]
                    cz='ffmpeg -i ' + curt_lj + ' -vcodec h264 -acodec aac -strict -2 '+zm_aft
                    thcc.append(cz)
                    thcc.append(curt_lj)
                    thcc.append(zm_aft)
                    thcc.append(zm_th)
                    if thcc in th_chuanc:
                        idx = th_chuanc.index(thcc)
                    else:
                        th_chuanc.append(thcc)
                        idx=th_chuanc.index(thcc)

                    return HttpResponse('此视频非网页可播放视频，已加载到转换为网页支持的编码任务的排队中,当前序列为： '+str(idx+1))
                else:
                    thcc=[]
                    cz='ffmpeg -i ' + curt_lj + ' -vcodec h264 -acodec aac -strict -2 '+zm_aft
                    thcc.append(cz)
                    thcc.append(curt_lj)
                    thcc.append(zm_aft)
                    thcc.append(zm_th)
                    if thcc in th_chuanc:
                        pass
                    else:
                        th_chuanc.append(thcc)
                    zm_t = threading.Thread(target=zm)
                    zm_t.start()
                    #os.popen('ffmpeg -i ' + curt_lj + ' -vcodec h264 -acodec aac -strict -2 '+zm_aft)
                return HttpResponse('此视频非网页可播放视频，视频正在转换为网页支持的编码，可能需要几分钟（由视频大小决定）')



            #os.popen('ffmpeg -i '+gaih_fe1+' -vcodec h264 -acodec aac -strict -2 h264.mp4')
        elif fe_lx == 'html':
            gaih_fe1=curt_lj[3:]
            gaih_fe1=gaih_fe1

            return render(request, gaih_fe1)

        return HttpResponse(felj+'....'+id)

def delafter_page(id,aft_or_per):
    global files
    id_info=id.split('.')
    curt_page=id_info[2]
    curt_use=id_info[0]
    curt_cs=id_info[1]
    del_pag=0
    id_pag=int(curt_page)
    id_curt = curt_use + '.' + curt_cs + '.' + str(id_pag)
    if aft_or_per == 'aft':
        del_pag=id_pag+1
    elif aft_or_per == 'per':
        del_pag = id_pag - 1
    elif aft_or_per == 'cur':
        del_pag = id_pag
    id_cut=curt_use+'.'+curt_cs+'.'+str(del_pag)
    del_lst=[]
    for i in files:
        #print(i)
        ids=i['id']
        ids_info = ids.split('.')
        cho_page = ids_info[2]
        cho_use = ids_info[0]
        cho_cs = ids_info[1]
        if id_cut == cho_use+'.'+cho_cs+'.'+cho_page:
            #files.remove(i)
            del_lst.append(files.index(i))
    filess=[]
    for i in range(len(files)):
        if i not in del_lst:
            filess.append(files[i])
    files=[]
    files=filess


def per_page(request):
    global file_l
    global resous
    resous = 'yes'
    text = request.GET
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

    delafter_page(id,'cur')
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

def shuaxin(luj,id):
    #print('shax id',id)

    global files,file_l
    shuaxin_fie=[]
    file_l=[]
    cur_wj_name_list=check_file(luj)
    id_info=id.split('.')
    curt_page=id_info[2]
    curt_use=id_info[0]
    curt_cs=id_info[1]
    id_pag=int(curt_page)
    id_sx = curt_use + '.' + curt_cs + '.' + str(id_pag)
    fie_sx=[]


    for i in files:
        #print(i)
        ids=i['id']
        ids_info = ids.split('.')
        cho_page = ids_info[2]
        cho_use = ids_info[0]
        cho_cs = ids_info[1]
        #print(i,id_sx,cho_use+'.'+cho_cs+'.'+cho_page)
        if id_sx == cho_use+'.'+cho_cs+'.'+cho_page:
            #print(i)
            fie_sx.append(i)
    # if id.split('.')[2] == '0':
    #     for  i in files:
    #
    #     files=[]
    # else:
    delafter_page(id, 'cur')
    old_fename_list=[]
    for i in fie_sx:
        old_fename_list.append(i['name'])

    if len(cur_wj_name_list) == len(old_fename_list):

        for i in fie_sx:
            if i['name'] not in cur_wj_name_list:
                for s in range(len(fie_sx)):
                    fie_sx[s]['name']=cur_wj_name_list[s]
                    fie_sx[s]['luj'] = luj+'/'+cur_wj_name_list[s]
                    if os.path.isdir(luj+'/'+cur_wj_name_list[s]):
                        fie_sx[s]['wjtb'] = '/static/images/w.jfif'
                    else:
                        fie_sx[s]['wjtb'] = '/static/images/wj.jfif'



    elif len(cur_wj_name_list) > len(fie_sx):
        new_fename=''
        for i in cur_wj_name_list:
            if i not in old_fename_list:
                new_fename=i
        new_dct={}
        new_dct['id'] = id_sx+'.'+str(len(fie_sx))
        new_dct['name'] = new_fename
        new_dct['luj'] = luj+'/'+new_fename
        new_dct['curt_lj'] = luj
        if os.path.isdir(luj+'/'+new_fename):
            new_dct['wjtb'] = '/static/images/w.jfif'
        else:
            new_dct['wjtb'] = '/static/images/wj.jfif'
        fie_sx.append(new_dct)

    elif len(cur_wj_name_list) < len(fie_sx):
        for i in old_fename_list:
            if i not in cur_wj_name_list:
                idx=old_fename_list.index(i)
                del fie_sx[idx]


    for i in fie_sx:
        files.append(i)
        file_l.append(i)



print('bbbbbbbbb',parse.quote('下载'))
import datetime
from django.utils.encoding import escape_uri_path
def wenjcl(request):
    global file_l,files,page,resous,ym
    resous = 'yes'
    # id_value = request.COOKIES["cur_id"]
    res=request.GET
    rezd = list(res.keys())
    idx_newname=rezd.index('newname')
    if idx_newname ==0:
        idx_id=idx_newname+1
    else:
        idx_id = idx_newname - 1
    wjid=rezd[idx_id]
    # print('id',id_value,wjid)
    xzorsh=res[wjid]
    cz=res[wjid]
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
        print('request.COOKIES',request.COOKIES)

        id_value = request.COOKIES["cur_id"]

        for i in files:
            if wjid == i['id']:
                wjlj=i['luj']
                wjname=i['name']

    wjlj=wjlj.replace('\\','/')
#http://127.0.0.1:9500/wenjcl/?20191020230908=sharedown    下载请求  url 编码  parse.quote(s)
    if cz =='下载':
        #print('xxxx',wjlj)
        if os.path.isdir(wjlj):
            zip_ya(wjlj)
            wjlj=wjlj+'.zip'
            wjname=wjname+'.zip'
        def file_iterator(file_name, chunk_size=20*1024*1024):
            with open(file_name,'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        the_file_name = wjlj
        #response = FileResponse(file_iterator(the_file_name))
        response = StreamingHttpResponse(file_iterator(the_file_name))
        response = FileResponse(response)
        response['Content-Type'] = 'application/octet-stream'
        response['content-length'] = os.path.getsize(wjlj)
        #response['Content-Disposition'] = 'attachment;filename="{0}"'.format(wjname)
        response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(escape_uri_path(wjname))
        return response
    elif cz == '分享':
        now=datetime.datetime.now()
        wjmy=now.strftime("%Y-%m-%d-%H-%M-%S")
        #url='http://127.0.0.1:9500/wenjcl/?newname=&'+wjmy+'='+'sharedown'
        url=ym+'/wenjcl/?newname=&'+wjmy+'='+'sharedown'
        # with open('sharefe.txt','a') as f:
        #     f.write(wjmy+'~'+wjlj+'~'+wjname+'\n')
        share_lj=wjlj
        share_user_id=wjid[0:1]
        return render(request, "share.html", locals())
        return HttpResponse('分享链接为：'+url)

    elif cz == '重命名':
        oldlj=wjlj
        father_lj=''
        newname=res['newname']
        oldlj_d=oldlj.split('/')

        old_name = oldlj_d[-1]

        if os.path.isdir(oldlj):
            pass
        else:
            if '.' in old_name:
                old_name_hz = old_name.split('.')[-1]
                newname = newname+'.'+old_name_hz
            else:
                pass


        del oldlj_d[-1]
        newlj=''
        for i in oldlj_d:
            newlj=newlj+i+'/'
            if i == oldlj_d[-1]:
                father_lj = father_lj + i
            else:
                father_lj=father_lj+i+'/'
        newlj=newlj+newname
        zt='succes'

        try:
            os.rename(oldlj,newlj)
            shuaxin(father_lj, wjid)
            page=2
            return HttpResponseRedirect('/s')
        except Exception as e:
            print('rename')
            zt=e
            pass
        # #os.rename(src,new)
        return HttpResponse(zt)
    elif cz == '删除':
        father_lj=''
        zt='succes'
        wjlj=wjlj
        id_r=wjid
        if os.path.isdir(wjlj):
            fe_bh = os.listdir(wjlj)
        else:
            fe_bh=['此文件不是文件夹']
        return render(request, "del_fie.html", locals())

def del_fie(request):
    global file_l,files,page,resous
    def sfsy(wj,wjlj_1):
        if wj == 'D:/self':
            return '0'
        elif 'D:/other_user' in wj and len(wjlj_1) == 4:
            return '0'
        else:
            return '1'
    resous = 'yes'
    zt = 'succes'
    wjlj=request.GET['newname']
    id_value=request.GET['id_r']
    chul=request.GET['xz']
    if chul == '删除':
        father_lj = ''
        wjlj_1 =wjlj.split('/')
        wj=''
        idx=0
        for i in wjlj_1:
            if idx < len(wjlj_1)-1:
                if idx == len(wjlj_1)-2:
                    wj=wj+i
                else:
                    wj=wj+i+'/'
                idx=idx+1
        try:
            if os.path.isdir(wjlj):

                shutil.rmtree(wjlj)
            else:
                os.remove(wjlj)
            oldlj_d = wjlj.split('/')
            del oldlj_d[-1]
            for i in oldlj_d:
                if i == oldlj_d[-1]:
                    father_lj = father_lj + i
                else:
                    father_lj = father_lj + i + '/'
            # shuaxin(father_lj, id_value)
        except Exception as e:
            zt = e
        if sfsy(wj,wjlj_1) == '0':
            return HttpResponseRedirect('/')
        else:
            shuaxin(father_lj, id_value)
            return HttpResponseRedirect('/s')
    else:
        return HttpResponseRedirect('/s')


    pass

def netcz(request):
    global files,file_l,resous
    resous = 'yes'
    # id_r=request.GET['id_r']
    cur_id=''
    value = request.COOKIES
    if 'cur_id' in value.keys():
        cur_id= value['cur_id']
    if request.method == "POST":
        res = request.POST
        curlj=res['cur_lj']
        id_r=res['id_r']
        file_obj = request.FILES.get("filename")
        rezd = list(res.keys())
        if 'newfile' in rezd:
            newfilename=res['newfile']
            if os.path.exists(curlj+'/'+newfilename):
                now = datetime.datetime.now()
                wjmy = now.strftime("%Y-%m-%d-%H-%M-%S")
                os.makedirs(curlj+'/'+wjmy)

                # shuaxin(curlj, cur_id)
                # return HttpResponseRedirect('/s')
                # return HttpResponse('已存在该文件夹，新建的文件夹为：'+wjmy)
            else:
                os.makedirs(curlj+'/'+newfilename)
                # print(cur_id)
                # print('befor',file_l)
                # shuaxin(curlj,cur_id)
                # print('after', file_l)
                # return HttpResponseRedirect('/s')
                #return HttpResponse('新建文件夹成功')

        elif file_obj != None:

            with open(curlj + '/'+file_obj.name, "wb") as f:
                for chunk in file_obj.chunks(chunk_size=20*1024*1024):
                    f.write(chunk)
            #shuaxin(curlj, cur_id)

            #return HttpResponseRedirect('/s')
            #return HttpResponse("file upload success!")
        elif file_obj == None and 'newfile' not in rezd:
            return HttpResponse("未操作")
        if cur_id.split('.')[2] == '0':
            return HttpResponseRedirect('/')
        else:
            shuaxin(curlj, id_r)
            return HttpResponseRedirect('/s')


from django.shortcuts import redirect
def del_cookie(request):
    res=HttpResponse('/s')
    res.delete_cookie("cur_id")
    return res

def user_cz(request):
    res=request.GET
    print(res)
    if 'zx' in res.keys():
        #res = HttpResponse('/')
        res=redirect('/')
        res.delete_cookie("cur_id")
        return res
        #return render(request, "dlzc_del_cookies.html")
    else:

        pass


def down_khd(request):
    return render(request, "downkhd.html")

def down_khd_act(request):
    khd_type = request.GET['type']

    if khd_type == 'windows':
        wjlj = 'static/小黑云客户端.7z'
    wjname='小黑云客户端.7z'

    def file_iterator(file_name, chunk_size=20 * 1024 * 1024):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = wjlj
    # response = FileResponse(file_iterator(the_file_name))
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response = FileResponse(response)
    response['Content-Type'] = 'application/octet-stream'
    response['content-length'] = os.path.getsize(wjlj)
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(wjname)
    response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(escape_uri_path(wjname))
    return response

    # return HttpResponse(khd_type)



def my_image(request):
    d = os.path.dirname(__file__)
    imagepath = os.path.join(d,"E:/微信图片_20200114094722.jpg")
    print("imagepath="+str(imagepath))
    image_data = open(imagepath,"rb").read()
    return HttpResponse(image_data,content_type="image/png") #注意旧版的资料使用mimetype,现在已经改为content_type


# def check_loca_fes(loca_lj):
#     local_fies_info = {}
#     local_fies_info['fe_name'] = []
#     local_fies_info['fes_name'] = []
#     local_fies_info['fe_xgtime'] = []
#     local_fies_info['fe_lj'] = []
#     local_fies_info['fe_falj'] = []
#     local_fies_info['fe_size'] = []
#     fie_list = os.listdir(loca_lj)
#     for i in fie_list:
#         felj = loca_lj + '\\' + i
#         if os.path.isdir(loca_lj + '\\' + i):
#             fesname=i
#             local_fies_info['fes_name'].append(fesname)
#         else:
#             fename=i
#             fexgtime = time.ctime(os.path.getmtime(loca_lj + '\\' + i))
#             fe_size=os.path.getsize(loca_lj + '\\' + i)
#             local_fies_info['fe_xgtime'].append(fexgtime)
#             local_fies_info['fe_name'].append(fename)
#             local_fies_info['fe_size'].append(fe_size)
#
#     return local_fies_info
#
#
# def check_romote_fes(request):
#     if request.method == "GET":
#         get_info=request.GET
#         user=get_info['name']
#         user_luj = get_info['luj']
#         print(user,user_luj)
#         if os.path.isdir(user_luj):
#             pass
#         else:
#             os.mkdir(user_luj)
#         data=check_loca_fes(user_luj)
#         return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
#     else:
#         print(request)
#         res = request.POST
#         print(res)
#         lj=res['luj']
#         print(lj)
#
#         print(request.FILES)
#         if request.FILES != {}:
#             try:
#                 file_obj = request.FILES.get("files")
#                 with open(lj, "ab") as f:
#                     for chunk in file_obj.chunks():
#                         f.write(chunk)
#                 return HttpResponse('succ')
#             except:
#                 return HttpResponse('false')
#         else:
#             if res['cz'] =='N':
#                 os.mkdir(lj)
#             elif res['cz'] == 's' and os.path.exists(lj):
#                 os.remove(lj)
#             return HttpResponse('')
