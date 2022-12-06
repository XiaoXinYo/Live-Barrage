const HOST = 'ws://127.0.0.1:5000';
const TIME = 1000;

const ws = new WebSocket(HOST);

ws.onopen = function() {
    console.log('连接成功');
};

ws.onclose = function() {
    console.log('断开连接');
};

let barrageIds = [];
setInterval(function() {
    let webcastChatroom = document.getElementsByClassName('webcast-chatroom___items')[0];
    let barrageElements = webcastChatroom.getElementsByClassName('webcast-chatroom___item');
    let barrages = [];
    for (let barrageElementsIndex = 0; barrageElementsIndex < barrageElements.length; barrageElementsIndex++) {
        let barrageElement = barrageElements[barrageElementsIndex];

        let id = barrageElement.getAttribute('data-id');
        let type = '';
        
        let original = barrageElement.innerHTML;
        
        let nickname = '';
        let content = '';
        originalText = original.replace(/">(\S*)<\/span><\/div><\/span>/g, '');
        originalText = originalText.replace(/<[^>]+>/g, '');
        originalText = originalText.trimStart().trimEnd();
        if (originalText.indexOf('欢迎来到直播间') === -1) {
            if (barrageElement.getAttribute('style') === 'background-color: transparent;') {
                type = 'welcome';
                originalText = originalText.split(' ');
            } else {
                if (originalText.indexOf('&nbsp;×&nbsp;') !== -1) {
                    continue;
                }
                type = 'message';
                originalText = originalText.split('：');
            }
            nickname = originalText[0];
            nickname = nickname.trimStart().trimEnd();
            originalText.shift();
            content = originalText.join('');
        } else {
            type = 'system';
            nickname = '系统';
            content = originalText;
        }
        
		let emoticons = original.match(/alt="([^"]*)"/g);
		let emoticon = '';
		if (emoticons !== null) {
		    for (let emoticonsIndex = 0; emoticonsIndex < emoticons.length; emoticonsIndex++) {
		        emoticon += emoticons[emoticonsIndex].replace('alt="', '').replace('"', '');
		    }
		}
		content += emoticon;
		
        let barrage = {
            'type': type,
            'nickname': nickname,
            'content': content,
        };
        
        if (barrageIds.indexOf(id) === -1) {
            barrages.push(barrage);
            barrageIds.push(id);
            if (barrageIds.length > 300) {
                barrageIds.splice(0, 100);
            }
        }
    }
    
    if (barrages) {
        ws.send(JSON.stringify(barrages));
    }
}, TIME);