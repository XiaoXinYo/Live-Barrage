## 哔哩哔哩
### 介绍
通过请求哔哩哔哩官方API获取抖音直播弹幕,使用WebSokcet向其他端传送弹幕.
### 配置
监测间隔(秒)在第38行修改.
### 方法
客户端连接WebSocket后发送房间号.
## 抖音
### 介绍
通过浏览器运行JavaScript脚本获取抖音直播弹幕,使用WebSokcet向其他端传送弹幕.
### 配置
1. WebSocket连接地址在第1行修改.
2. 监测间隔(毫秒)在第2行修改.
### 示例(Tiktok/example/)
#### Python(barrage.py)
1. 环境: Python3.
2. 包: asyncio,websockets,json.
#### Java(java文件夹)
1. 环境: gradle.
2. 包: java-websocket,slf4j,fastjson.