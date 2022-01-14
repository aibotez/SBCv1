
import wmi
import base64
import socket
import uuid

def get_mac_address():
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac
def get_computer_user():
    myname = socket.getfqdn(socket.gethostname())
    return myname
c = wmi.WMI()
def printMain_board():
    boards = []
    for board_id in c.Win32_BaseBoard():
        tmpmsg = {}
        tmpmsg['UUID'] = board_id.qualifiers['UUID'][1:-1]# 主板UUID,有的主板这部分信息取到为空值，ffffff-ffffff这样的
        tmpmsg['SerialNumber'] = board_id.SerialNumber# 主板序列号
        tmpmsg['Manufacturer'] = board_id.Manufacturer# 主板生产品牌厂家
        tmpmsg['Product'] = board_id.Product# 主板型号
        boards.append(tmpmsg)
        re_info = tmpmsg['Manufacturer']+tmpmsg['Product']+tmpmsg['SerialNumber']+tmpmsg['UUID']
        return re_info
def printCPU():
    tmpdict = {}
    tmpdict["CpuCores"] = 0
    cpu = c.Win32_Processor()[0]
    tmpdict["cpuid"] = cpu.ProcessorId.strip()
    tmpdict['systemName'] = cpu.SystemName
    # for cpu in c.Win32_Processor():
    #     print(cpu)
    #     tmpdict["cpuid"] = cpu.ProcessorId.strip()
    #     tmpdict['systemName'] = cpu.SystemName
    re_info = tmpdict['systemName']+tmpdict["cpuid"]
    return re_info
def get_computer_info():
    a = printMain_board()+get_computer_user()+get_mac_address()
    a = a.replace(' ','').encode('utf-8')#转为utf-8，防止包含中文,,转码为byte
    a =str(base64.b64encode(a), encoding='utf-8') #byte 转为base64字符
    # print(base64.b64decode(a).decode('utf-8'))#转换回来
    # print(a)
    return a
