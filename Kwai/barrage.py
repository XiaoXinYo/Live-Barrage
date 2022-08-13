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

async def handle(websocket):
    print('连接成功')
    url = await websocket.recv()
    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58'
    live_data = requests.get(url, headers=header).text
    live_stream_id = get_middle_text(live_data, '"liveStreamId":"' , '","caption')
    while True:
        data = requests.get(f'https://livev.m.chenzhongtech.com/wap/live/feed?liveStreamId={live_stream_id}').text
        try:
            data = json.loads(data)
            data = json.loads(data)
        except Exception:
            await websocket.send('直播流ID错误')
            break
        data = data.get('liveStreamFeeds')
        if data:
            barrage = []
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
            if barrage:
                await websocket.send(json.dumps(barrage, ensure_ascii=False))
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