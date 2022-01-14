from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
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


path=os.getcwd().replace('\\','/')
path=path+'/user/user.txt'
user_info=path
ym='http://zhenz.club/'
#ym='http://127.0.0.1:9500/'
share_wj='sharefe.txt'
def check_share_info(req):
    now = datetime.datetime.now()
    now_d = now.strftime("%d")
    now_h = now.strftime("%H")
    now_m = now.strftime("%m")
    now_Y = now.strftime("%Y")
    now_M = now.strftime("%M")
    with open(share_wj) as f:
        info = f.read()
    info =info.split('\n')
    #print(info)
    del info[-1]
    for i in info:
        j = i.split('~')[-1]
        req1 = i.split('~')[0]
        #print(req1)
        if req1 == req:
            gqt = j.split('#')[-1]
            if gqt != '00':
                gqt_Y = gqt.split('-')[0]
                gqt_m = gqt.split('-')[1]
                if int(gqt_m) < 10:
                    gqt_m = '0'+gqt_m
                gqt_d = gqt.split('-')[2]
                if int(gqt_d) < 10:
                    gqt_d = '0'+gqt_d
                gqt_h = gqt.split('-')[3]
                if int(gqt_h) < 10:
                    gqt_h = '0'+gqt_h
                gqt_M = gqt.split('-')[4]
                if int(gqt_M) < 10:
                    gqt_M = '0'+gqt_M
                now_s = int(now_Y+now_m+now_d+now_h+now_M)
                gq_s = int(gqt_Y+gqt_m+gqt_d+gqt_h+gqt_M)
                #print(now_s,gq_s,'ttttttttttt')
                if now_s <= gq_s :
                    return 1
                else:
                    info[info.index(i)]=''
                    with open(share_wj,'w') as f:
                        for i in info:
                            if i != '':
                                f.write(i+'\n')
                    return 0
            else:
                return 1
    return 2


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
def time_h_to(tim,pd):

    if '.' not in tim:
        tim = int(tim)
    else:
        tim = float(tim)
    now = datetime.datetime.now()
    now_d = int(now.strftime("%d"))
    now_h = int(now.strftime("%H"))
    now_m = int(now.strftime("%m"))
    now_M = int(now.strftime("%M"))
    now_Y = int(now.strftime("%Y"))
    gq_Ys = str(now_Y)
    gq_ms = str(now_m)
    gq_ds = str(now_d)
    gq_hs = str(now_h)
    gq_Ms = now.strftime("%M")
    if pd == 'd':
        if tim >=30:
            add_m = int(tim/30)
            add_d = tim % 30
            gq_m = now_d+add_d
            ls_d=now_d+add_d
            if ls_d >= 30:
                gq_m = gq_m + int(ls_d/30)
                gq_d = now_d+(ls_d % 30)
            else:
                gq_d = ls_d
        else:
            ls_d=now_d+tim
            if ls_d >= 30:
                gq_m = now_m + int(ls_d/30)
                gq_d = now_d+(ls_d % 30)
            else:
                gq_d = ls_d
                gq_m = now_m
        gq_ms = str(gq_m)
        gq_ds = str(gq_d)
    elif pd =='m':
        if tim >=12:
            add_Y = int(tim/12)
            add_m = tim % 12
            gq_Y = now_Y+add_Y
            ls_m=now_m+add_m
            if ls_m >= 12:
                gq_Y = gq_Y + int(ls_m/12)
                gq_m = now_m+(ls_m % 12)
            else:
                gq_m = ls_m
        else:
            ls_m=now_m+tim
            if ls_m >= 12:
                gq_Y = now_Y + int(ls_m/12)
                gq_m = now_m+(ls_m % 12)
            else:
                gq_m = ls_m
                gq_Y = now_Y
        gq_ms = str(gq_m)
        gq_Ys = str(gq_Y)
    elif pd == 'Y':
        gq_Ys = str(tim+now_Y)
    elif pd == 'h':
        #print(gq_ds)
        gq_d = gq_ds
        gq_h = gq_hs
        if tim >=24:
            add_d = int(tim/24)
            add_h = tim % 24
            gq_d = now_d+add_d
            ls_h=now_h+add_h
            if ls_h >= 24:
                gq_d = gq_d + int(ls_h/24)
                gq_h = now_h+(ls_h % 24)
            else:
                gq_h = ls_h
        else:
            ls_h=now_h+int(tim)
            if ls_h >= 24:
                gq_d = now_d + int(ls_h/24)
                gq_h = now_h+(ls_h % 24)
            else:
                if int(tim) == tim:
                    gq_h = ls_h
                    gq_d = now_d
                else:
                    min=tim*60
                    if min >=60:
                        gq_h = now_h+int(min/60)
                        gq_Ms = str(now_M+ min % 60)
                    else:
                        gq_Ms = str(now_M + int(min))
        gq_ds = str(gq_d)
        gq_hs = str(gq_h)
        #print('mmmmm',gq_ms,gq_ds)
    return gq_Ys+'-'+gq_ms+'-'+gq_ds+'-'+gq_hs+'-'+gq_Ms



def check_time_limt(tim):
    if tim == '':
        time_l = '00'
    else:
        if '-' in tim :
            info = tim.split('-')
            if len(info) == 2:
                H = info[0]
                M = info[1]
                now = datetime.datetime.now()
                wjtim = now.strftime("%Y-%m-%d")+'-'+H+'-'+M
                return wjtim
            elif len(info) == 3:
                d = info[0]
                H = info[1]
                M = info[2]
                now = datetime.datetime.now()
                wjtim = now.strftime("%Y-%m")+'-'+d+'-'+H+'-'+M
                return wjtim
            elif len(info) == 4:
                m= info[0]
                d = info[1]
                H = info[2]
                M = info[3]
                now = datetime.datetime.now()
                wjtim = now.strftime("%Y")+'-'+m+'-'+d+'-'+H+'-'+M
                return wjtim
            elif len(info) == 5:
                Y = info[0]
                m= info[1]
                d = info[2]
                H = info[3]
                M = info[4]
                now = datetime.datetime.now()
                wjtim = '-'+Y+'-'+m+'-'+d+'-'+H+'-'+M
                return wjtim
        elif '天' in tim:
            # now = datetime.datetime.now()
            # today_d = now.strftime("%d")
            # gq_d = str(int(today_d)+ int(tim.split('天')[0]))
            # wjtim = now.strftime("%Y-%m")+'-'+gq_d+now.strftime("-%H-%M")
            return time_h_to(tim.split('天')[0],'d')
        elif '月' in tim:
            # now = datetime.datetime.now()
            # today_m = now.strftime("%m")
            # gq_m = str(int(today_m)+ int(tim.split('月')[0]))
            # wjtim = now.strftime("%Y")+'-'+gq_m+now.strftime("-%d-%H-%M")
            # return wjtim
            return time_h_to(tim.split('月')[0], 'm')
        elif '年' in tim:
            # now = datetime.datetime.now()
            # today_Y = now.strftime("%Y")
            # gq_Y = str(int(today_Y)+ int(tim.split('年')[0]))
            # wjtim = gq_Y+now.strftime("-%m-%d-%H-%M")
            # return wjtim
            return time_h_to(tim.split('年')[0], 'Y')
        else:
            return time_h_to(tim, 'h')

def get_fie_lx(lj):
    lj1=lj.lower()
    if '.jpg' in lj1 or '.png' in lj1 or '.bmp' in lj1 or '.jpeg' in lj1:
        return 'tp'
    elif '.txt' in lj1 or '.doc' in lj1 or 'docx' in lj1 or 'pptx' in lj1 or 'ppt' in lj1 or 'xlsx' in lj1:
        return 'pdf_z'
    elif '.pdf' in lj1:
        return 'pdf'
    elif '.mp4' in lj1 or '.webm' in lj1 or '.ogg' in lj1 or '.avi' in lj1 or 'rmvp' in lj1 or '3jp' in lj1:
        return 'video'
    elif '.html' in lj1:
        return 'html'
def get_wb(lj):
    pass
from win32com.client import gencache
from win32com.client import constants, gencache
import pythoncom,sys
from win32com import client
from win32com.client.gencache import EnsureDispatch
def createpdf(wordPath, pdfPath):
    pythoncom.CoInitialize()
    # xl = EnsureDispatch("Word.Application")
    # print(sys.modules[xl.__module__].__file__)

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
resouse='n'


def share_to(request):
    global resouse
    resouse ='n'
    info = request.GET
    time_l=''
    share_t_l=info['share_time_limt']
    if share_t_l == '':
        time_l = '00'
    else:
        time_l=check_time_limt(share_t_l)
    share_pass_l = info['share_pass']
    if share_pass_l == '':
        pass_l = '**'
    else:
        pass_l=share_pass_l
    user = info['user']
    share_lj = info['share_lj']
    to_user = info['share_user_limt']
    if to_user == '':
        to_user = '00'
    info_con = user+'#'+share_lj+'#'+to_user+'#'+pass_l+'#'+time_l
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d-%H-%M-%S")
    re_url = user+'-'+now
    info_wr = re_url+'~'+info_con
    share_url = ym+'share_url/?info='+re_url
    with open('sharefe.txt','a') as f:
        f.write(info_wr+'\n')
    return HttpResponse('分享链接为： '+share_url)


def get_info(info):
    with open(share_wj,'r') as f:
        info_txt = f.read()
    info_lst = info_txt.split('\n')
    del info_lst[-1]
    for i in info_lst:
        info_re = i.split('~')[0]
        info_con = i.split('~')[1]
        if info == info_re:
            info_lj = info_con.split('#')[1]
            info_to = info_con.split('#')[2]
            info_pass = info_con.split('#')[3]
            info_gq_time=info_con.split('#')[4]
            return {'info_lj':info_lj,'info_to':info_to,'info_pass':info_pass,'info_gq_time':info_gq_time,'request_hoome':info}
    return '0'
def share_re(request):
    global resouse
    resouse = 'n'
    info1 = request.GET['info']
    user =get_cur_username(info1[0:1]+'.1.1')
    re_gq_pd=check_share_info(info1)
    if re_gq_pd == 0:
        return HttpResponse('资源已过期')
    elif re_gq_pd == 2:
        return HttpResponse('无该资源')
    info = get_info(info1)
    if 'khd_share' not in request.GET.keys():
        if info['info_to'] != '00':
            value = request.COOKIES
            if 'cur_id' in value.keys():
                cur_id= value['cur_id']
                user = get_cur_username(cur_id)
                if user != info['info_to']:
                    return HttpResponse('你没有权限获取该文件')
            else:
                return HttpResponse('该文件设置了指定用户，你还没有登录')
        password = info['info_pass']
        fe_lj = info['info_lj']
        if os.path.isdir(fe_lj):
            file_tu_lj = '/static/images/w.jfif'
        else:
            file_tu_lj = '/static/images/wj.jfif'
        fie_to_b = []
        fie_zd={}
        fie_zd['name'] = info['info_lj'].split('/')[-1]
        fie_zd['fe_lj'] = info['info_lj']
        fie_zd['fetu'] = file_tu_lj
        fie_zd['url']='share_fe_left_cz/?lj='+info['info_lj']+'&&info='+info1
        fie_to_b.append(fie_zd)
        bkbk = fe_lj
        #left = '10000px'
        #stye="position:absolute; left:10000px;font-size:20px;background:#4F909D;color:#FFFFFF;"
        return render(request, "share_show.html", locals())
    else:
        data={}
        data['luj'] = info['info_lj']
        data['pass'] = info['info_pass']
        if os.path.isdir(info['info_lj']):
            fe_type = 'dirs'
        else:
            fe_type = 'fie'
        data['fe_type'] = fe_type
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

def fe_left_cz(request):
    global zm_t,th_chuanc,resouse
    fe = request.GET['lj']
    info1 = request.GET['info']
    user = get_cur_username(info1[0:1] + '.1.1')

    info = get_info(info1)
    fe_lj = info['info_lj']
    re_hoome=info['request_hoome']
    if resouse == 'b':
        if fe_lj in fe:
            pass
        else:
            url =ym+'share_url/?info='+re_hoome
            return HttpResponseRedirect(url)
    password='**'
    print(fe)
    fie_to_b = []
    if os.path.isdir(fe):
        fe_lst=os.listdir(fe)
        for i in fe_lst:
            fie_zd = {}
            fie_zd['name'] = i
            fie_zd['fe_lj'] = fe+'/'+i
            fie_zd['url'] = '?lj=' +fe+'/'+i+'&&info='+info1
            if os.path.isdir(fe+'/'+i):
                fie_zd['fetu'] = '/static/images/w.jfif'
            else:
                fie_zd['fetu']='/static/images/wj.jfif'
            fie_to_b.append(fie_zd)
        bkbk = fe
        left='10px'
        stye = "position:absolute; left:10px;font-size:20px;background:#4F909D;color:#FFFFFF;"
        return render(request, "share_show.html", locals())
    else:
        curt_lj=fe
        fe_lx = get_fie_lx(fe)
        fename = fe.split('/')[-1]
        fej_fa = fe.replace('/'+fename,'')
        if fe_lx == 'tp':
            d = os.path.dirname(__file__)
            imagepath = os.path.join(d, fe)
            image_data = open(imagepath, "rb").read()
            return HttpResponse(image_data, content_type="image/png")  # 注意旧版的资料使用mimetype,现在已经改为content_type
        elif fe_lx == 'pdf_z':
            lj = os.getcwd()
            lj = lj.replace('\\', '/')
            lj = lj + '/static/zhongz/' + fe.split('/')[-1].split('.')[0] + '.pdf'
            gaih_fe = lj
            gaih_fe1 = '/static/zhongz/' + fe.split('/')[-1].split('.')[0] + '.pdf'
            if os.path.exists(gaih_fe):
                os.remove(gaih_fe)
            createpdf(fe, gaih_fe)
            reurl = "/static/js/pdf.js/web/viewer.html?file=" + gaih_fe1
            return HttpResponseRedirect(reurl)
            # return render(request, "show_pdf.html", locals())
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
            #print(curt_lj)
            info = ffmpeg.probe(curt_lj)['streams'][0]['codec_name']
            info = str(info)
            info = info.lower()
            fename_aft = fename.split('.')
            fename_aft = fename_aft[-1]
            fename_aft = fename.replace(fename_aft, 'mp4')

            #print(fej_fa, fename)
            #print(info)
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
                if '.mp4' == curt_lj[-4:]:
                    moov_tq(curt_lj, zm_aft, zm_th)
                rehtspsz = get_video_frm(curt_lj)
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
                    # zm_t = threading.Thread(target=zm)
                    zm_t.start()
                    # os.popen('ffmpeg -i ' + curt_lj + ' -vcodec h264 -acodec aac -strict -2 '+zm_aft)
                return HttpResponse('此视频非网页可播放视频，视频正在转换为网页支持的编码，可能需要几分钟（由视频大小决定）')

            # os.popen('ffmpeg -i '+gaih_fe1+' -vcodec h264 -acodec aac -strict -2 h264.mp4')
        elif fe_lx == 'html':
            gaih_fe1 = curt_lj[3:]
            gaih_fe1 = gaih_fe1
            return render(request, gaih_fe1)
        return HttpResponse('wj')

def share_fe_cz(request):

    pass
def back(request):
    global resouse
    resouse = 'b'
    bak = request.GET
    info = request.GET['info']
    bak = bak.keys()
    bak =list(bak)[1]
    bak =bak+'biaoz....id'
    felj_cut = bak.split('/')[-1]
    felj = bak.replace('/'+felj_cut,'')
    fe = felj
    print('infoo',info)
    url ='http://127.0.0.1:9500/share_url/share_fe_left_cz/?lj='
    url = url+fe+'&&info='+info
    return HttpResponseRedirect(url)

# def share_home_bk(request):
#     info = request.GET['info']
#
#
#     pass
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
def down(request):
    info = request.GET
    #print(info)
    key, = info
    zhi = info[key]
    #print('keyy',zhi)
    if zhi == '下载':
        wjlj = key
        wjname = key.split('/')[-1]
        if os.path.isdir(wjlj):
            zip_ya(wjlj)
            wjlj = wjlj + '.zip'
            wjname = wjname + '.zip'
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
        # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(wjname)
        response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(escape_uri_path(wjname))
        return response
    elif zhi == '保存':
        value = request.COOKIES
        if 'cur_id' in value.keys():
            cur_id= value['cur_id']
            user = get_cur_username(cur_id)
            if user == 'z':
                user_path = 'D:/self/'
                fe_path = user_path+key.split('/')[-1]
                try:
                    copyfile(key,fe_path)
                    return HttpResponse('保存成功')
                except Exception as e:
                    return HttpResponse(e)
            else:
                user_path = 'D:/other_user/'+user+'/'
                fe_path = user_path+key.split('/')[-1]
                try:
                    copyfile(key,fe_path)
                    return HttpResponse('保存成功')
                except Exception as e:
                    return HttpResponse(e)
        else:
            return HttpResponseRedirect(ym)
