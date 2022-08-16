# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import asyncio
import websockets
import requests
import json

ADDRESS = '0.0.0.0'
PORT = 5000
TIME = 3000

def get_middle_text(text, text_left='', text_right=''):
    try:
        if not text_left:
            return text.split(text_right)[1]
        elif not text_right:
            return text.split(text_left)[1]
        data = text.split(text_left)[1].split(text_right)[0]
    except Exception:
        data = ''
    return data

class Bilibili_Live_Barrage:
    def __init__(self, signature):
        '''
        signature:直播网址或房间号
        '''
        self.signature = signature
        self._get_room_id()
        self.id = []
    
    def _get_room_id(self):
        if 'live.bilibili.com' in self.signature:
            header = {}
            header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58'
            live_data = requests.get(self.signature, headers=header).text
            self.room_id = get_middle_text(live_data, 'defaultRoomId":"' , '","roomsNum"')
        else:
            self.room_id = self.signature
    
    def get(self):
        data = requests.get(f'https://api.live.bilibili.com/ajax/msg?roomid={self.room_id}').text
        if 'HistoryReq.Roomid' in data:
            return '直播网址或房间号错误'
        data = json.loads(data)
        data = data.get('data').get('admin') + data.get('data').get('room')
        barrage = []
        if data:
            for data_count in data:
                if data_count.get('emoticon').get('id') == 0:
                    content = data_count.get('text')
                else:
                    content = f'[{data_count.get("text")}]'
                check_info = data_count.get('check_info')
                single_barrage = {
                    'user_id': data_count.get('uid'),
                    'nickname': data_count.get('nickname'),
                    'content': content,
                    'timestamp': check_info.get('ts')
                }
                if check_info.get('ct') not in self.id:
                    barrage.append(single_barrage)
                    self.id.append(check_info.get('ct'))
                    if len(self.id) > 300:
                        del self.id[0: 100]
        return barrage

async def handle(websocket):
    print('连接成功')
    signature = await websocket.recv()
    barrage = Bilibili_Live_Barrage(signature)
    while True:
        barrage_data = barrage.get()
        if barrage_data:
            if barrage_data == '直播网址或房间号错误':
                await websocket.send('直播网址或房间号错误')
                break
            await websocket.send(json.dumps(barrage_data, ensure_ascii=False))
        await asyncio.sleep(TIME / 1000)

async def run(websocket):
    while True:
        try:
            await handle(websocket)
        except websockets.ConnectionClosed:
            print('断开连接')
            break

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(websockets.serve(run, ADDRESS, PORT))
    asyncio.get_event_loop().run_forever()