## 哔哩哔哩
### 介绍
通过请求官方API获取直播弹幕,使用WebSokcet向其他端传送弹幕.
### 需求
1. 环境: Python3.
2. 包: asyncio,websockets,requests,json.
### 配置
监测间隔(秒)在第78行修改.
### 方法
客户端连接WebSocket后发送直播网址或房间号.
## 抖音
### 介绍
通过浏览器运行JavaScript脚本获取直播弹幕,使用WebSokcet向其他端传送弹幕.
### 配置
1. WebSocket连接地址在第1行修改.
2. 监测间隔(毫秒)在第2行修改.
### 方法
先运行服务端,再在浏览器运行脚本.
### 示例(Tiktok/example/)
#### Python(barrage.py)
1. 环境: Python3.
2. 包: asyncio,websockets,json.
#### Java(java文件夹)
1. 环境: gradle.
2. 包: java-websocket,slf4j,fastjson.
## 快手
通过请求官方API获取直播弹幕,使用WebSokcet向其他端传送弹幕.
### 需求
1. 环境: Python3.
2. 包: asyncio,websockets,requests,json.
### 配置
监测间隔(秒)在第69行修改.
### 方法
客户端连接WebSocket后发送直播网址.