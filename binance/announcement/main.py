#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, requests
import pandas as pd
from bs4 import BeautifulSoup
from requests import get,post
from discord_webhook import DiscordWebhook
import json
import schedule
import time



wechatUrl = ''
lastHerf = ''
load_dict = {}

with open("./config.json",'r') as load_f:
    load_dict = json.load(load_f)
    wechatUrl = load_dict['wechat']
    lastHerf = load_dict['last']









def getNew():
    url = "https://www.binance.com/en/support/announcement/c-48?navId=48"
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_list = soup.find_all(class_ = 'css-1ej4hfo')
    new = news_list[0]
    _last = new.get('href');

    if _last != load_dict['last']:
        load_dict['last'] = _last;
        upDateConfig()
        senMsg(_last,new.string)
    else:
        print('无变化');


   



def upDateConfig():
    json_str = json.dumps(load_dict)
    with open("./config.json",'w') as load_f:
        load_f.write(json_str)
        print("加载入文件完成...")

def senMsg(href,text):
    url = 'https://www.binance.com'+href
    data = json.dumps(
        {
            'msgtype': 'markdown',
           
            'markdown':{
                'content': f'''
                    ><font color="warning">{text}</font> \n
                    [链接]({url})'''
            }
        }
    )
    post(
        wechatUrl,
        data=data
    )

getNew()
schedule.every(60 * 5).seconds.do(getNew)
while True:
    schedule.run_pending()