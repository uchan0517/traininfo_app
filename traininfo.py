import streamlit as st
import datetime
import pandas as pd
import jpholiday
import requests

urt = "https://ntool.online/data/train_all.json"
res = requests.get(urt)
chien_json = res.json()
chien = chien_json["data"]["6"][8]

#number = input("何月何日:")
dt_now=datetime.datetime.now()
today = dt_now.strftime('%Y%m%d')
now_h = dt_now.strftime('%H')
now_m = dt_now.strftime('%M')

if dt_now.weekday()<5 and jpholiday.is_holiday(dt_now)==False:
    df = pd.read_excel("gakkentoshi.xlsx", index_col=0,sheet_name="平日")
    print("平日ダイヤ")
    print(df)
else:
    df = pd.read_excel("gakkentoshi.xlsx", index_col=0,sheet_name="休日")
    print("休日ダイヤ")

df_A = df[((df['時']==int(now_h)) & (df['分']>=int(now_m)))]
if df_A.empty:
    df_A = df[df['時']>int(now_h)]
df_now = df[df_A.index[0]:df_A.index[0]+3]
df_now = df_now.reset_index().drop("index",axis=1)
df_now.index = df_now.index + 1
df_now.insert(loc=0,column="発車順",value=["先発","次発","次々発"])
df_now.set_index("発車順")

if dt_now.weekday()<5 and jpholiday.is_holiday(dt_now)==False:
    df = pd.read_excel("gakkentoshi_down.xlsx", index_col=0,sheet_name="平日")
    print("平日ダイヤ")
else:
    df = pd.read_excel("gakkentoshi_down.xlsx", index_col=0,sheet_name="休日")
    print("休日ダイヤ")
df_A = df[((df['時']==int(now_h)) & (df['分']>=int(now_m)))]

if df_A.empty:
    df_A = df[df['時']>int(now_h)]
df_now2 = df[df_A.index[0]:df_A.index[0]+3]
df_now2 = df_now2.reset_index().drop("index",axis=1)
df_now2.index = df_now2.index + 1
df_now2.insert(loc=0,column="発車順",value=["先発","次発","次々発"])
df_now2.set_index("発車順")

if dt_now.weekday()<5 and jpholiday.is_holiday(dt_now)==False:
    df = pd.read_excel("gakkentoshi 住道.xlsx", index_col=0,sheet_name="平日")
    print("平日ダイヤ")
    print(df)
else:
    df = pd.read_excel("gakkentoshi 住道.xlsx", index_col=0,sheet_name="休日")
    print("休日ダイヤ")

df_A = df[((df['時']==int(now_h)) & (df['分']>=int(now_m)))]
if df_A.empty:
    df_A = df[df['時']>int(now_h)]
df_now0 = df[df_A.index[0]:df_A.index[0]+3]
df_now0 = df_now0.reset_index().drop("index",axis=1)
df_now0.index = df_now0.index + 1
df_now0.insert(loc=0,column="発車順",value=["先発","次発","次々発"])
df_now0.set_index("発車順")

if dt_now.weekday()<5 and jpholiday.is_holiday(dt_now)==False:
    df = pd.read_excel("gakkentoshi down住道.xlsx", index_col=0,sheet_name="平日")
    print("平日ダイヤ")
else:
    df = pd.read_excel("gakkentoshi down住道.xlsx", index_col=0,sheet_name="休日")
    print("休日ダイヤ")
df_A = df[((df['時']==int(now_h)) & (df['分']>=int(now_m)))]

if df_A.empty:
    df_A = df[df['時']>int(now_h)]
df_now1 = df[df_A.index[0]:df_A.index[0]+3]
df_now1 = df_now1.reset_index().drop("index",axis=1)
df_now1.index = df_now1.index + 1
df_now1.insert(loc=0,column="発車順",value=["先発","次発","次々発"])
df_now1.set_index("発車順")

st.title("学研都市線 四条畷&住道駅 時刻表")
st.subheader("四条畷駅")
col1, col2, = st.columns([1,1])#gap="small"
with col1:
   st.write("上り  京橋：尼崎方面")
   st.write(df_now)
with col2:
   st.write("下り  松井山手：木津方面")
   st.write(df_now2)

st.subheader("住道駅")
col1, col2, = st.columns([1,1])#gap="small"
with col1:
   st.write("上り  京橋：尼崎方面")
   st.write(df_now0)
with col2:
   st.write("下り  松井山手：木津方面")
   st.write(df_now1)
st.button("更新", type="primary")
st.subheader("運行状況")
st.write(chien["railName"]+"："+chien["info"])

