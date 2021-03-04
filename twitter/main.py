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
    try:
        data = api.GetStatus(favorite.id).text
        print("get one status now, msg: ", data)
        
        data = json.dumps(
            {
                'msgtype': 'markdown',
            
                'markdown':{
                    'content': f'''
<font color="warning">{favorite.user.name}</font>
{data}
                    '''
                },
            
            }
        )

        post(
            WECHAT_URL,
            data=data
        )

    except Exception as e:
        console.log("Error senMsg, err: ", e)



# 检查
def favorite():
    global statusId #注明是用全局 statusId

    try:
        favorite = api.GetHomeTimeline(count=5)
        print(favorite)

        for one in favorite:
            if str(one.id) != str(statusId):
                senMsg(one)
            else:
                break

        statusId = favorite[0].id
        upDateConfig()
    
    except Exception as e:
        console.log("Error get favorite, err: ", e)


# 定时执行，twitter限制为每分钟1次调用
schedule.every(120).seconds.do(favorite)

while True:
    schedule.run_pending()