from concurrent.futures import ThreadPoolExecutor
from multiprocessing.dummy import Pool as ThreadPool
import threading,requests,time,json
# import fcntl


class ThreadDownFie():
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
        self.cur_dow_size=0
        self.down_fie_start_time=0
        self.ls_time=0
        self.threadLock = threading.Lock()
        self.get_ip_gil=0
        self.mean_speed=0
        self.cur_speed=0
        self.ip_list = self.get_ip_list()
        self.fe_size=self.get_fe_size()
        self.down_info={}
        self.creat_fie(self.fe_size)
        self.fp = open(self.local_lj, 'rb+')

    def creat_fie(self,fie_size):
        fe = open(self.local_lj, 'w')
        fe.seek(fie_size-1)
        fe.write(' ')
        fe.close()
    def openfie(self):
        fd = open(self.local_lj, 'rb+')
        return fd


    def get_ip_list(self):
        url = self.ym + 're_ip_list/'
        res = requests.get(url).text
        ip_list = json.loads(res)
        # print(ip_list['ip_list'])
        return ip_list['ip_list']

    def get_xianlu_ip(self):
        ip_x = self.ip_list
        re_ip = ip_x[self.get_ip_gil]
        self.get_ip_gil = self.get_ip_gil + 1
        if self.get_ip_gil >= len(ip_x):
            self.get_ip_gil = 0
        # print(re_ip)
        return re_ip

    def get_fe_size(self):
        url = self.ym + 'get_fe_size/?lj=' + self.ro_lj
        res = requests.get(url).text
        fie_size = int(res)
        return fie_size

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

    def write_fie_chuk(self,chunk_cont,chunk_sek):

        fie = self.local_lj
        sek = chunk_sek
        cont = chunk_cont
        self.threadLock.acquire()
        self.fp.seek(sek)
        # fcntl.flock(fp.fileno(),fcntl.LOCK_EX)
        self.fp.write(cont)
        self.threadLock.release()
    def down_fe(self,fie_lj, fie_range_start, fie_range_length,cur_ip):
        # global cur_dow_size, t1, down_info
        if cur_ip == 'none':
            self.threadLock.acquire()
            cur_ip = self.get_xianlu_ip()
            self.threadLock.release()
        url = 'http://' + cur_ip + ':80/return_fie_chunk/'
        # url = ym+'/return_fie_chunk/'
        data = {
            'lj': fie_lj,
            'range_start': fie_range_start,
            'range_length': fie_range_length
        }
        # print(fie_range_start/1024/1024,url)
        try:
            res = requests.post(url, data=data,timeout=4).content
        except:
            print('line99')
            return 'erro'
        #print('fish',url)
        cur_time=time.time()
        self.write_fie_chuk(res,fie_range_start)
        self.cur_dow_size = self.cur_dow_size+len(res)
        self.mean_speed = self.cur_dow_size/(cur_time-self.down_fie_start_time)/1024/1024
        return res

    def down_act(self,fie_req_info):
        t1 = time.time()
        size1 = self.cur_dow_size
        fie_lj = fie_req_info['lj']
        fie_range_start = fie_req_info['range_start']
        fie_range_length = fie_req_info['range_length']
        fie_chuk = self.down_fe(fie_lj, fie_range_start, fie_range_length,'none')
        if fie_chuk == 'erro':
            fie_chuk = self.down_fe(fie_lj, fie_range_start, fie_range_length,self.ip_list[0])
        t2 = time.time()
        size2 = self.cur_dow_size
        self.cur_speed = (size2-size1)/(t2-t1)/1024/1024
        # print('cur_sped',self.cur_speed)

    def creat_threads(self,thread_nums_signal):
        print(self.fe_size/1024/1024,'文件大小')
        self.creat_fie(self.fe_size)
        # self.fp = self.openfie()
        thread_nums = len(self.ip_list)*thread_nums_signal
        thread_nums=1
        fie_req_info_list = self.return_fe_chunk_start()
        self.down_fie_start_time = time.time()
        self.ls_time = self.down_fie_start_time
        with ThreadPoolExecutor(max_workers=thread_nums) as pool:
            results = pool.map(self.down_act, fie_req_info_list)
        self.fp.close()






# ym='http://v4.zhenz.club:90/'
# ro_lj='D:\\self\文件\\jre-8u251-windows-i586.exe'
# local_fie='jre-8u251-windows-i586.exe'
# fe_chunk_len =1*1024*1024
# down = ThreadDownFie(local_fie, ro_lj, ym, fe_chunk_len)
# def run():
#     down.creat_threads(4)
# t1 = threading.Thread(target=run)
# t1.setDaemon(True)
# t1.start()
# #
# #
# while down.cur_dow_size < down.fe_size:
#     print(down.cur_speed,'cur_speed')
#     # print(down.cur_dow_size/1024/1024, 'cur_dow_size')
#     time.sleep(0.5)