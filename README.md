## 哔哩哔哩
### 介绍
通过请求官方API获取直播弹幕,使用WebSokcet向其他端传送弹幕.
### 需求
1. 环境: Python3.
2. 包: asyncio,websockets,requests,json.
### 配置
1. WebSocket地址和端口分别在在第9行和第10行.
2. 监听间隔(毫秒)在第11行.
### 方法
客户端连接WebSocket后发送直播网址或房间号.
### 响应参数
名称|说明
---|---
user_id|用户ID
nickname|昵称
content|内容
timestmap|时间戳
## 抖音
### 介绍
通过浏览器运行JavaScript脚本获取直播弹幕,使用WebSokcet向其他端传送弹幕.
### 配置
1. WebSocket连接地址在第1行.
2. 监听间隔(毫秒)在第2行.
### 方法
先运行服务端,再在浏览器运行脚本.
### 响应参数
名称|说明
---|---
type|类型
nickname|昵称
user_level|用户等级
fan_club_name|粉丝团名称
fan_club_level|粉丝团等级
is_admin|是否为管理员
content|内容
gift_image_url|礼物图像网址
### 示例(Tiktok/example/)
## 斗鱼
### 介绍
通过浏览器运行JavaScript脚本获取直播弹幕,使用WebSokcet向其他端传送弹幕.
### 配置
1. WebSocket连接地址在第1行.
2. 监听间隔(毫秒)在第2行.
### 方法
先运行服务端,再在浏览器运行脚本.
名称|说明
---|---
user_id|用户ID
nickname|昵称
user_level|用户等级
is_admin|是否为管理员
content|内容
### 示例(参考抖音示例)
## 快手
通过请求官方API获取直播弹幕,使用WebSokcet向其他端传送弹幕.
### 需求
1. 环境: Python3.
2. 包: asyncio,websockets,requests,json.
### 配置
1. WebSocket地址和端口分别在在第9行和第10行.
2. 监听间隔(毫秒)在第11行.
### 方法
客户端连接WebSocket后发送直播网址.
### 响应参数
名称|说明
---|---
user_id|用户ID
nickname|昵称
content|内容
timestmap|时间戳