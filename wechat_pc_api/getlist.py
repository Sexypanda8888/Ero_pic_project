from __future__ import unicode_literals

import wechat
import json
import time
from wechat import WeChatManager, MessageType
import os 
wechat_manager = WeChatManager(libs_path='./libs')

# @wechat.CONNECT_CALLBACK(in_class=False)
# def on_connect(client_id):
#     print('[on_connect] client_id: {0}'.format(client_id))
# @wechat.RECV_CALLBACK(in_class=False)
# def on_recv(client_id, message_type, message_data):
#     print('[on_recv] client_id: {0}, message_type: {1}, message:{2}'.format(client_id,
#                                                                             message_type, json.dumps(message_data,ensure_ascii=False)))

class LoginTipBot(wechat.CallbackHandler):
    @wechat.RECV_CALLBACK(in_class=True)
    def on_message(self, client_id, message_type, message_data):
        if message_type ==11025 :
            wechat_manager.get_chatrooms(client_id)
        if message_type == MessageType.MT_DATA_CHATROOMS_MSG:
            print(message_data)
if __name__ == "__main__":
    bot = LoginTipBot()

    # 添加回调实例对象
    wechat_manager.add_callback_handler(bot)
    wechat_manager.manager_wechat(smart=True)

    # 阻塞主线程
    while True:
        time.sleep(0.5)
