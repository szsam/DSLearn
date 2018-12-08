# 放到 ~/.qqbot-tmp/plugins/ 目录下
# （ ~ 代表用户主目录， win7 下为 C:\Users\xxx ），
# 或系统中可以 import 到的目录下
# （如 python 的安装目录下的 Lib/site-packages 目录）

import socket


def onQQMessage(bot, contact, member, content):
    if bot.isMe(contact, member):
        print('自己的消息')
        return
    print("contact qq：" + contact.qq)
    sk = socket.socket()
    sk.connect((socket.gethostname(), 8080))
    sk.send(content.encode('utf-8'))

    # data = sk.recv(1024).decode('utf-8')
    # if data is None:
    #		data = "无判断"
    # bot.SendTo(contact, data)

    sk.close()