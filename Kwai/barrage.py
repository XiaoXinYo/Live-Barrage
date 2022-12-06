# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import asyncio
import websockets
import requests
import json

HOST = '0.0.0.0'
PORT = 5000
TIME = 3000

def getMiddleText(text, textLeft='', textRight=''):
    try:
        if not textLeft:
            return text.split(textRight)[1]
        elif not textRight:
            return text.split(textLeft)[1]
        data = text.split(textLeft)[1].split(textRight)[0]
    except Exception:
        data = ''
    return data

class KwaiLiveBarrage:
    def __init__(self, url):
        '''
        url:直播网址
        '''
        self.url = url
        self._getLiveStreamId()
    
    def _getLiveStreamId(self):
        headers = {
            'Cookie': 'clientid=3; did=web_0ab029d675a4c9df087e3c7f6873e556; client_key=65890b29; ksliveShowClipTip=true',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58'
        }
        data = requests.get(self.url, headers=headers).text
        self.liveStreamId = getMiddleText(data, '"liveStreamId":"' , '","caption')

    def get(self):
        data = requests.get(f'https://livev.m.chenzhongtech.com/wap/live/feed?liveStreamId={self.liveStreamId}').text
        try:
            data = json.loads(data)
            data = json.loads(data)
        except Exception:
            return False
        data = data.get('liveStreamFeeds')
        
        barrages = []
        if data:
            for dataItem in data:
                author = dataItem.get('author')
                barrage = {
                    'userId': author.get('userId'),
                    'nickname': author.get('userName'),
                    'content': dataItem.get('content'),
                    'timestmap': dataItem.get('time')
                }
                barrages.append(barrage)
        return barrages

async def handle(websocket):
    url = await websocket.recv()
    barrage = KwaiLiveBarrage(url)
    while True:
        barrages = barrage.get()
        if barrages:
            await websocket.send(json.dumps(barrages, ensure_ascii=False))
        elif barrages == False:
            await websocket.send('直播网址错误')
            break
        await asyncio.sleep(TIME / 1000)

async def run(websocket):
    while True:
        try:
            print('连接成功')
            await handle(websocket)
        except websockets.ConnectionClosed:
            print('断开连接')
            break

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(websockets.serve(run, HOST, PORT))
    asyncio.get_event_loop().run_forever()