package com.github.coaixy;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello world!");
        Socket server = new Socket(5000);
        server.run();
    }
}