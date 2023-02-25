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
        text_ = text.split(textLeft)[1].split(textRight)[0]
    except Exception:
        text_ = ''
    return text_

class KwaiLiveBarrage:
    def __init__(self, liveStreamId):
        '''
        liveStreamId:直播流ID
        '''
        self.liveStreamId = liveStreamId

    def get(self):
        data = requests.get(f'https://livev.m.chenzhongtech.com/wap/live/feed?liveStreamId={self.liveStreamId}').text
        try:
            data = json.loads(data)
            data = json.loads(data)
        except Exception:
            return False
        liveStreamFeeds = data.get('liveStreamFeeds')
        
        barrages = []
        if liveStreamFeeds:
            for liveStreamFeed in liveStreamFeeds:
                barrage = {
                    'userId': liveStreamFeed.get('author').get('userId'),
                    'nickname': liveStreamFeed.get('author').get('userName'),
                    'content': liveStreamFeed.get('content'),
                    'timestmap': liveStreamFeed.get('time')
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
            await websocket.send('直播流ID错误')
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