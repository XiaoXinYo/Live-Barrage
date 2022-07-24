# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import asyncio
import websockets
import json 

async def receive(websocket):
    while True:
        data = await websocket.recv()
        data = json.loads(data)
        for data_count in data:
            single_data = data[data_count]
            print(f"{data_count} | {single_data.get('type')} | {single_data.get('prefix')} | {single_data.get('username')}: {single_data.get('content')}")

async def run(websocket):
    while True:
        try:
            await receive(websocket)
        except websockets.ConnectionClosed:
            print("断开连接")
            break
       
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(websockets.serve(run, "127.0.0.1", 5000))
    asyncio.get_event_loop().run_forever()
