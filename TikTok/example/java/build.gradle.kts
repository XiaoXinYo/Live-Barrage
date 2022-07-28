plugins {
    id("java")
    id("application")
}
application{
    mainClassName = "com.github.coaixy.Main"
}

group = "com.github.coaixy"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter-api:5.8.1")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.8.1")
    // https://mvnrepository.com/artifact/org.java-websocket/Java-WebSocket
    implementation("org.slf4j:slf4j-simple:1.7.36")
    implementation("org.java-websocket:Java-WebSocket:1.5.3")
    // https://mvnrepository.com/artifact/com.alibaba/fastjson
    implementation("com.alibaba:fastjson:2.0.10")



}
tasks.getByName<Test>("test") {
    useJUnitPlatform()
}