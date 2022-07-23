setInterval(function () {
        var webcast_chatroom = document.getElementsByClassName('webcast-chatroom___items')[0];
        var flex = webcast_chatroom.firstElementChild;
        var message_element = flex.getElementsByClassName('webcast-chatroom___item');
        var message = [];
        
        for (var message_element_count = 0;message_element_count < message_element.length;message_element_count++) {
            var single_message_element = message_element[message_element_count];
            
            var uid = message_element[message_element_count].getAttribute('data-id');
            var is_admin = false;
            var user_grade_level_url = '';
            var fan_club_leve_url = '';
            var gift_url = '';
            
            var original = single_message_element.innerHTML;
            
            var img_src = original.match(/src="([^"]*)"/g);
            if (img_src != null) {
                for(var img_src_count = 0;img_src_count < img_src.length;img_src_count++) {
                    src = img_src[img_src_count].replace('src=', '').replace('"', '');
                    if (src.indexOf('admin') != -1) {
                        is_admin = true;
                    } else if (src.indexOf('user_grade_level') != -1) {
                        user_grade_level_url = src;
                    } else if (src.indexOf('fansclub_level') != -1) {
                        fan_club_leve_url = src;
                    } else {
                        gift_url = src;
                    }
                }
            }
            
            original = original.replace(/<[^>]+>/g, '');
            original = original.trimStart().trimEnd();
            original = original.replace('&nbsp;×&nbsp;', '*');
            original = original.split('：');
            original_username = original[0];
            original_username = original_username.split('\n')
            if (original_username.length == 2) {
                var prefix = original_username[0];
                var username = original_username[1];
                username = username.trimStart().trimEnd();
            } else {
                var prefix = '';
                var username = original_username[0];
            }
            original.shift();
            var content = original.join('');
            
            var single_message = {
                'uid': uid,
                'is_admin': is_admin,
                'user_grade_level_url': user_grade_level_url,
                'fan_club_leve_url': fan_club_leve_url,
                'prefix': prefix,
                'username': username,
                'content': content,
                'gift_url': gift_url
            };
            message.push(single_message);
            single_message_element.remove();
        }
        
        console.log(message); 
    },3000)
