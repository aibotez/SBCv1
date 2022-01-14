from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse,FileResponse
from django.utils.encoding import escape_uri_path
from urllib import parse
from shutil import copyfile
import shutil,json,np,io
import socket,os,time,threading
import ffmpeg,cv2,base64,datetime
from ffmpy3 import FFmpeg
from PIL import Image
from django.http import HttpResponse,JsonResponse
from shutil import copyfile,copytree
import base64,threading,requests
from selenium import webdriver
from mysql_cz import MySqlCz


path=os.getcwd().replace('\\','/')
path=path+'/user/user.txt'
user_info=path

current_khd_version = '1.0.2'
min_khd_version = '1.0.2'



user = 'root'
password='zhouyajie'
host ='127.0.0.1'
port = '3306'
database='nas'
mysql0 = MySqlCz(user,password,host,port,database)
bg = 'ddns_ipv4'

def re_ip_list(request):
    global mysql0
    try:
        wan_ip_list=mysql0.check_ip_data(bg)
    except:
        mysql0 = MySqlCz(user,password,host,port,database)
        wan_ip_list=mysql0.check_ip_data(bg)
    if wan_ip_list == 'erro':
        return HttpResponse('erro')
    else:
        wan_ip_list_chrck=['pan.xht.cool']
        for i in wan_ip_list:

            if len(i)>4:
                wan_ip_list_chrck.append(i)
        print(wan_ip_list_chrck,'20')
        return JsonResponse({'ip_list':wan_ip_list_chrck}, json_dumps_params={'ensure_ascii': False})

def judge_khd(user_khd):
    lsbl = user_khd.split('.')
    user_v=int(lsbl[0]+lsbl[1]+lsbl[2])
    lsbl = min_khd_version.split('.')
    min_v=int(lsbl[0]+lsbl[1]+lsbl[2])
    if user_v < min_v:
        return '0'
    else:
        return '1'

def khd_version_judge(request):
    user_khd_version = request.GET['khd_version_judge']
    juge = judge_khd(user_khd_version)
    return HttpResponse(juge)




def get_fa_lj(path):
    fe_lst = path.split('/')
    lsbl = ''
    for i in fe_lst:
        if fe_lst.index(i) < len(fe_lst)-2:
            lsbl = lsbl + i +'/'
    if lsbl == '':
        lsbl = fe_lst[0] + '/'
    else:
        lsbl = lsbl + fe_lst[-2]
    return lsbl
def up_fes(request):
    if request.method == "POST":
        res = request.POST
        lj=res['luj'].replace('\\','/')
        print('lin81',res['luj'])

        lj = str(base64.b64decode(lj),encoding='utf-8')
        
        if request.FILES != {}:
            try:
                file_obj = request.FILES.get("files")
                with open(lj, "ab") as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)
                return HttpResponse('succ')
            except Exception as e:
                print('101',e)
        
                return HttpResponse('false')
        else:
            if os.path.isdir(lj):
                if 'new' in res.keys():
                    i = 1
                    while True:
                        if os.path.isdir(lj+str(i)):
                            i = i+1
                        else:
                            os.makedirs(lj+str(i))
                            break
                pass
            else:
                os.makedirs(lj)
            return HttpResponse('new dirs')
    else:
        lj = request.GET['luj'].replace(' ','+')
        lj = str(base64.b64decode(lj),encoding='utf-8')
        res = request.GET
        if res['cz'] == 'remove' and os.path.exists(lj):
            os.remove(lj)
            return HttpResponse('remove')
        else:
            return HttpResponse('1')

def khd_qq(request):
    lj_info=request.GET['lj'].replace(' ','+')
    print(lj_info)
    lj_info = str(base64.b64decode(lj_info),encoding='utf-8')
    print(lj_info)
    data={}
    re_fes_info=[]
    if os.path.isdir(lj_info):
        fies = os.listdir(lj_info)
        for i in fies:
            fe={}
            fe_type = ''
            if os.path.isdir(lj_info+'/'+i):
                fe_type = 'dirs'
            else:
                fe_type = 'fie'
            fe['fe_name'] = i
            fe['fe_lj'] = lj_info+'/'+i
            fe['fe_type'] = fe_type
            re_fes_info.append(fe)
        data['data_type'] = 'dirs'
        data['data'] = re_fes_info
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
    else:
        data['data_type'] = 'fie'
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


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
def khd_xz(request):
    wjlj=request.GET['lj'].replace(' ','+')
    print(wjlj)
    wjlj = str(base64.b64decode(wjlj),encoding='utf-8')
    wjname=request.GET['name']
    if os.path.isdir(wjlj):
        data={}
        dirs=[]
        file = []
        root =[]
        for root1, dirs1, files in os.walk(wjlj):
            dirs.append(dirs1)
            file.append(files)
            root.append(root1)
        data['dirs'] = dirs
        data['file'] = file
        data['root'] =root
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
    def file_iterator(file_name,chunk_size):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name = wjlj
    fe_size_int = int(os.path.getsize(wjlj))
    if fe_size_int >= 30:
        chunk_size = 2 * 1024 * 1024
    else:
        chunk_size = 2 * 1024 * 1024
    # response = FileResponse(file_iterator(the_file_name))
    response = StreamingHttpResponse(file_iterator(the_file_name,chunk_size))
    response = FileResponse(response)
    response['Content-Type'] = 'application/octet-stream'
    response['content-length'] = os.path.getsize(wjlj)
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(wjname)
    response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(escape_uri_path(wjname))
    return response

def zhant(request):
    if request.method == 'POST':

        pass
    else:
        copy_src = request.GET['copy_src']
        pastr_lj = request.GET['paste_lj']
        print(copy_src,pastr_lj)
        if os.path.isdir(copy_src):
            copytree(copy_src,pastr_lj)
            pass
        else:
            copyfile(copy_src,pastr_lj)
        return HttpResponse('1')
def del_fe(request):
    del_fe = request.GET['fe']
    del_fe = del_fe.replace(' ','+')
    #print('ffff',del_fe)
    del_fe = str(base64.b64decode(del_fe),encoding='utf-8')
    #print('ffff',del_fe)
    if os.path.isdir(del_fe):
        shutil.rmtree(del_fe)
    else:
        os.remove(del_fe)
    return HttpResponse('1')
def rename(request):
    lj_src = request.GET['luj_src'].replace(' ','+')
    lj_lat = request.GET['luj_lat'].replace(' ','+')


    lj_src = str(base64.b64decode(lj_src),encoding='utf-8')
    lj_lat = str(base64.b64decode(lj_lat),encoding='utf-8')
    
    os.rename(lj_src,lj_lat)
import datetime
def get_fe_info(request):
    lj = request.GET['luj'].replace(' ','+')
    lj = str(base64.b64decode(lj),encoding='utf-8')
    data = {}
    if os.path.isdir(lj):
        fe_size =0
        for root,dirs,files in os.walk(lj):
            for f in files:
                fe_size = fe_size+os.path.getsize(os.path.join(root,f))
    else:
        fe_size = os.path.getsize(lj)
    data['fe_size'] = fe_size
    #t =os.path.getctime(lj)
    t=time.strftime('%Y-%m-%d  %H:%M:%S',time.localtime(os.path.getctime(lj)))
    data['fe_build_time'] = t
    t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(os.path.getmtime(lj)))
    data['fe_xiug_time'] = t
    t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(os.path.os.path.getatime(lj)))
    data['fe_fangw_time'] = t
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
def get_size(request):
    lj = request.GET['luj']
    size = 0
    for root, dirs, files in os.walk(lj):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    if 'D:/self' in lj:
        sum_size = 1024*1024*1024*1024
    else:
        sum_size = 100*1024*1024*1024
    data = {}
    data['size'] = size
    data['sum_size'] = sum_size
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
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
def get_user_info(request):
    user_a = check_user()
    user = request.GET['user']
    for i in user_a['user_name']:
        if i == user:
            idx = user_a['user_name'].index(i)
            user_id = user_a['user_id'][idx]
            return HttpResponse(user_id)
    return HttpResponse('NO')

from pdf2image import convert_from_path

def pdftojpg(fe,page):
    with open(fe, 'rb') as f:
        c = f.read(30*1024*1024)
    with open('output.pdf', 'wb') as f:
        f.write(c)

    page = int(page)
    page = 0
    pages = convert_from_path('output.pdf')
    pages[page].save('ls.jpg', 'JPEG')
    with open('ls.jpg','rb') as f:
        base_tp = f.read()
        base_tp=str(base64.b64encode(base_tp), encoding='utf-8')
    #base_tp = base64.b64decode(base_tp)
    return base_tp
#a=pdftojpg('123.pdf',1)
def get_fie_lx(lj):
    lj1=lj.lower()
    if '.jpg' in lj1 or '.png' in lj1 or '.bmp' in lj1 or '.jpeg' in lj1:
        return 'tp'
    elif '.doc' in lj1 or 'docx' in lj1 or 'pptx' in lj1 or 'ppt' in lj1 or 'xlsx' in lj1:
        return 'pdf_z'
    elif '.pdf' in lj1:
        return 'pdf'
    elif '.mp4' in lj1 or '.webm' in lj1 or '.ogg' in lj1 or '.avi' in lj1 or 'rmvp' in lj1 or '3jp' in lj1:
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
def pdf_c_jpg(request):
    lj = request.GET['luj']
    fe_type = get_fie_lx(lj)
    if request.GET['first'] == 'y':
        return HttpResponse(fe_type)
    page = request.GET['page']
    try:
        img_e = pdftojpg(lj,page)
        print(type(img_e))
        data={}
        data['station'] = 'ok'
        data['type'] = 'tp'
        data['data'] = img_e
    except Exception as e:
        print(e)
        data={}
        data['station'] = 'no'
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

# import os
# os.popen('"C:\Program Files\internet explorer\iexplore.exe" http://zhenz.club')
from selenium import webdriver

# import webbrowser as web
# browser = web.open('http://zhenz.club',new=0,autoraise=True)


# driver = webdriver.Chrome()
# driver.get('https://www.baidu.com')
#web.set_window_size(1000, 800)
#web.register('a', constructor, instance=None)


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
    # word = gencache.EnsureDispatch(work_c)
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
from django.shortcuts import render
def khd_yl(request):
    global resous,zm_t,th_chuanc
    felj = request.GET['luj']
    name = request.GET['user']
    curt_use = name
    curt_lj = felj
    fe_lx = get_fie_lx(felj)
    if fe_lx == 'tp':
        d = os.path.dirname(__file__)
        imagepath = os.path.join(d, felj)
        image_data = open(imagepath, "rb").read()
        return HttpResponse(image_data, content_type="image/png")  # 注意旧版的资料使用mimetype,现在已经改为content_type
    elif fe_lx == 'pdf_z':
        lj = os.getcwd()
        lj = lj.replace('\\', '/')
        lj = lj + '/static/zhongz/' + curt_use + '.pdf'
        gaih_fe = lj
        gaih_fe1 = '/static/zhongz/' + curt_use + '.pdf'
        if os.path.exists(gaih_fe):
            os.remove(gaih_fe)
        createpdf(felj, gaih_fe)
        reurl = "/static/js/pdf.js/web/viewer.html?file=" + gaih_fe1
        return HttpResponseRedirect(reurl)
        # return render(request, "show_pdf.html", locals())
    elif fe_lx == 'txt':
        lj = os.getcwd()
        lj = lj.replace('\\', '/')
        lj = lj + '/static/zhongz/' + curt_use + '.html'
        gaih_fe = lj
        gaih_fe1 = '/static/zhongz/' + curt_use + '.html'
        if os.path.exists(gaih_fe):
            os.remove(gaih_fe)
        txt2html(felj, gaih_fe)
        return HttpResponseRedirect(gaih_fe1)
    elif fe_lx == 'pdf':
        gaih_fe1 = curt_lj[3:]
        gaih_fe1 = '/static/' + gaih_fe1
        # shutil.copyfile(felj,'static/zhongz/'+curt_use+'.pdf')
        # gaih_fe1 = '/static/zhongz/'+curt_use+'.pdf'
        # url="/static/js/pdf.js/web/viewer.html?file=/static/zhongz/1.pdf"
        reurl = "/static/js/pdf.js/web/viewer.html?file=" + gaih_fe1
        return HttpResponseRedirect(reurl)
    elif fe_lx == 'video':
        gaih_fe = curt_lj[3:]
        gaih_fe1 = '/static/' + gaih_fe
        print(curt_lj)
        info = ffmpeg.probe(curt_lj)['streams'][0]['codec_name']
        info = str(info)
        info = info.lower()
        fename = felj.split('/')[-1]
        fename_aft = fename.split('.')
        fename_aft = fename_aft[-1]
        fename_aft = fename.replace(fename_aft, 'mp4')

        fej_fa=get_fa_lj(felj)


        zm_aft = fej_fa + '/zm_' + fename_aft
        zm_th = fej_fa + '/' + fename_aft
        # spsz=curt_lj+'.jpg'
        # rehtspsz=gaih_fe1+'.jpg'
        wjl = os.listdir(fej_fa)
        # if fename+'.jpg' in wjl:
        #     pass
        # else:
        #     ff = FFmpeg(inputs={curt_lj: None}, outputs={spsz: '-y -f mjpeg -ss 0 -t 1'}).run()
        if info == 'h264' or info == 'vp8' or info == 'theora':
            # moov_tq(curt_lj, zm_aft, zm_th)
            # if '.mp4' == curt_lj[-4:]:
            #     moov_tq(curt_lj, zm_aft,zm_th)
            #rehtspsz = get_video_frm(curt_lj)
            # print(rehtspsz)
            return render(request, "show_video.html", locals())
        else:
            if zm_t.isAlive():
                thcc = []
                cz = 'ffmpeg -i ' + curt_lj + ' -vcodec h264 -acodec aac -strict -2 ' + zm_aft
                thcc.append(cz)
                thcc.append(curt_lj)
                thcc.append(zm_aft)
                thcc.append(zm_th)
                if thcc in th_chuanc:
                    idx = th_chuanc.index(thcc)
                else:
                    th_chuanc.append(thcc)
                    idx = th_chuanc.index(thcc)

                return HttpResponse('此视频非网页可播放视频，已加载到转换为网页支持的编码任务的排队中,当前序列为： ' + str(idx + 1))
            else:
                thcc = []
                cz = 'ffmpeg -i ' + curt_lj + ' -vcodec h264 -acodec aac -strict -2 ' + zm_aft
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
                # os.popen('ffmpeg -i ' + curt_lj + ' -vcodec h264 -acodec aac -strict -2 '+zm_aft)
            return HttpResponse('此视频非网页可播放视频，视频正在转换为网页支持的编码，可能需要几分钟（由视频大小决定）')

        # os.popen('ffmpeg -i '+gaih_fe1+' -vcodec h264 -acodec aac -strict -2 h264.mp4')
    elif fe_lx == 'html':
        gaih_fe1 = curt_lj[3:]
        gaih_fe1 = gaih_fe1
        return render(request, gaih_fe1)

    return HttpResponse(felj + '....' + id)

def get_fe_info_judge(request):
    felj = request.GET['luj']
    print(felj)
    if os.path.exists(felj):
        fe_size = os.path.getsize(felj)
        return HttpResponse(str(fe_size))
    else:
        return HttpResponse('nofile')
threadLock = threading.Lock()
def get_fe_size(request):
    felj = request.GET['lj']
    threadLock.acquire()
    # with open(felj,'rb') as f:
    #     cont = f.read()
    fesize = os.path.getsize(felj)
    threadLock.release()
    return HttpResponse(str(fesize))
def return_fie_chunk(request):
    res = request.POST
    fie = res['lj']
    fie_range_start = int(res['range_start'])
    fie_range_length = int(res['range_length'])
    threadLock.acquire()
    with open(fie,'rb+') as f:
        f.seek(fie_range_start)
        content = f.read(fie_range_length)
    threadLock.release()

    # response = FileResponse(content)
    response=HttpResponse(content, content_type='application/octet-stream')
    # response = FileResponse(response)
    # print(567)
    # response['Content-Type'] = 'application/octet-stream'
    # print(569)
    # response['content-length'] = os.path.getsize(fie)
    # print(571)
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format('wj.py')
    return response

def upfie_test(lj,chunk_cont,chunk_sek):
    lj_name = lj.split('/')[-1]
    fa_lj = lj.replace('/'+lj_name,'')
    with open(fa_lj+'/test/'+str(chunk_sek)+'_'+lj_name,'wb')as f:
        f.write(chunk_cont)

def write_fie_chuk(lj,chunk_cont,chunk_sek):
    sek = chunk_sek
    cont = chunk_cont
    threadLock.acquire()
    fp = open(lj, 'rb+')
    fp.seek(sek)
    # fcntl.flock(fp.fileno(),fcntl.LOCK_EX)
    fp.write(cont)
    fp.close()
    threadLock.release()
def creat_fie(lj,fie_size):
    lj_name = lj.split('/')[-1]
    fa_lj = lj.replace('/'+lj_name,'')
    if not os.path.isdir(fa_lj):
        os.makedirs(fa_lj)
    fe = open(lj, 'w')
    fe.seek(fie_size-1)
    fe.write(' ')
    fe.close()
def up_fie_chunk(request):
    res = request.POST
    lj = res['lj'].replace('\\', '/')
    upfe_size = int(res['fe_size'])
    chunk_sek =int(res['range_start'])
    chunk_len = res['range_length']
    if not os.path.exists(lj) or os.path.getsize(lj) != upfe_size:
        creat_fie(lj,upfe_size)
    # if res['act'] == 'start':
    #     fd = open(lj, 'rb+')
    # elif res['act'] == 'stop':
    #     fd.close()
    #     return HttpResponse('fish')

    if request.FILES != {}:
        file_obj = request.FILES.get("files").read()
        write_fie_chuk(lj, file_obj, chunk_sek)
        # upfie_test(lj,file_obj, chunk_sek)
        return HttpResponse('ok')
        # try:
        #
        #     file_obj = request.FILES.get("files")
        #     print('size', len(file_obj))
        #     write_fie_chuk(lj,file_obj, chunk_sek)
        #     print('fishh')
        #     return HttpResponse('ok')
        # except:
        #     print('line676')
    return HttpResponse('error')

import hashlib
def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return 'nofie'
    myHash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myHash.update(b)
    f.close()
    return myHash.hexdigest()
def getmd5(request):
    lj = request.POST['lj']
    md5 = GetFileMd5(lj)
    return HttpResponse(md5)
def chuk_read(lj):
    with open(lj, 'rb') as f:
        while True:
            c = f.read(1024*1024)
            if c:
                yield c
            else:
                break
def complexfie(request):
    lj = request.POST['lj']
    fie_list = request.POST['fie_list']
    fie_list=json.loads(fie_list)
    print(fie_list)
    fp = open(lj,'wb')
    for i in fie_list:
        print(i)
        for chuk in chuk_read(i):
            fp.write(chuk)
        #
        # chuk = chuk_read(i)
        # while chuk != '0':
        #     fp.write(chuk)
        #     chuk = chuk_read(i)
        os.remove(i)
    fp.close()
    return HttpResponse('ok')
