# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import asyncio
import websockets
import json

HOST = '127.0.0.1'
PORT = 5000

async def handle(websocket):
    print('连接成功')
    while True:
        data = await websocket.recv()
        data = json.loads(data)
        for data_count in data:
            print("{:10s} | {:10s} | {:10s}".format(data_count.get('type'), data_count.get('nickname'), data_count.get('content')))

async def run(websocket):
    while True:
        try:
            await handle(websocket)
        except websockets.ConnectionClosed:
            print('断开连接')
            break
       
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(websockets.serve(run, HOST, PORT))
    asyncio.get_event_loop().run_forever()