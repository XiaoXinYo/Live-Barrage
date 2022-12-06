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

class BilibiliLiveBarrage:
    def __init__(self, signature):
        '''
        signature:直播网址或房间号
        '''
        self.signature = signature
        self._getRoomId()
        self.barrageIds = []
    
    def _getRoomId(self):
        if 'live.bilibili.com' in self.signature:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58'
            }
            liveData = requests.get(self.signature, headers=headers).text
            self.roomId = getMiddleText(liveData, 'defaultRoomId":"' , '","roomsNum"')
        else:
            self.roomId = self.signature
    
    def get(self):
        data = requests.get(f'https://api.live.bilibili.com/ajax/msg?roomid={self.roomId}').text
        if 'HistoryReq.Roomid' in data:
            return False
        data = json.loads(data)
        data = data.get('data').get('admin') + data.get('data').get('room')
        
        barrages = []
        if data:
            for dataItem in data:
                if dataItem.get('emoticon').get('id') == 0:
                    content = dataItem.get('text')
                else:
                    content = f'[{dataItem.get("text")}]'
                
                checkInfo = dataItem.get('check_info')
                
                barrage = {
                    'userId': dataItem.get('uid'),
                    'nickname': dataItem.get('nickname'),
                    'content': content,
                    'timestamp': checkInfo.get('ts')
                }

                if checkInfo.get('ct') not in self.barrageIds:
                    barrages.append(barrage)
                    self.barrageIds.append(checkInfo.get('ct'))
                    if len(self.barrageIds) > 300:
                        del self.barrageIds[0: 100]
        return barrages

async def handle(websocket):
    signature = await websocket.recv()
    barrage = BilibiliLiveBarrage(signature)
    while True:
        barrages = barrage.get()
        if barrages:
            await websocket.send(json.dumps(barrages, ensure_ascii=False))
        elif barrages == False:
            await websocket.send('直播网址或房间号错误')
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