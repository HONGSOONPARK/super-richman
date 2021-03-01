from datetime import datetime

print(datetime.today().strftime("%Y%m%d%H%M%S"))

import telegram

# stoneheadcoding , @daegalibot
# 텔레그램 토큰
telgm_token = '1635387024:AAEQfnk-F5A274EmpY1SSFY8bPYJbdULf2g'

bot = telegram.Bot(token = telgm_token)
# 머리돌 채널 ID  : -1001280712219

# updates = bot.getUpdates()

# print(updates)

# for i in updates:
#     print(i)

# print('start telegram chat bot')




# 테이블 조회
def telgm_bot_send_msg(id, msg):
    bot.sendMessage(chat_id = id, text=msg)
    