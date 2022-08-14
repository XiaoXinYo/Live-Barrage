# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import asyncio
import websockets
import requests
import json

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

class Kwai_Live_Barrage:
    def __init__(self, url):
        '''
        url:直播网址
        '''
        self.url = url
        self._get_live_stream_id()
    
    def _get_live_stream_id(self):
        header = {}
        header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58'
        data = requests.get(self.url, headers=header).text
        self.live_stream_id = get_middle_text(data, '"liveStreamId":"' , '","caption')

    def get(self):
        data = requests.get(f'https://livev.m.chenzhongtech.com/wap/live/feed?liveStreamId={self.live_stream_id}').text
        try:
            data = json.loads(data)
            data = json.loads(data)
        except Exception:
            return '直播流ID错误'
        data = data.get('liveStreamFeeds')
        barrage = []
        if data:
            for data_count in data:
                author = data_count.get('author')
                single_brrage = {
                    'user' : {
                        'id': author.get('userId'),
                        'name': author.get('userName'),
                        'head_url': author.get('headurl')
                    },
                    'content': data_count.get('content'),
                    'timestmap': data_count.get('time')
                }
                barrage.append(single_brrage)
        return barrage

async def handle(websocket):
    print('连接成功')
    url = await websocket.recv()
    barrage = Kwai_Live_Barrage(url)
    while True:
        barrage_data = barrage.get()
        if barrage_data:
            if barrage_data == '直播流ID错误':
                await websocket.send('直播流ID错误')
                break
            await websocket.send(json.dumps(barrage_data, ensure_ascii=False))
        await asyncio.sleep(3)

async def run(websocket):
    while True:
        try:
            await handle(websocket)
        except websockets.ConnectionClosed:
            print('断开连接')
            break

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(websockets.serve(run, '127.0.0.1', 5000))
    asyncio.get_event_loop().run_forever()