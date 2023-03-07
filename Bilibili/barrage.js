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
        } else {
            barrageId = barrageElement.getAttribute('data-ct');
            type = 'message';
            userId = barrageElement.getAttribute('data-uid');
            nickname = barrageElement.getAttribute('data-uname');
            content = barrageElement.getAttribute('data-danmaku');
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