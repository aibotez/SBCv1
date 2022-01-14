import os
def sharewifi():
    ssid=input('输入热点名 ')
    keypass=input('输入热点密码 ')
    #os.system('copy a b')
    #os.remove(a)
    try:
        os.remove('share_ls.bat')
    except:
        pass
    try:
        os.system('copy sharewifi.bat share_ls.bat')
    except:
        pass
    
    jlwk='netsh wlan set hostednetwork mod=allow ssid='+ssid+' key='+keypass+'\n'
    startwifi='netsh wlan start hostednetwork'+'\n'
    with open('share_ls.bat','a') as f:
        f.write(jlwk+startwifi)
    os.system('share_ls.bat')
sharewifi()
