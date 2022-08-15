var ADDRESS = 'ws://127.0.0.1:5000';
var TIME = 1000;

var ws = new WebSocket(ADDRESS);
ws.onopen = function() {
    console.log('连接成功');
};

ws.onclose = function() {
    console.log('断开连接');
};

var barrage_id = [];
setInterval(function() {
    var barrage_element = document.getElementsByClassName('Barrage-listItem');
    var barrage = [];
    for (var barrage_element_count = 0; barrage_element_count < barrage_element.length; barrage_element_count++) {
        var single_barrage_element = barrage_element[barrage_element_count];
        
        var id = single_barrage_element.getAttribute('id');
        var type = '';
        
        var barrage_div = single_barrage_element.firstElementChild;
        
        var user_level = '';
        var user_id = '';
        var nickname = '';
        var is_admin = false;
        var content = '';
        if (barrage_div.getAttribute('class') == 'Barrage-icon Barrage-icon--sys') {
            type = 'system';
            nickname = '系统'
            content = single_barrage_element.innerHTML.replace(/<[^>]+>/g, '');
            content = content.trimStart().trimEnd();
        } else {
            var user_level_element = barrage_div.getElementsByClassName('js-user-level')[0];
            user_level = user_level_element.getAttribute('title');
            user_level = user_level.replace('用户等级：', '');
            
            var username_element = barrage_div.getElementsByClassName('Barrage-nickName')[0];
            user_id = nickname_element.getAttribute('data-uid');
            nickname = nickname_element.getAttribute('title');
            
            if (barrage_div.getElementsByClassName('Barrage-icon--roomAdmin').length > 0) {
                is_admin = true;
            }
            
            var content_element = barrage_div.getElementsByClassName('Barrage-text');
            if (content_element.length == 0) {
                type = 'message';
                content_element = barrage_div.getElementsByClassName('Barrage-content')[0];
                content = content_element.firstChild.nodeValue;
                content = content.trimStart().trimEnd();
            } else {
                type = 'welcome';
                content_element = content_element[0];
                content = content_element.firstChild.nodeValue;
                content = content.trimStart().trimEnd();
            }
        }
        
        var single_barrage = {
            'type': type,
            'user_id': user_id,
            'nickname': nickname,
            'user_level': user_level,
            'is_admin': is_admin,
            'content': content
        };
        
        if (barrage_id.indexOf(id) == -1) {
            barrage.push(single_barrage);
            barrage_id.push(id);
            if (barrage_id.length > 300) {
                barrage_id.splice(0, 100);
            }
        }
    }
    
    barrage_json = JSON.stringify(barrage);
    if (barrage_json != '{}') {
        console.log(barrage);
        ws.send(barrage_json);
    }
}, TIME);