from api_rubika import Bot
from text import texts
from separate_file import *

bot = Bot("auth")
# در قسمت auth توکن یا شناسه اکانت خود را وارد کنید !

max = 5
# با تغییر عدد می تونید تعدادی که کاربر می تونه اخطار دریافت کنه رو مشخص کنید !

# Creator : https://github.com/abolX
# Rubika : @elctro_bot

def alert(guid):
	with open('alert_list.txt','a') as f:
		f.write('\n' + guid)
	alert_count = open('alert_list.txt','r').read().split('\n').count(guid)
	
	if alert_count == max :
		return bot.block(guid)
	
	for i in range(max):
		extra = i + 1
		if alert_count == extra :
			return bot.send_message(guid, f'‼️ شما [{extra}/{max}] اخطار دریافت کردید\n\nلطفا از کلمات فیلتر استفاده نکنید در صورت گرفتن {max} اخطار بلاک خواهید شد !')

def send_to_group(guid, message, message_id):
	try:
		if len(message.split()) == 1 :
			return bot.send_message(guid, texts.txt_not_text, message_id)
		
		if hasSwear(" ".join(message.split()[1:]))[0] :
			return alert(guid)
			
		group_info = bot.join_group(message.split()[0])
		
		if group_info["status"] == "ERROR_GENERIC" :
			if group_info["status_det"] == "INVALID_AUTH" :
				return bot.send_message(guid, texts.txt_bot_removed, message_id)
			else:
				return bot.send_message(guid, texts.txt_not_exist_gp, message_id)
			
		if not "SendMessages" in group_info["data"]["chat_update"]["chat"]["access"] :
			bot.leave_group(group_info["data"]["group"]["group_guid"])
			return bot.send_message(guid, texts.txt_not_send_message_gp, message_id)
			
		bot.send_message(guid, "پیام شما به گروه " + group_info["data"]["group"]["group_title"] + " ارسال شد ✅", message_id)
		
		bot.send_message(group_info["data"]["group"]["group_guid"], texts.txt_send_group + " ".join(message.split()[1:]) + texts.txt_send_group2)
		
		bot.leave_group(group_info["data"]["group"]["group_guid"])
	except:
		bot.send_message(guid, texts.txt_error, message_id)

def send_with_guid(guid, message, message_id):
	try:
		if len(message.split()) == 1 :
			return bot.send_message(guid, texts.txt_not_text, message_id)
		
		if hasSwear(" ".join(message.split()[1:]))[0] :
			return alert(guid)

		user_info = bot.get_user_info(message.split()[0])
		
		if user_info["status"] == "ERROR_GENERIC" :
			return bot.send_message(guid, texts.txt_guid_not_exist, message_id)
			
		if not "SendMessages" in user_info["data"]["chat"]["access"] :
			return bot.send_message(guid, texts.txt_bot_is_block, message_id)
			
		user = user_info["data"]["user"]
		
		if not user["user_guid"] in open('guids.txt', 'r').read().split('\n'):
			return bot.send_message(guid, texts.txt_not_join, message_id)
		
		bot.send_message(guid, "پیام شما به " + user.get('first_name') + " ارسال شد ✅", message_id)
		
		bot.send_message(user["user_guid"],  "سلام " + user.get('first_name') + " پیام ناشناس داری😃!\n\n" + " ".join(message.split()[1:]))
	except:
		bot.send_message(guid, texts.txt_error, message_id)
		
def send_with_username(guid, message, message_id):
	try:
		if len(message.split()) == 1 :
			return bot.send_message(guid, texts.txt_not_text, message_id)
		
		if hasSwear(" ".join(message.split()[1:]))[0] :
			return alert(guid)

		user_info = bot.get_username_info(message.split()[0][1:])["data"]
		
		if user_info["exist"] != True :
			return bot.send_message(guid, texts.txt_not_exist, message_id)
			
		if user_info["type"] != "User":
			return bot.send_message(guid, texts.txt_is_channel, message_id)
			
		if not "SendMessages" in user_info["chat"]["access"] :
			return bot.send_message(guid, texts.txt_bot_is_block, message_id)
			
		user = user_info["user"]
		
		if not user["user_guid"] in open('guids.txt', 'r').read().split('\n'):
			return bot.send_message(guid, texts.txt_not_join, message_id)
			
		bot.send_message(guid, "پیام شما به " + user.get('first_name') + " ارسال شد ✅", message_id)
		
		bot.send_message(user["user_guid"],  "سلام " + user.get('first_name') + " پیام ناشناس داری😃!\n\n" + " ".join(message.split()[1:]))
	except:
		bot.send_message(guid, texts.txt_error, message_id)
			
		
while True:
	try:
		for msg in bot.chats_update():
			
			if msg["abs_object"]["type"] == "User":
				
				if msg["last_message"]["text"] and not msg["last_message"]["message_id"] in answered:
					
					
					if msg["last_message"]["text"] in ["start","/start","!start"]:
						
						member_count = len(open('guids.txt', 'r').read().split("\n"))
						guid = msg["last_message"]["author_object_guid"]
						name = bot.get_user_info(guid)["data"]["user"]["first_name"]
							
						if not guid in open('guids.txt', 'r').read().split('\n'):
							info_msg = bot.send_message(guid, "سلام " + name + texts.txt_welcome + str(member_count) + texts.txt_welcome2)
							msg_id[guid] = info_msg['data']['message_update']['message_id']
								
							with open('guids.txt', 'a') as f:
								f.write('\n' + guid)
						else:
							info_msg = bot.send_message(guid, "سلام " + name + texts.txt_welcome + str(member_count) + texts.txt_welcome2)
							msg_id[guid] = info_msg['data']['message_update']['message_id']
								
							
					elif msg["last_message"]["text"] in ["help","/help","!help","back","/back","!back"]:
						guid = msg["last_message"]["author_object_guid"]
							
						if msg_id.get(guid) != None:
							bot.edit_message(msg_id[guid], guid, texts.txt_help)
						else:
							bot.send_message(guid, texts.txt_help)


					elif msg["last_message"]["text"] in ["group","/group","!group"]:
						guid = msg["last_message"]["author_object_guid"]
							
						if msg_id.get(guid) != None:
							bot.edit_message(msg_id[guid], guid, texts.txt_use_group + "\n\n\n" + "‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍🔴 - برگشت صفحه قبلی :\n /back")
						else:
							bot.send_message(guid, texts.txt_use_group)
							
					
					elif msg["last_message"]["text"] in ["NotId","/NotId","!NotId"]:
						guid = msg["last_message"]["author_object_guid"]
							
						if msg_id.get(guid) != None:
							bot.edit_message(msg_id[guid], guid, texts.txt_send_with_guid + "\n\n\n" + "‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍🔴 - برگشت صفحه قبلی :\n /back")
						else:
							bot.send_message(guid, texts.txt_send_with_guid)

							
					elif msg["last_message"]["text"].startswith("https://rubika.ir/joing/"):
						msg = msg["last_message"]
						send_to_group(msg["author_object_guid"], msg["text"], msg["message_id"])
							
					elif msg["last_message"]["text"].startswith("u0"):
						msg = msg["last_message"]
						send_with_guid(msg["author_object_guid"], msg["text"], msg["message_id"])
						
					elif msg["last_message"]["text"].startswith("@"):
						msg = msg["last_message"]
						send_with_username(msg["author_object_guid"], msg["text"], msg["message_id"])
						
					answered.append(msg["last_message"]["message_id"])
					
	except: pass