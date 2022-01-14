from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse,FileResponse
from urllib import parse
import shutil,json,np,io,requests
import socket,os,time,threading
import ffmpeg,base64
from ffmpy3 import FFmpeg
from PIL import Image





url1 = 'https://www.hxcbb5.com/index.aspx'
url_list = 'https://www.cthxc.com/Video/GetList'
url_per='https://www.cthxc.com/Video/GetPreUrl'
url_getinfo='https://www.cthxc.com/Video/GetInfo'
#  zhu   fi18.cc   bei  fi19.cc
# s='jKfe7PpPHmIVWwdEjSts60cuLujl/ggl/YlzeFXbipgB1Xi8ZQPtLlX2F6UvRUuCAIQEAKJS/sffzBoLBolkrs2o+LzkUFPxL1VLNq4biqPCqH3DhOBX1YJy8WJ5SOLqAgm8eBM9xIqlyUC9aoiXIzhxiJ36em2NciLY='
# s1=base64.b64decode(s)
# s1 = bytes(s1)
# print(s1)


def get_video_info(page):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        #'token': 'APbQ4c4wDyhCkwwvoQwLJqnIeQyBjodUoLrjH9PtbVVckcRei8aHdyYCAPHef6AB7YMuD3wybl8A8G3fNrvDIe78x7wTsgESsY2Ftzhg+55WpxvrSt2EWSr3C6w6FDfvDpKvD977KsKi59SIA3BVB/X/6UAbA+652GYpeIC++5s=',
        'path': '/Video/GetList',
        'authority': 'www.cthxc.com',
        'method': 'POST',
        'scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '100',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://www.hxcbb5.com',
        'referer': 'https://www.hxcbb5.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site'
    }
    payload = {
        'ClientType': 1,
        'length': 48,
        'start': 48*(page-1),
        'pageindex': page,
        'ordertext': [{
            'column', 'AddTime',
            'dir', 'desc'
        }]
    }
#[{"ID":14400,"Name":"在柏林","CoverImgUrl":"https://img25.qqlszt.com/1jxxl/JXXL1795ECFA.jpg","SeeCount":12819,"CollectionCount":1069,"LikeCount":925,"Point":0.0,"Length":707,"Disabled":0,"IsNeedLogin":1,"IsVip":1,"Tags":"上位","TypeName":"私","ParentID":4,"AddTime":"2020-02-27 16:12:51","TypeID":7,"Hot":17876}
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError
    res = requests.post(url_list,data=json.dumps(payload, default=set_default),headers=headers).text
    # sessions = requests.session()
    # res = sessions.post(url=url_list, data=json.dumps(payload, default=set_default), headers=headers).text
    res = res.replace('null','0')
    res = eval(res)
    video_infoo = res['data']
    for i in range(len(video_infoo)):
        lgh = int(video_infoo[i]['Length'])
        video_infoo[i]['Length'] = str(int(lgh/60))
    return video_infoo
# ID,Name,CoverImgUrl,Length
def get_video_indexurl(video_id):
    headers={
        'token':'',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        'path':'/Video/GetInfo',
        'authority':'www.cthxc.com',
        'method':'POST',
        'scheme': 'https',
        'accept':'application/json, text/plain, */*',
        'content-length':'45',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'content-type':'application/json;charset=UTF-8',
        'origin':'https://www.hxcbb5.com',
        'referer':'https://www.hxcbb5.com/player.aspx?math=0&id='+video_id,
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'cross-site'
    }
    payload={
        'VideoID':video_id,
        'UserID':0,
        'ClientType':1
    }
    res = requests.post(url_getinfo,data=json.dumps(payload),headers=headers).text

    res = res.replace('null','0')
    res = eval(res)
    res=res['data']
    v_name = res['Name']
    v_time = str(int(int(res['Length'])/60))
    v_re_url = res['PreUrl']
    preurl = v_re_url
    re_v_url_t_q = preurl.split('/')[-1]
    re_v_url_t = preurl.replace(re_v_url_t_q,'')

    res_ls = requests.get(v_re_url).text
    res_ls = res_ls.split('\n')
    for i in res_ls:
        if 'index' in i:
            i = i.replace('\r', '')
            inde_len = i.replace('index', '').replace('.ts', '')
            break


    v_info={}
    v_info['time'] = v_time
    v_info['preurl'] = re_v_url_t
    v_info['name'] = v_name
    v_info['inde_len'] = len(inde_len)

    return v_info
def down_video(video_info):
    url_v = video_info['preurl']
    inde_len = video_info['inde_len']
    i = 0
    # if os.path.exists(lj):
    #     os.remove(lj)
    while True:
        inde = str(i)
        for tx in range(inde_len-len(inde)):
            inde = '0'+inde
        print(inde)
        t_c = 'index'+inde+'.ts'
        i = i+1
        urll = url_v + t_c
        v_data = requests.get(urll).content
        if 'Message' in str(v_data):
            print('fssh')
            break
        else:
            time.sleep(1)
            yield v_data

def down_apd_video(video_info,lj):
    url_v = video_info['preurl']
    inde_len = video_info['inde_len']
    i = 0
    if os.path.exists(lj):
        os.remove(lj)
    # with open(lj,'w') as f:
    #     f.write('')
    zm_lj = 'zm_' + lj

    xr = 'file '+"'"+lj+"'"+'\n'+'file '+"'"+zm_lj+"'"
    with open('files.txt','w') as f:
        f.write(xr )

    while True:
        inde = str(i)
        for tx in range(inde_len-len(inde)):
            inde = '0'+inde
        print(inde)
        t_c = 'index'+inde+'.ts'
        i = i+1
        urll = url_v + t_c
        try:
            if os.path.exists(zm_lj):
                os.remove(zm_lj)
            if '0000.ts' in t_c:
                print('0000')
                ff = FFmpeg(inputs={urll: None},outputs={lj: ' -vcodec h264 -acodec aac -strict -2 -movflags faststart'}).run()
            else:
                ff = FFmpeg(inputs={urll: None}, outputs={zm_lj: ' -vcodec h264 -acodec aac -strict -2 -movflags faststart'}).run()
                os.system('ffmpeg -f concat -safe 0 -i files.txt -c copy yzm.mp4')
                time.sleep(1)
                os.remove(lj)
                print('1')
                os.rename('yzm.mp4',lj)
            print('2')
            print(t_c)
            time.sleep(1)
        except:

            print('ddsss')
            break
#os.system('ffmpeg -f concat -safe 0 -i files.txt -c copy yzm.mp4')
def apd_video(re_bl):
    video_id = re_bl[0]
    lj = re_bl[1]
    video_info = get_video_indexurl(video_id)
    down_apd_video(video_info, lj)

def chose_page(request):
    return HttpResponse('该功能已关闭！！！')
    page = request.GET['page']
    page = int(page)
    videos_info = get_video_info(page)
    cur_page = '当前页数：'+str(page)
    return render(request,"zyh.html", locals())
def se_zy(request):
    cur_url=request.META['HTTP_HOST']
    cur_url = 'http://'+cur_url+'/'
    c_url = cur_url+'zyh_chose_page/?page=1'
    print(c_url)
    return HttpResponseRedirect(c_url)
    # return render(request, "zyh.html", locals())
def chose_v(request,id):
    cur_url=request.META['HTTP_HOST']
    cur_url = 'http://'+cur_url+'/'
    video_id = id
    bf_url = cur_url+'video_bf_id/'+id
    video_id = id
    lj = id+'.mp4'
    path = lj
    re_bl=[]
    re_bl.append(video_id)
    re_bl.append(lj)
    t1 = threading.Thread(target=apd_video,args=(re_bl,))
    t1.setDaemon(True)
    #t1.start()
    return render(request, "view_video.html", locals())
def bl_video(path):
    with open(path, 'rb') as f:
        c = f.read()
        if c:
            return c
def bf_video(request,id):
    # path ='暴走大事件.MP4'
    path = 'yzm_test1.mpg'
    video_id = id
    lj = id+'.mp4'
    path = lj
    while True:
        if os.path.exists(lj):
            break
    # re_bl=[]
    # re_bl.append(video_id)
    # re_bl.append(lj)
    # t1 = threading.Thread(target=apd_video,args=(re_bl,))
    # t1.setDaemon(True)
    # t1.start()

    def file_iterat(chunk_size=20 * 1024 * 1024):
        # while True:
        #     c = bl_video(path)
        #     if c:
        #         print(path)
        #         path = 'b.mp4'
        #         yield c
        #     else:
        #         break
        with open(path, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    content_type = 'video/mp4'
    size = os.path.getsize(path)
    #resp = StreamingHttpResponse(file_iterat(chunk_size=2 * 1024 * 1024), content_type=content_type)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        #resp = StreamingHttpResponse(file_iterat(path))
    resp['Content-Length'] = str(size)
    #resp['Content-Type'] = 'application/x-mpegURL'
    resp['Accept-Ranges'] = 'bytes'
    return resp
from django.utils.encoding import escape_uri_path
def zyh_down(request):
    id = request.GET
    id = list(id.keys())[0]
    print(id)
    wjname = id+'.ts'
    video_info = get_video_indexurl(id)
    data=down_video(video_info)
    response = StreamingHttpResponse(data)
    response = FileResponse(response)
    response['Content-Type'] = 'application/octet-stream'
    #response['content-length'] = os.path.getsize(wjlj)
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(wjname)
    response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(escape_uri_path(wjname))
    return response

def page_cz(request):
    cur_url=request.META['HTTP_HOST']
    cur_url = 'http://'+cur_url+'/'
    print(request.GET)
    re_s = request.GET
    cur_page = re_s['cur_page'].split('：')[-1]
    print(cur_page)
    if 'next' in re_s.keys():
        next_page = int(cur_page)+1
        c_url = cur_url + 'zyh_chose_page/?page='+str(next_page)
        return HttpResponseRedirect(c_url)
    else:
        per_page = int(cur_page)-1
        c_url = cur_url + 'zyh_chose_page/?page='+str(per_page)
        return HttpResponseRedirect(c_url)



from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
import re, mimetypes




def test_se(request):

    return render(request, "m3u8_test.html")

def test1(request):
    wjlj = '暴走大事件.MP4'
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
    response['Content-Type'] = 'application/octet-stream'
    response['content-length'] = os.path.getsize(wjlj)
    response['Content-Range'] = 'bytes %s-%s/%s' % (0, 20*1024, 50*1024)
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(wjname)
    #response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(escape_uri_path(wjname))
    return response





def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
  with open(file_name, "rb") as f:
    f.seek(offset, os.SEEK_SET)
    remaining = length
    while True:
      bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
      data = f.read(bytes_length)
      if not data:
        break
      if remaining:
        remaining -= len(data)
      yield data
def test(request):
    def file_iterat(file_name, chunk_size=2 * 1024 * 1024):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    """将视频文件以流媒体的方式响应"""
    path = '14393.ts'
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    content_type='video/m3u8'

    print(content_type)
    if range_match:
        print('11')
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 8  # 8M 每片,响应体最大体积
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206,
                                     content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        print('2222')
        # 不是以视频流方式的获取时，以生成器方式返回整个文件，节省内存
        #resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp = StreamingHttpResponse(file_iterat(path))
        resp['Content-Length'] = str(size)
        #resp['Content-Type'] = 'application/x-mpegURL'
    resp['Accept-Ranges'] = 'bytes'
    print(resp)
    return resp
