from contextlib import redirect_stderr
from django.shortcuts import render, HttpResponse
import csv
import time
import datetime
from datetime import date
from bs4 import BeautifulSoup
import difflib
import requests
from datetime import datetime
from django.contrib import messages
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd


# Create your views here.

def index(request):
    context={'variable1':"this is sent",
    'variable2':'this is not sent'
    }
    return render(request,'index.html',context)
    return HttpResponse("Hi Jwngdao")

#def monitor2(request):
    context={'a':"this is sent"
    #'variable2':'this is not sent'
    }
    return render(request,'monitor2.html',context)
    return HttpResponse("Hi Jwngdao")
#def profile(request):
    return HttpResponse("Hi Jwngdao")

def monitor(request):
    file=open('/home/zwngdao/Documents/django/test2/static/nic_urls.csv')
    read_urls=csv.reader(file)

    
    
    #file3=open('/home/zwngdao/Documents/django/test2/static/nic_urls2.csv')
    #read_urls3=pd.read_csv(file3)
    #read_urls4=read_urls3.status
    #rowcount=0
    #for row in read_urls4:   
    #    read_urls5=read_urls3.status[rowcount]
    #    rowcount+=1  
    #    hello=str(rowcount)+read_urls5        
    #    print(hello)
        

    #file2=open('/home/zwngdao/Documents/django/test2/static/nic_urls2.csv')
    #read_urls2=pd.read_csv(file2)
    #read_urls3=read_urls3.status[2]
    #print(read_urls3)
    
    
    #return HttpResponse("Initializing")
    #return render(request,)
    #df=pd.read_csv("/home/zwngdao/Documents/django/test2/static/nic_urls.csv")
    #df.loc[1,'status']="red"
    #df.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls.csv", index=False)
    #print(df)


    date_now=str(date.today())
    a=''
    for n,url in enumerate(read_urls):
        #print(url)
        url=','.join(url)
        globals()['url_%d'%n]=""
        
        a=a+"\t"+globals()['url_%d'%n]+url
    #return HttpResponse("Initializing"+a)

    while True:
        
        file=open('/home/zwngdao/Documents/django/test2/static/nic_urls.csv')
        read_urls=csv.reader(file)
        #read_urls=pd.read_csv(file)
        #read_urls=read_urls.URL
        

        a=''    
        for n, url in enumerate(read_urls):
            url=','.join(url)
    
            try:
                response=requests.get(url)
                currentdata=BeautifulSoup(response.text,"lxml")
                img_data=""
                for item in currentdata.find_all('img'):
                    img_data=img_data+str(item['src'])
                currentdata=currentdata.get_text()+img_data
            
                if globals()["url_%d"%n]!=currentdata:
                                

                    if globals()["url_%d"%n]=="":
                        #print(globals()["url_%d"%n]) 
                        
                        globals()["url_%d"%n]=currentdata
                        context={"a":"Monitoring has been started for "+url+" at "+str(datetime.now())}
                        
                        print("Monitoring has been started for "+url+" at "+str(datetime.now()))
                        
                        #return render(request,'monitor2.html',context)
                        #context={'a':"hi jwngdao"}

                        #return render(request,'monitor.html',context)
                    
                    else:
                        print("Changes detected for "+url+" at "+str(datetime.now()))
                        #messages.info(request, 'Changes detected!')
                        oldpage=globals()["url_%d"%n].splitlines()
                        newpage=currentdata.splitlines()
                        globals()["url_%d"%n]=currentdata
                        diff=difflib.unified_diff(oldpage,newpage,n=2)
                        changes="\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])
                        #############filter###############
                        #list1 = ['You are Visitor Number']
                        #list2 = [changes]
 
                        # Filter the second list based on first list
                        #filter_data = [x for x in list2 if
                        #all(y not in x for y in list1)]
                        #changes=filter_data
                        ###############
                        #######CREATING FILES######
                        

                        
                        with open('/home/zwngdao/Documents/django/test2/'+'Monitoring Status'+str(date.today())+'.txt','a') as f:
                            f.writelines("\n########################################################################\n"+"Changes detected for "+url+" at "+str(datetime.now())+"\n"+ changes+"\n###########################################################################\n")
                            
                            f.writelines("\n")
                        with open('/home/zwngdao/Documents/django/test2/static/'+'monitoringstatus'+'.txt','a') as f:
                            f.writelines("\n########################################################################\n"+"Changes detected for "+url+" at "+str(datetime.now())+"\n"+ changes+"\n###########################################################################\n")

                        with open('notification.txt','w') as f:
                            f.writelines("New Changes had been detected for "+url+" at "+str(datetime.now()))
                            f.writelines("\n")
                        ##color changing#

                        with open('changedwebsite.txt','w') as f:
                            f.writelines(url)

                        ###update_color###

                        file2=open('/home/zwngdao/Documents/django/test2/static/nic_urls2.csv')
                        read_urls2=pd.read_csv(file2)
                        read_urls2.loc[n,'status']=1
                        read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
                        #######################
                    
                        if date_now==str(date.today()):
                            with open('/home/zwngdao/Documents/django/test2/static/'+"Today's Changes"+'.txt','a') as f:
                                f.writelines("\n########################################################################\n"+"Changes detected for "+url+" at "+str(datetime.now())+"\n"+ changes+"\n###########################################################################\n")
                        else:
                            with open('/home/zwngdao/Documents/django/test2/static/'+"Today's Changes"+'.txt','w') as f:
                                f.writelines("\n########################################################################\n"+"Changes detected for "+url+" at "+str(datetime.now())+"\n"+ changes+"\n###########################################################################\n")
                                date_now=date_now+1


                    

                        ###################EMAIL SERVICE#################
                        fromaddr = "jwd.monitoring@gmail.com"
                        toaddr = "jwd2.monitor@gmail.com"

                        msg = MIMEMultipart()
                        
                        msg['From'] = fromaddr
                        msg['To'] = toaddr
                       
                        msg['Subject'] = "Changes detected for "+url+" at "+str(datetime.now())
    
                        body = "Changes detected for "+url+" at "+str(datetime.now())+"Kindly find the attachment to view the changes"
                        
                        msg.attach(MIMEText(body, 'plain'))
                        
                        filename = 'Monitoring Status'+str(date.today())+'.txt'
                        attachment = open('/home/zwngdao/Documents/django/test2/'+'Monitoring Status'+str(date.today())+'.txt', "rb")
                        
                        p = MIMEBase('application', 'octet-stream')
                        
                        p.set_payload((attachment).read())
                   
                        encoders.encode_base64(p)
                        
                        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                        
            
                        msg.attach(p)
                        s = smtplib.SMTP('smtp.gmail.com', 587)
                       
                        s.starttls()
                        s.login(fromaddr, "jwngdao1")
                      
                        text = msg.as_string()
                      
                        s.sendmail(fromaddr, toaddr, text)
                        s.quit()
                        
                        #notice= open('notification.txt', 'r')
                        #notice=notice.read()
                        #print(notice)
                        #context={'changed':"Changes detected for "+url+" at "+str(datetime.now())}
                        #return render(request,'index.html',context)
                        
                    
                    f.writelines("\n")

                else:
                    print("No Changes detected for "+url+" at "+str(datetime.now()))
            except Exception as e:
                continue
            
            time.sleep(5)


def notice1(request):
    while True:
        notice1= open('notification.txt', 'r')
        notice2=notice1.read()
        file3=open('/home/zwngdao/Documents/django/test2/static/nic_urls2.csv')
        read_urls3=pd.read_csv(file3)
        #read_urls4=read_urls3.status
        rowcount0=0
        rowcount1=1
        rowcount2=2
        rowcount3=3
        rowcount4=4
        rowcount5=5
        rowcount6=6
        rowcount7=7
        rowcount7=7
        rowcount8=8
        rowcount9=9
        rowcount10=10
        rowcount11=11
        rowcount12=12
        rowcount13=13
        rowcount14=14
        rowcount15=15
        rowcount16=16
        rowcount17=17
        rowcount18=18
        rowcount19=19
        rowcount20=20
        rowcount21=21
        rowcount22=22
        rowcount23=23
        rowcount24=24
        rowcount25=25
        

        status0=read_urls3.status[0]
        rowstat0=rowcount0+status0

        status1=read_urls3.status[1]
        rowstat1=rowcount1+status1

        status2=read_urls3.status[2]
        rowstat2=rowcount2+status2

        status3=read_urls3.status[3]
        rowstat3=rowcount3+status3

        status4=read_urls3.status[4]
        rowstat4=rowcount4+status4

        status5=read_urls3.status[5]
        rowstat5=rowcount5+status5

        status6=read_urls3.status[6]
        rowstat6=rowcount6+status6

        status7=read_urls3.status[7]
        rowstat7=rowcount7+status7

        status8=read_urls3.status[8]
        rowstat8=rowcount8+status8

        status9=read_urls3.status[9]
        rowstat9=rowcount9+status9

        status10=read_urls3.status[10]
        rowstat10=rowcount10+status10

        status11=read_urls3.status[11]
        rowstat11=rowcount11+status11

        status12=read_urls3.status[12]
        rowstat12=rowcount12+status12

        status13=read_urls3.status[13]
        rowstat13=rowcount13+status13


        status14=read_urls3.status[14]
        rowstat14=rowcount14+status14

        status15=read_urls3.status[15]
        rowstat15=rowcount15+status15

        status16=read_urls3.status[16]
        rowstat16=rowcount16+status16

        status17=read_urls3.status[17]
        rowstat17=rowcount17+status17

        status18=read_urls3.status[18]
        rowstat18=rowcount18+status18

        status19=read_urls3.status[19]
        rowstat19=rowcount19+status19

        status20=read_urls3.status[20]
        rowstat20=rowcount20+status20

        status21=read_urls3.status[21]
        rowstat21=rowcount21+status21

        status22=read_urls3.status[22]
        rowstat22=rowcount22+status22

        status23=read_urls3.status[23]
        rowstat23=rowcount23+status23

        status24=read_urls3.status[24]
        rowstat24=rowcount24+status24

        status25=read_urls3.status[25]
        rowstat25=rowcount25+status25

        

        

        

        changedwebsite=open('changedwebsite.txt','r')
        changedwebsite=changedwebsite.read()
        #print(notice2)
        context={'changed':notice2,
                 'rowstat0':rowstat0,
                 'rowstat1':rowstat1,
                 'rowstat2':rowstat2,
                 'rowstat3':rowstat3,
                  'rowstat4':rowstat4,
                 'rowstat5':rowstat5,
                 'rowstat6':rowstat6,
                 'rowstat7':rowstat7,
                 'rowstat8':rowstat8,
                 'rowstat9':rowstat9,
                 'rowstat10':rowstat10,
                 'rowstat11':rowstat11,
                 'rowstat12':rowstat12,
                 'rowstat13':rowstat13,
                 'rowstat14':rowstat14,
                 'rowstat15':rowstat15,
                 'rowstat16':rowstat16,
                 'rowstat17':rowstat17,
                 'rowstat18':rowstat18,
                 'rowstat19':rowstat19,
                 'rowstat20':rowstat20,
                 'rowstat21':rowstat21,
                 'rowstat22':rowstat22,
                 'rowstat23':rowstat23,
                 'rowstat24':rowstat24,
                 'rowstat25':rowstat25

                }
            #time.sleep(10)
        
        return render(request,'index.html',context)
        refresh123()
        time.sleep(10)
        continue
def resetcolor(request):
    with open('changedwebsite.txt','w') as f:
        f.writelines("")




file2=open('/home/zwngdao/Documents/django/test2/static/nic_urls2.csv')
read_urls2=pd.read_csv(file2)

def zero(request):
    read_urls2.loc[0,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def one(request):
    read_urls2.loc[1,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def two(request):
    read_urls2.loc[2,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def three(request):
    read_urls2.loc[3,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def four(request):
    read_urls2.loc[4,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def five(request):
    read_urls2.loc[5,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def six(request):
    read_urls2.loc[6,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def seven(request):
    read_urls2.loc[7,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def eight(request):
    read_urls2.loc[8,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def nine(request):
    read_urls2.loc[9,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def ten(request):
    read_urls2.loc[10,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def one1(request):
    read_urls2.loc[11,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def one2(request):
    read_urls2.loc[12,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def one3(request):
    read_urls2.loc[13,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def one4(request):
    read_urls2.loc[14,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def one5(request):
    read_urls2.loc[15,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def one6(request):
    read_urls2.loc[16,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def one7(request):
    read_urls2.loc[17,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def one8(request):
    read_urls2.loc[18,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def one9(request):
    read_urls2.loc[19,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def two0(request):
    read_urls2.loc[20,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def two1(request):
    read_urls2.loc[21,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def two2(request):
    read_urls2.loc[22,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def two3(request):
    read_urls2.loc[23,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')


def two4(request):
    read_urls2.loc[24,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')

def two5(request):
    read_urls2.loc[25,'status']=0
    read_urls2.to_csv("/home/zwngdao/Documents/django/test2/static/nic_urls2.csv", index=False)
    return render(request,'resettogreen.html')


    