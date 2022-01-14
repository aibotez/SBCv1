import mysql.connector

class MySqlCz():

    def __init__(self,user,password,host,port,database):
        config = {'user':user,
                  'password':password,  # 自己设定的密码
                  'host':host,  # ip地址，本地填127.0.0.1，也可以填localhost
                  'port':port,  # 端口，本地的一般为3306
                  'auth_plugin':'mysql_native_password',
                  'database':database  # 数据库名字，这里选用test_s
                  }
        self.con = mysql.connector.connect(**config)
        self.mycursor = self.con.cursor(buffered=True)
    def add_data(self,bd,clow,vlue):
        sql="INSERT INTO {}({}) VALUES('{}')".format(bd,clow,vlue)#增加数据
        self.mycursor.execute(sql)
        self.con.commit()
    def del_data(self):
        pass
    def chage_ip_data(self,bg,txt,cone):
        sql = 'update {} set ip = {} where ids = {}'.format(bg,txt,cone)
        self.mycursor.execute(sql)
        self.con.commit()
    def check_ip_data(self,bg):
        sql = "SELECT * FROM {} WHERE ids >0".format(bg)
        self.mycursor.execute(sql)
        myresult=self.mycursor.fetchall()
        IP =[]
        for i in myresult:
            IP.append(i[-1])
        return IP
    def update_ip(self,bg,iplist):
        for i in range(len(iplist)):
            ids = str(i+1)
            ip = '"{}"'.format(str(iplist[i]))
            self.chage_ip_data(bg,ip,ids)



# user = 'dl_ip'
# password='z_12345678'
# host ='127.0.0.1'
# port = '3306'
# database='ip_dl'
# mysql0 = MySqlCz(user,password,host,port,database)
# bg = 'ddns_ipv4'
#
# iplist = ['19002.85.3.2','196.562.0.2','56.25.2.5','865.5.8.3']
# mysql0.update_ip(bg,iplist)
#
# data = mysql0.check_ip_data(bg)
# print(data)
