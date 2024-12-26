import requests
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime,timedelta
import pandas as pd
import jpholiday

#number = input("何月何日:")
dt_now=datetime.now()
i=1
if dt_now.weekday()<5 and jpholiday.is_holiday(dt_now)==False:
    z=0
    tomorrow = dt_now + timedelta(days=i)
    while tomorrow.weekday()<=4:
        tomorrow = dt_now + timedelta(days=i)
        i+=1
else:
    z=1
    tomorrow = dt_now + timedelta(days=i)
    while tomorrow.weekday()>=5:
        tomorrow = dt_now + timedelta(days=i)
        i+=1

today = dt_now.strftime('%Y%m%d')
tomorrow = tomorrow.strftime('%Y%m%d')
now_h = dt_now.strftime('%H')
now_m = dt_now.strftime('%M')
for r in range(2):
    if r == 0:
        res=requests.get(f'https://timetable.jr-odekake.net/station-timetable/2892067001?date={today}')
    else:
        res=requests.get(f'https://timetable.jr-odekake.net/station-timetable/2892067001?date={tomorrow}')
    soup = BeautifulSoup(res.text,"html.parser")
    hour = soup.find_all("tr" ,class_="body-row")
    h = []
    lis=[]

    for k,i in enumerate(hour):
        l=[]
        m=[]
        d=[]
        
        h.append(i.find(class_="hour").text)
        minutes = i.find_all(class_="minute-item")
        legend_G = []
        legend_O = []
        legend = []
        x=[]
        for j in minutes:
            legend_G=j.find_all(class_="legendGreen")
            legend_O=j.find_all(class_="legendOrange")
            mini=j.find(class_="minute")
            dest=j.find(class_="destination")
            if legend_O:
                legend = "快"
            elif legend_G:
                legend = "区快"
            else:
                legend = "普"
            l.append(legend)
            m.append((mini.text).zfill(2))
            d.append(dest.text)
        for i in range(len(l)):
            x=[h[k],m[i],l[i],d[i]]
            lis.append(x)

    list1=lis
    columns1 =["時","分","種別","行先"]
    if r==0:
        df1=pd.DataFrame(data=list1, columns=columns1)
    else:
        df2=pd.DataFrame(data=list1, columns=columns1)

file="gakkentoshi 住道.xlsx"
with pd.ExcelWriter(file,engine='openpyxl') as writer:
    if z==0:
        df1.to_excel(writer,sheet_name="平日")
        df2.to_excel(writer,sheet_name="休日")
    else:
        df1.to_excel(writer,sheet_name="休日")
        df2.to_excel(writer,sheet_name="平日")
