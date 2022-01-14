import requests,os,threading,time



def get_fa_lj(path):
    fe_lst = path.split('/')
    lsbl = ''
    for i in fe_lst:
        if fe_lst.index(i) < len(fe_lst)-2:
            lsbl = lsbl + i +'/'
    if lsbl == '':
        lsbl = fe_lst[0]
    else:
        lsbl = lsbl + fe_lst[-2]
    return lsbl
def up_fe(file_name,chunk_size):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                pass
                #print('stop')
                break
def up_fe_call(lj,ro_lj_fe,url):
    chunk_size=20*1024*1024

    re_url =url +'?luj='+ro_lj_fe+'&&cz=remove'
    data = {}
    data['luj'] = ro_lj_fe
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
def shangc(cs):
    loca_lj = cs[0]
    romote_lj =cs[1]
    url = cs[2]
    loca_fa_lj = get_fa_lj(loca_lj)
    romote_fa_lj = get_fa_lj(romote_lj)
    romote_lj_pj = loca_lj.replace(loca_fa_lj, romote_fa_lj)
    if os.path.isdir(loca_lj):
        #print(romote_lj_pj)
        for root,dirs,fies in os.walk(loca_lj):
            #res = requests.post(url, files={}, data=data).text
            root = root.replace('\\','/')
            romote_lj_pj = root.replace(loca_fa_lj, romote_fa_lj)
            data ={}
            data['luj'] = romote_lj_pj
            res = requests.post(url, files={}, data=data).text
            for i in fies:
                loca_fe = root+'/'+i
                romte_fe = romote_lj_pj+'/'+i
                up_fe_call(loca_fe, romte_fe, url)
            # print(romote_lj_pj)
            #print(root)
            # print(dirs)
            # print(fies)
    else:
        data = {}
        data['luj'] = romote_lj_pj
        #res = requests.post(url, files={}, data=data).text
        up_fe_call(loca_lj, romote_lj_pj, url)

# cs = []
# cs.append('D:/1')
# cs.append('D:/self/1')
# url = 'http://127.0.0.1:9500/khd_upfe/'
# cs.append(url)
#
# t = threading.Thread(target=shangc,args=(cs,))
# t.start()
# # cs[0] = 'D:/apach'
# # t1 = threading.Thread(target=shangc,args=(cs,))
# # t1.start()
# # print('123')