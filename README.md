## 哔哩哔哩
### 介绍
请求官方API获取直播弹幕,使用WebSocket向客户端发送弹幕.
### 需求
1. 语言: Python.
2. 包: asyncio,websockets,requests.
### 配置
1. WebSocket地址和端口分别在第9行和第10行.
2. 监听间隔(毫秒)在第11行.
### 方法
客户端连接WebSocket后发送直播网址/房间号.
### 响应参数
名称|说明
---|---
userId|用户ID
nickname|昵称
content|内容
timestmap|时间戳
### 示例(Bilibili/example/)
## 抖音
### 介绍
通过浏览器运行JavaScript脚本获取直播弹幕,使用WebSocket向服务端发送弹幕.
### 配置
1. WebSocket地址在第1行.
2. 监听间隔(毫秒)在第2行.
### 方法
先运行服务端,再运行脚本.
### 响应参数
名称|说明
---|---
type|类型,system代表系统,welcome代表欢迎,message代表消息
nickname|昵称
content|内容
### 示例(Tiktok/example/)
## 斗鱼
### 介绍
通过浏览器运行JavaScript脚本获取直播弹幕,使用WebSocket向服务端发送弹幕.
### 配置
1. WebSocket地址在第1行.
2. 监听间隔(毫秒)在第2行.
### 方法
先运行服务端,再运行脚本.
名称|说明
---|---
type|类型,system代表系统,welcome代表欢迎,message代表消息
userId|用户ID
nickname|昵称
content|内容
### 示例(参考抖音示例)
## 快手
请求官方API获取直播弹幕,使用WebSocket向客户端发送弹幕.
### 需求
1. 语言: Python.
2. 包: asyncio,websockets,requests,json.
### 配置
1. WebSocket地址和端口分别在第9行和第10行.
2. 监听间隔(毫秒)在第11行.
### 方法
客户端连接WebSocket后发送直播流ID(查看页面源代码,搜索liveStreamId).
### 响应参数
名称|说明
---|---
userId|用户ID
nickname|昵称
content|内容
timestmap|时间戳
### 示例(参考哔哩哔哩示例)