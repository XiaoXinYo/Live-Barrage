# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from typing import Union
import asyncio
import websockets
import requests
import json

HOST = '0.0.0.0'
PORT = 5000
TIME = 3000

def getMiddleText(text: str, textLeft: str='', textRight: str='') -> str:
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
    def __init__(self, liveStreamId: str) -> None:
        '''
        liveStreamId:直播流ID
        '''
        self.liveStreamId = liveStreamId
        self.session = requests.Session()

    def get(self) -> Union[bool, list]:
        data = self.session.get(f'https://livev.m.chenzhongtech.com/wap/live/feed?liveStreamId={self.liveStreamId}').text
        try:
            data = json.loads(data)
            data = json.loads(data)
        except Exception:
            return False
        
        liveStreamFeeds = data['liveStreamFeeds']
        barrages = []
        if liveStreamFeeds:
            for liveStreamFeed in liveStreamFeeds:
                barrage = {
                    'userId': liveStreamFeed['author']['userId'],
                    'nickname': liveStreamFeed['author']['userName'],
                    'content': liveStreamFeed['content'],
                    'timestmap': liveStreamFeed['time']
                }
                barrages.append(barrage)
        return barrages

async def handle(ws: websockets) -> None:
    url = await ws.recv()
    barrage = KwaiLiveBarrage(url)
    while True:
        barrages = barrage.get()
        if barrages:
            await ws.send(json.dumps(barrages, ensure_ascii=False))
        elif barrages == False:
            await ws.send('直播流ID错误')
            break
        await asyncio.sleep(TIME / 1000)

async def app(ws: websockets) -> None:
    while True:
        try:
            ipAddress = ws.remote_address[0]
            print(f'{ipAddress}:连接成功')
            await handle(ws)
        except websockets.ConnectionClosed:
            print(f'{ipAddress}:断开连接')
            break

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(websockets.serve(app, HOST, PORT))
    asyncio.get_event_loop().run_forever()