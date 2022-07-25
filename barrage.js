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
    var webcast_chatroom = document.getElementsByClassName('webcast-chatroom___items')[0];
    var barrage_element = webcast_chatroom.getElementsByClassName('webcast-chatroom___item');
    var barrage = {};
    
    for (var barrage_element_count = 0; barrage_element_count < barrage_element.length; barrage_element_count++) {
        var single_barrage_element = barrage_element[barrage_element_count];

        var id = barrage_element[barrage_element_count].getAttribute('data-id');
        var type = 'message';
        
        var original = single_barrage_element.innerHTML;
        
        var prefix = '';
        original_prefix = original.match(/">(\S*)<\/span><\/div><\/span>/g);
        if (original_prefix != null) {
            prefix = original_prefix[0];
            prefix = prefix.replace(/<[^>]+>/g, '');
            prefix = prefix.trimStart().trimEnd();
            prefix = prefix.replace('">', '');
        }
        
        var username = '';
        var content = '';
        original_text = original.replace(/">(\S*)<\/span><\/div><\/span>/g, '');
        original_text = original_text.replace(/<[^>]+>/g, '');
        original_text = original_text.trimStart().trimEnd();
        if (original_text.indexOf('欢迎来到直播间') == -1) {
            if (single_barrage_element.getAttribute('style') == 'background-color: transparent;') {
                type = 'welcome';
                original_text = original_text.split(' ');
            } else {
                original_text = original_text.replace('&nbsp;×&nbsp;', '*');
                original_text = original_text.split('：');
            }
            username = original_text[0];
            username = username.trimStart().trimEnd();
            original_text.shift();
            content = original_text.join('');
        } else {
            type = 'system';
            username = '系统消息';
            content = original_text;
        }
        
        var original_emoticon = original.match(/alt="([^"]*)"/g);
        var emoticon = '';
        if (original_emoticon != null) {
            for (var original_emoticon_count = 0;original_emoticon_count < original_emoticon.length; original_emoticon_count++) {
                single_original_emoticon = original_emoticon[original_emoticon_count].replace('alt="', '').replace('"', '');
                if (single_original_emoticon != '') {
                    emoticon += single_original_emoticon;
                }
            }
        }
        
        content += emoticon;
        
        var is_admin = false;
        var user_grade_level = '';
        var fan_club_leve = '';
        var gift_image_url = '';
        var img_src = original.match(/src="([^"]*)"/g);
        if (img_src != null) {
            for (var img_src_count = 0; img_src_count < img_src.length; img_src_count++) {
                single_img_src = img_src[img_src_count].replace('src="', '').replace('"', '');
                if (single_img_src.indexOf('admin') != -1) {
                    is_admin = true;
                } else if (single_img_src.indexOf('user_grade_level') != -1) {
                    user_grade_level = single_img_src.match(/_[1-9]\d*.png/g)[0];
                    user_grade_level = user_grade_level.replace('_', '').replace('.png', '')
                } else if (single_img_src.indexOf('fansclub') != -1) {
                    fan_club_leve = single_img_src.match(/_[1-9]\d*.png/g)[0];
                    fan_club_leve = fan_club_leve.replace('_', '').replace('.png', '')
                } else {
                    if (content.indexOf('送出了') != -1) {
                        type = 'gift';
                        gift_image_url = single_img_src;
                    }
                }
            }
        }
        
        var single_barrage = {
            'type': type,
            'is_admin': is_admin,
            'user_grade_level': user_grade_level,
            'fan_club_leve': fan_club_leve,
            'prefix': prefix,
            'username': username,
            'content': content,
            'gift_image_url': gift_image_url
        };
        barrage[id] = single_barrage;
    }

    for (barrage_count in barrage) {
        if (barrage_id.indexOf(barrage_count) != -1) {
            delete(barrage[barrage_count]);
        } else {
            barrage_id.push(barrage_count);
            if (barrage_id.length > 300) {
                barrage_id.splice(0, 100)
            }
        }
    }
    
    barrage_json = JSON.stringify(barrage);
    if (barrage_json != '{}') {
        console.log(barrage);
        ws.send(barrage_json);
    }
}, TIME);