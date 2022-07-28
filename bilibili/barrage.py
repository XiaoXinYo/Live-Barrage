# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import asyncio
import websockets
import requests
import json

async def handle(websocket):
    print('连接成功')
    room_id = await websocket.recv()
    id_d = []
    while True:
        data = requests.get(f'https://api.live.bilibili.com/ajax/msg?roomid={room_id}').text
        data = json.loads(data)
        data = data.get('data').get('admin') + data.get('data').get('room')
        if data:
            barrage = []
            for data_count in data:
                if data_count.get('emoticon').get('id') == 0:
                    content = data_count.get('text')
                else:
                    content = f'[{data_count.get("text")}]'
                check_info = data_count.get('check_info')
                single_barrage = {
                  'uid': data_count.get('uid'),
                  'nickname': data_count.get('nickname'),
                  'content': content,
                  'timestamp': check_info.get('ts')
                }
                if check_info.get('ct') not in id_d:
                    barrage.append(single_barrage)
                    id_d.append(check_info.get('ct'))
                    if len(id_d) > 300:
                        del id_d[0: 100]
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