# -*- coding:utf-8 -*-
import twitter
import configparser
from requests import post 
import json
import schedule

fileName = 'config.ini'
config = configparser.ConfigParser()
config.read(fileName)


CONSUMER_KEY = config.get('config','CONSUMER_KEY')
CONSUMER_SECRET = config.get('config','CONSUMER_SECRET')
ACCESS_TOKEN = config.get('config','ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config.get('config','ACCESS_TOKEN_SECRET')
WECHAT_URL = config.get('config','wechatUrl')


statusId = config.get('status','id')





api = twitter.Api(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)









# 更新本地 配置文件 statusID
def upDateConfig():
    userID = config.set('status','id',str(statusId))
    with open(fileName, 'w') as configfile:
        config.write(configfile)
        print('写入成功')



#发送通知短信
def senMsg(favorite):
    
   

    data = json.dumps(
        {
            'msgtype': 'markdown',
           
            'markdown':{
                'content': f'''
<font color="warning">{favorite.user.name}</font>
{favorite.text}
                '''
            },
           
        }
    )
    post(
        WECHAT_URL,
        data=data
    )



# 检查
def favorite():
    global statusId #注明是用全局 statusId
    favorite = api.GetHomeTimeline()[0]
    if favorite.id != statusId:
        statusId = favorite.id
        # upDateConfig()
        senMsg(favorite)



schedule.every(30).seconds.do(favorite)
while True:
    schedule.run_pending()