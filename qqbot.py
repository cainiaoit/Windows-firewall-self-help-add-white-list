# -*- coding:utf-8 -*-
import os
import re
import requests

from qqbot import QQBotSlot as qqbotslot, RunBot



#获取到qq号
def qqinfo(member,bot):
        auin=member.uin
        name=member.name
        bl=bot.List('buddy')
        
        for i in bl:
            if i.uin == auin:
                qq=i.name
                break
        return qq
    
#过滤出防火墙IP
def gv(data):
    newdata=[]
    for i in data:
        if i == '':
            continue
        if ':' in i:
            newdata.append(i.split(':')[1])
            print i
    return newdata 

#获取到已存在和不存在的IP 
def yanma(ip,fg):
        ycz=[]
        bcz=[]
        
        for i in ip:
            fgnum=0
            for ii in fg:
                if '/24' in ii:
                    if re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', i)[0] in ii:
                        ycz.append(i)
                        fgnum = 1
                        break
            if i in fg:
                ycz.append(i)
            elif fgnum == 0:
                bcz.append(i)
                    
        return ycz,bcz

#获取防火墙IP列表和要删除的IP
def Firewalls_and_messages(bcz,ycz,fg,ip,dir,file):
    iplist='%s,%s,%s'%(','.join(fg),','.join(ycz),','.join(bcz))
    delete=''
                    
    #清除旧IP
    if not os.path.isdir(dir):
        os.makedirs(dir)
                    
    if os.path.exists(file):
        wfile=open('%s'%file).read()
        deleteip=[]
        if len(wfile) > 0:
            #文件里的IP如果没有出现到消息里则删除
            for i in wfile.split(' '):
                if i == '':
                    continue
                if i not in ip:
                    deleteip.append(i)
                    iplist=iplist.replace('%s'%i, '')
                                            
            if len(deleteip) > 0:
                delete=',已经删除上次的地址'+'%s'%' '.join(deleteip)
    
    
    return iplist,delete  

def discuss(bot):
    restr=''
    if bot.Update('discuss'):
        stri=[]
        g=bot.List('discuss')
        for i in g:
            gg=bot.List('discuss','%s'%i.name)[0]
            if not bot.Update(gg):
                stri.append(i.name)
                            
        if len(stri) == 0:
            restr='刷新讨论组成功'
        else:
            restr='刷新讨论组失败的:%s'%','.join(str(v) for v in stri)    
    else:
        restr='刷新讨论组失败'
    return restr

def group(bot):
    restr=''
    if bot.Update('group'):

        stri=[]
        g=bot.List('group')
        for i in g:
            gg=bot.List('group','%s'%i.name)[0]
            if not bot.Update(gg):
                stri.append(i)
        
        
        if len(stri) == 0:
            restr='刷新群成功'
        else:
            restr="刷新群失败的%s"%','.join(str(v) for v in stri)
    else:
        restr='刷新群失败'
        
    return restr


@qqbotslot
def onQQMessage(bot, contact, member, content):

    #允许执行的QQ
    adminqq=[]
    ifqq=[]
    
    
    newcontent=re.sub("\xc2\xa0|\xe3\x80\x80",' ',content).split(' ')
    
    tmp=[]
    

    for i in newcontent:
        if len(tmp) == 2:
            break
        if i != '':
            tmp.append(i)
    
    print tmp[0]
    
    if tmp[0] == "@qqbot机器人" and tmp[1] == "添加OAIP":
        
        qq=qqinfo(member, bot)
        
        #bot.Update('buddy')
        #bot.Update('discuss')
        
        if qq in ifqq:
            
            ip=re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', content)
            newip=' '.join(ip)
            
            if len(ip) > 0:
                
                
                dir='C:/IP'
                file='%s/%s.txt'%(dir,qq)
                cmd="netsh advfirewall firewall show rule name=allow_TCP"
                
                #规则名称，启用，方向，配置文件，分组，本地IP，远程IP，协议，本地端口，远程端口，边缘遍历，操作
                Rule_name,Enabled,direction,configuration,Grouping,local_IP,Long_range_IP,Agreement,Local_port,teleport,Edge_traversal,operation=gv(os.popen("%s"%cmd).read().replace(' ','').split('\n'))
                #去除/32
                fg=Long_range_IP.replace('/32','').split(',')
                
                #获取已存在和不存在防火墙里的IP，
                ycz,bcz = yanma(ip,fg)
                
                #IP已经存在则直接发送消息提示
                if len(bcz) == 0 :
                    bot.SendTo(contact, member.name+',已经存在 %s'%' '.join(ycz))
                else:
                    iplist,delete=Firewalls_and_messages(bcz,ycz,fg,ip,dir,file)
                    cmd1="netsh advfirewall firewall set rule name=\"allow_TCP\" new remoteip=\"%s\""%iplist
                    #cmd2="netsh advfirewall firewall set rule name=\"allow_UDP\" new remoteip=\"%s\""%iplist
                    
                    
                    f=open('%s'%file,'w')
                    f.write(' '.join(bcz))
                    f.flush()
                    f.close()
                    
                    #添加新ip
                    status1=os.popen("%s"%cmd1).read()
                    #status2=os.popen("%s"%cmd2).read()
                    ygx=unicode("已更新",'utf-8').encode('gbk')
    
                    #判断是否执行成功
                    if ygx in status1 and ygx in status2 :
                        
                        #判断已存在的IP是否有
                        yczip=''
                        if len(ycz) != 0 :
                            yczip=',已存在%s'%' '.join(ycz)
                        
                        bot.SendTo(contact, member.name+',已经将  %s 添加IP白名单%s%s'%(' '.join(bcz),yczip,delete))
                        
                    else:
                        bot.SendTo(contact, member.name+',添加失败 %s'%','.join(ip))
            else:
                bot.SendTo(contact, member.name+',格式为："@qqbot机器人 添加OAIP *.*.*.*",没有检测到IP,多个ip用空格隔开')
        
        
                
    elif tmp[0] == "@qqbot机器人" and tmp[1] == "刷新好友":
        qq=qqinfo(member, bot)
        if bot.Update('buddy') and qq in adminqq:
            bot.SendTo(contact, member.name+'刷新好友成功')
        else:
            bot.SendTo(contact, member.name+'刷新好友失败')
            
    elif tmp[0] == "@qqbot机器人" and tmp[1] == "刷新讨论组":
        qq=qqinfo(member, bot)
        if qq in adminqq:                 
            bot.SendTo(contact, member.name+discuss(bot))    
                
    elif tmp[0] == "@qqbot机器人" and tmp[1] == "刷新组":
        qq=qqinfo(member, bot)
        if qq in adminqq:
            bot.SendTo(contact, member.name+group(bot))
    elif tmp[0] == "@qqbot机器人" and tmp[1] == "刷新所有":
        qq=qqinfo(member, bot)
        if qq in adminqq:
            if bot.Update('buddy') and qq in adminqq:
                bot.SendTo(contact, member.name+'刷新好友成功')
            else:
                bot.SendTo(contact, member.name+'刷新好友失败')
            bot.SendTo(contact, member.name+group(bot))
            bot.SendTo(contact, member.name+discuss(bot))

    elif tmp[0] == "@qqbot机器人" and tmp[1] == "格式":
        bot.SendTo(contact, member.name+"，格式为：\"@qqbot机器人 添加OAIP *.*.*.*\",没有检测到IP,多个ip用空格隔开")
            

            
if __name__ == '__main__':
    RunBot()
