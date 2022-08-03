from api_rubika import Bot
from text import texts

bot = Bot("auth")
# در قسمت auth توکن یا شناسه اکانت خود را وارد کنید !


"""
	Telegram me : @A_ABOL
	Github : https://github.com/abolX 
	Rubika : @electro_bot
	هر گونه کپی برداری و استفاده به نام خود حرام است !
"""

answered = []
def hasSwear(Msg):
	swData = [False,None]
	Msg = ''.join(filter(str.isalpha, Msg)).replace("-", "")
	for i in open("swear_file.txt").read().split("\n"):
		if i in Msg:
			swData = [True, i]
			break
		else: continue
	return swData

while True:
	try:
		
		for msg in bot.update():
			
			if msg["abs_object"]["type"] == "User":
				
				if msg["last_message"]["text"] and not msg["last_message"]["message_id"] in answered:
					
					
					if msg["last_message"]["text"] in ["start","/start","!start"]:
						try:
							guid = msg["last_message"]["author_object_guid"]
							name = bot.get_user_info(guid)["data"]["user"]["first_name"]
							
							if not guid in open('guids.txt', 'r').read().split('\n'):
								bot.send_message(guid, "سلام " + name + texts.txt_welcome)
								
								with open('guids.txt', 'a') as f:
									f.write('\n' + guid)
							else:
								bot.send_message(guid, "سلام " + name + " عزیز 🌹")
						except:
							bot.send_message(guid, texts.txt_error)
							
							
					elif msg["last_message"]["text"] in ["help","/help","!help"]:
						try:
							guid = msg["last_message"]["author_object_guid"]
							bot.send_message(guid, texts.txt_help)
						except:
							bot.send_message(guid, texts.txt_error)
							
							
					elif msg["last_message"]["text"].startswith("@"):
						try:
							guid = msg["last_message"]["author_object_guid"]
							if not hasSwear(" ".join(msg["last_message"]["text"].split(" ")[1:]))[0]:
								
								check = bot.get_username_info(msg["last_message"]["text"].split(" ")[0][1:])["data"]
								if check["exist"] == True:
									
									if check["type"] == "User":
										user = check["user"]
										
										if user["user_guid"] in open('guids.txt', 'r').read().split('\n'):
											bot.send_message(guid, "پیام شما به " + user.get('first_name') + " ارسال شد ✅")
											bot.send_message(user["user_guid"],  "سلام " + user.get('first_name') + " پیام ناشناس داری😃!" + " ".join(msg["last_message"]["text"].split(" ")[1:]))
										
										else: 
											bot.send_message(guid, texts.txt_not_join)
									else:
										bot.send_message(guid, texts.txt_is_channel)
								else:
									bot.send_message(guid, texts.txt_not_exist)
							else:
								bot.send_message(guid, texts.txt_has_swear)
						except:
							bot.send_message(guid, texts.txt_error)
					
					answered.append(msg["last_message"]["message_id"])
					
	except: pass
