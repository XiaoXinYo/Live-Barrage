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
    let barrageElements = document.getElementsByClassName('Barrage-listItem');
    let barrages = [];
    for (let barrageElementsIndex = 0; barrageElementsIndex < barrageElements.length; barrageElementsIndex++) {
        let barrageElement = barrageElements[barrageElementsIndex];
        
        let barrageId = barrageElement.getAttribute('id');
        let barrageDiv = barrageElement.firstElementChild;
        
        let type = '';
        let userId = '';
        let nickname = '';
        let content = '';
        if (barrageDiv.getAttribute('class') === 'Barrage-icon Barrage-icon--sys') {
            type = 'system';
            nickname = '系统'
            content = barrageElement.innerHTML.replace(/<[^>]+>/g, '');
            content = content.replace(/\s+/g, '');
        } else {
            let userElement = barrageDiv.getElementsByClassName('Barrage-nickName')[0];
            nickname = userElement.getAttribute('title');
            
            let contentElement = barrageDiv.getElementsByClassName('Barrage-text');
            if (contentElement.length === 1) {
				content = contentElement[0].innerHTML;
				content = content.replace(/<[^>]+>/g, '');
				content = content.trimStart().trimEnd();
				
				if (content.indexOf('赠送给主播') === -1) {
					type = 'welcome';
				} else {
					continue;
				}
            } else {
                type = 'message';
                userId = userElement.getAttribute('data-uid');
                
                contentElement = barrageDiv.getElementsByClassName('Barrage-content')[0];
                content = contentElement.firstChild.nodeValue;
                content = content.trimStart().trimEnd();
				
				let emoticons = contentElement.innerHTML.match(/rel="([^"]*)"/g);
				let emoticon = '';
				if (emoticons !== null) {
				    for (let emoticonsIndex = 0; emoticonsIndex < emoticons.length; emoticonsIndex++) {
				        emoticon += `[${emoticons[emoticonsIndex].replace('rel="', '').replace('"', '')}]`;
				    }
				}
				content += emoticon;
            }
        }
        
        let barrage = {
            'type': type,
            'userId': userId,
            'nickname': nickname,
            'content': content
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