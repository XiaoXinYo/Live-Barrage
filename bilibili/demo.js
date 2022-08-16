let ADDRES = "ws://127.0.0.1:5000"

let ws = new WebSocket(ADDRES)
ws.onopen = function() {
	console.log("连接成功")
	ws.send("8224637")
}
ws.onmessage = function(e) {
	console.log(e.data)
}