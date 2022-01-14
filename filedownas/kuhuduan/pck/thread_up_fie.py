from concurrent.futures import ThreadPoolExecutor
from multiprocessing.dummy import Pool as ThreadPool
import threading,requests,time,json,os
# import fcntl


class ThreadUpFie():
    # def get_ip_list(self):
    #     url = self.ym + '/re_ip_list/'
    #     res = requests.get(url).text
    #     ip_list = json.loads(res)
    #     return ip_list['ip_list']
    def __init__(self,local_lj,ro_lj,ym,fe_chunk_len):
        self.local_lj = local_lj
        self.ro_lj = ro_lj
        self.ym = ym
        self.fe_chunk_len=fe_chunk_len
        self.cur_up_size=0
        self.up_fie_start_time=0
        self.ls_time=0
        self.threadLock = threading.Lock()
        self.get_ip_gil=0
        self.mean_speed=0
        self.cur_speed=0
        self.ip_list = self.get_ip_list()
        self.fe_size=os.path.getsize(self.local_lj)
        self.up_info={}
        self.fp = None
        #self.fp = open(self.local_lj, 'rb+')


    def openfie(self):
        try:
            fd = open(self.local_lj, 'rb+')
            self.fp = fd
            return fd
        except:
            return 'erro'


    def get_ip_list(self):
        url = self.ym + 're_ip_list/'
        res = requests.get(url).text
        ip_list = json.loads(res)
        return ip_list['ip_list']

    def get_xianlu_ip(self):
        ip_x = self.ip_list
        re_ip = ip_x[self.get_ip_gil]
        self.get_ip_gil = self.get_ip_gil + 1
        if self.get_ip_gil >= len(ip_x):
            self.get_ip_gil = 0
        # return ip_x[0]
        return re_ip

    def return_fe_chunk_start(self):
        fie_size = self.fe_size
        i = 0
        cont_list = []
        while True:
            if i > fie_size:
                break
            else:
                cont_list.append({'lj':self.ro_lj, 'range_start': i, 'range_length': self.fe_chunk_len})
                i = i + self.fe_chunk_len
        return cont_list

    def up_fie_chuk(self,chunk_sek):
        fie = self.local_lj
        sek = chunk_sek
        self.threadLock.acquire()
        self.fp.seek(sek)
        # fcntl.flock(fp.fileno(),fcntl.LOCK_EX)
        cont=self.fp.read(self.fe_chunk_len)
        self.threadLock.release()
        return cont
    def up_fe(self,fie_lj, fie_range_start, fie_range_length,cur_ip):
        # global cur_dow_size, t1, down_info
        if cur_ip == 'none':
            self.threadLock.acquire()
            cur_ip = self.get_xianlu_ip()
            self.threadLock.release()
        url = 'http://' + cur_ip + ':80/up_fie_chunk/'
        chuk=self.up_fie_chuk(fie_range_start)
        # url = ym+'/return_fie_chunk/'
        data = {
            'lj': fie_lj,
            'act':'run',
            'fe_size':self.fe_size,
            'range_start': fie_range_start,
            'range_length': fie_range_length
        }
        fie_up = {'files': chuk}
        # print(fie_range_start/1024/1024,url)
        try:
            res = requests.post(url, data=data,files=fie_up,timeout=40)
        except:
            print('line99')
            return 'erro'
        #print('fish',url)
        cur_time=time.time()
        self.cur_up_size = self.cur_up_size+len(chuk)
        self.mean_speed = self.cur_up_size/(cur_time-self.up_fie_start_time)/1024/1024
        return res

    def up_act(self,fie_req_info):
        t1 = time.time()
        size1 = self.cur_up_size
        fie_lj = fie_req_info['lj']
        fie_range_start = fie_req_info['range_start']
        fie_range_length = fie_req_info['range_length']
        fie_chuk = self.up_fe(fie_lj, fie_range_start, fie_range_length,'none')
        if fie_chuk == 'erro':
            fie_chuk = self.up_fe(fie_lj, fie_range_start, fie_range_length,self.ip_list[0])
        t2 = time.time()
        size2 = self.cur_up_size
        self.cur_speed = (size2-size1)/(t2-t1)/1024/1024
        print('cur_sped',self.cur_speed)

    def creat_threads(self,thread_nums_signal):
        print(self.fe_size/1024/1024,'文件大小')
        # self.creat_fie(self.fe_size)
        # self.fp = self.openfie()
        thread_nums = len(self.ip_list)*thread_nums_signal
        # thread_nums=thread_nums_signal
        # thread_nums=1
        fie_req_info_list = self.return_fe_chunk_start()
        self.up_fie_start_time = time.time()
        self.ls_time = self.up_fie_start_time
        # self.up_act(fie_req_info_list[0])
        with ThreadPoolExecutor(max_workers=thread_nums) as pool:
            results = pool.map(self.up_act, fie_req_info_list)
        self.fp.close()






# ym='http://v4.zhenz.club:90/'
# ro_lj='D:\\self\文件\\mysql-installer-community-8.0.20.0.msi'
# local_fie='mysql-installer-community-8.0.20.0.msi'
# fe_chunk_len =1*1024*1024
# up = ThreadUpFie(local_fie, ro_lj, ym, fe_chunk_len)
# up.creat_threads(8)
# def run():
#     up.creat_threads(4)
# t1 = threading.Thread(target=run)
# t1.setDaemon(True)
# t1.start()





# down=ThreadDownFie(local_fie,ro_lj,ym,fe_chunk_len)
# down.creat_threads(4)

# while up.cur_up_size < up.fe_size:
#     print(up.cur_speed,'cur_speed')
#     # print(up.cur_dow_size/1024/1024, 'cur_dow_size')
#     time.sleep(0.5)