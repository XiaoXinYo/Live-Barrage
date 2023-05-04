/* Author: XiaoXinYo */

const HOST = 'ws://127.0.0.1:5000';
const TIME = 1000;

const WS = new WebSocket(HOST);

WS.onopen = function() {
    console.log('连接成功');
};

WS.onclose = function() {
    console.log('断开连接');
};

const welcomeObserver = new MutationObserver((mutationsList) => {
    brushPrompt = document.getElementById('brush-prompt');
    let spans = brushPrompt.getElementsByTagName('span');
    try {
        let nickname = '';
        let content = '';
        if (spans[0].getAttribute('class').indexOf('fans') === -1) {
            nickname = spans[0].innerHTML;
            content = spans[1].innerHTML;
        } else {
            nickname = spans[1].innerHTML;
            content = spans[2].innerHTML;
        }
        if (content.indexOf('进入') === -1) {
            return;
        }
        let barrage = {
            'type': 'welcome',
            'nickname': nickname,
            'content': content,
        };
        WS.send(JSON.stringify([barrage]));
    } catch (error) {
    }
    
});
welcomeObserver.observe(document.getElementById('brush-prompt'), {childList: true});

let barrageIds = [];
setInterval(function() {
    let barrageElements = document.getElementById('chat-items').children;
    let barrages = [];
    for (let barrageElementsIndex = 0; barrageElementsIndex < barrageElements.length; barrageElementsIndex++) {
        let barrageElement = barrageElements[barrageElementsIndex];
        
        let barrageId = '';
        let type = '';
        let userId = '';
        let nickname = '';
        let content = '';
        className = barrageElement.getAttribute('class');
        if (className === 'chat-item  convention-msg border-box') {
            barrageId = '0';
            type = 'system';
            nickname = '系统'
            content = barrageElement.innerHTML.replace(/<[^>]+>/g, '');
            content = content.replace(/\s+/g, '');
        } else if (className === 'chat-item important-prompt-item') {
            barrageId = '1';
            type = 'welcome';
            let nicknameElement = barrageElement.firstElementChild;
            nickname = nicknameElement.innerHTML;
            nickname = nickname.trimStart().trimEnd();

            let contentElement = barrageElement.lastElementChild;
            content = contentElement.innerHTML;
            content = content.trimStart().trimEnd();
        } else if (className.indexOf('chat-item danmaku-item') !== -1) {
            barrageId = barrageElement.getAttribute('data-ct');
            type = 'message';
            userId = barrageElement.getAttribute('data-uid');
            nickname = barrageElement.getAttribute('data-uname');
            content = barrageElement.getAttribute('data-danmaku');
        } else {
            continue;
        }

        let barrage = {
            'type': type,
            'userId': userId,
            'nickname': nickname,
            'content': content,
        };
        if (barrageIds.indexOf(barrageId) === -1) {
            barrages.push(barrage);
            barrageIds.push(barrageId);
            if (barrageIds.length > 300) {
                barrageIds.splice(0, 100);
            }
        }
    }
    
    if (barrages) {
        WS.send(JSON.stringify(barrages));
    }
}, TIME);