package com.github.coaixy;

import com.alibaba.fastjson.JSONObject;
import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;

import java.net.InetSocketAddress;

public class Socket extends WebSocketServer {
    Socket(int port){
        super(new InetSocketAddress(port));
    }
    @Override
    public void onOpen(WebSocket conn, ClientHandshake handshake) {

    }

    @Override
    public void onClose(WebSocket conn, int code, String reason, boolean remote) {

    }

    @Override
    public void onMessage(WebSocket conn, String message) {
        StringBuilder sb = new StringBuilder();
        sb.append(message);
        sb.delete(message.length()-1,message.length());
        sb.delete(0,23);
        message = sb.toString();

        JSONObject object = JSONObject.parseObject(message);
        String type = object.getString("type");
        String name = object.getString("username");
        String content = object.getString("content");
        if (type.equalsIgnoreCase("message")){
            System.out.println(name+":"+content);
        }
    }

    @Override
    public void onError(WebSocket conn, Exception ex) {

    }

    @Override
    public void onStart() {
        System.out.println("Server Start");
        setConnectionLostTimeout(100);
    }
}
