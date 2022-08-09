text_cr =" Telegram me : @A_ABOL\n Github : https://github.com/abolX\n Rubika : @electro_bot\n"

from re import findall
from random import randint, choice
from json import loads, dumps, JSONDecodeError
from base64 import b64encode
from requests import post, get
from datetime import datetime
from io import BytesIO
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, urlsafe_b64decode

class encryption:
    def __init__(self, auth):
        self.key = bytearray(self.secret(auth), "UTF-8")
        self.iv = bytearray.fromhex('00000000000000000000000000000000')

    def replaceCharAt(self, e, t, i):
        return e[0:t] + i + e[t + len(i):]

    def secret(self, e):
        t = e[0:8]
        i = e[8:16]
        n = e[16:24] + t + e[24:32] + i
        s = 0
        while s < len(n):
            e = n[s]
            if e >= '0' and e <= '9':
                t = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
                n = self.replaceCharAt(n, s, t)
            else:
                t = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
                n = self.replaceCharAt(n, s, t)
            s += 1
        return n

    def encrypt(self, text):
        raw = pad(text.encode('UTF-8'), AES.block_size)
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        enc = aes.encrypt(raw)
        result = b64encode(enc).decode('UTF-8')
        return result

    def decrypt(self, text):
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        dec = aes.decrypt(urlsafe_b64decode(text.encode('UTF-8')))
        result = unpad(dec, AES.block_size).decode('UTF-8')
        return result

class Bot:
	def __init__(self, auth):
		self.auth = auth
		self.enc = encryption(auth); print(text_cr)
		
		if self.auth[:2] in 'g0': 
			print("خطا ! guid و bot اشتباه جایگذاری شده است !")
		elif len(self.auth) < 32:
			print("لطفا auth را درست وارد کنید !")
		
	def send_message(self, chat_id, text, message_id=None):
		if message_id == None:
			t = False
			while t == False:
				try:
					p = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/")
					p = loads(self.enc.decrypt(p.json()["data_enc"]))
					t = True
				except:
					t = False
			return p
		else:
			t = False
			while t == False:
				try:
					p = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/")
					p = loads(self.enc.decrypt(p.json()["data_enc"]))
					t = True
				except:
					t = False
			return p
		
	def edit_message(self, message_id, guid, newText):
		edit = False
		while edit == False:
			try:
				edited = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"editMessage",
					"input":{
						"message_id":message_id,
						"object_guid":guid,
						"text":newText 
					},
					"client":{
						"app_name":"Main",
						"app_version":"4.0.4",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
				}))},url="https://messengerg2c68.iranlms.ir/")
				return edited
				edit = True
			except: edit = False
		return edited

		
	def delete_messages(self, chat_id, message_ids):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"deleteMessages",
			"input":{
				"object_guid":chat_id,
				"message_ids":message_ids,
				"type":"Global"
			},
			"client":{
				"app_name":"Main",
				"app_version":"4.0.4",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c17.iranlms.ir/").json()["data_enc"]))
		
	def chats_update(self):
		time_stamp = str(round(datetime.today().timestamp()) - 200)
		p = post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getChatsUpdates",
			"input":{
				"state":time_stamp,
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c67.iranlms.ir/")
		p = loads(self.enc.decrypt(p.json().get("data_enc"))).get("data").get("chats")
		return p

	def get_user_info(self, chat_id):
		user_info = False
		while user_info == False:
			try:
				p = loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"getUserInfo",
					"input":{
						"user_guid":chat_id
					},
					"client":{
						"app_name":"Main",
						"app_version":"3.2.1",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
				}))},url="https://messengerg2c37.iranlms.ir/").json()["data_enc"]))
				user_info = True
			except: continue
		return p
		
	def get_username_info(self, username):
		t = False
		while t == False:
			try:
				s = loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"getObjectByUsername",
					"input":{
						"username":username
					},
					"client":{
						"app_name":"Main",
						"app_version":"3.2.1",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
				}))},url="https://messengerg2c23.iranlms.ir/").json().get("data_enc")))
				return s
				t = True
			except: t = False
		return s
		
	def get_message_info(self, chat_id, message_ids):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesByID",
			"input":{
				"object_guid": chat_id,
				"message_ids": message_ids
			},
			"client":{
				"app_name": "Main",
				"app_version" : "4.0.4",
				"platform": "Web",
				"package": "web.rubika.ir",
				"lang_code": "fa"
				}
					
			}))}, url="https://messengerg2c64.iranlms.ir/").json()["data_enc"])).get("data").get("messages")
			
	def join_group(self, link):
		join = False
		while join == False:
			try:
				joined = loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"joinGroup",
					"input":{
						"hash_link": link.split('/')[-1]},
					"client":{
						"app_name": "Main",
						"app_version" : "4.0.4",
						"platform": "Web",
						"package": "web.rubika.ir",
						"lang_code": "fa"
					}
				}))},url="https://messengerg2c17.iranlms.ir/").json()["data_enc"]))
				return joined
				join = True
			except: join = False
		return joined
				
	def leave_group(self, group_guid):
		leave = False
		while leave == False:
			try:
				leaved = loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"leaveGroup",
					"input":{
						"group_guid": group_guid},
					"client":{
						"app_name": "Main",
						"app_version" : "4.0.4",
						"platform": "Web",
						"package": "web.rubika.ir",
						"lang_code": "fa"
					}
					}))},url="https://messengerg2c17.iranlms.ir/").json()["data_enc"]))
				return leaved
				leave = True
			except: leave = False
		return leaved

	def block(self, chat_id):
		block = False
		while block == False:
			try:
				blocked = loads(self.enc.decrypt(post(json={"api_version": "5", "auth": self.auth, "data_enc": self.enc.encrypt(dumps({
					"method": "setBlockUser",
					"input":{
						"action": "Block",
						"user_guid": chat_id
					},
					"client":{
						"app_name": "Main",
						"app_version" : "4.0.4",
						"platform": "Web",
						"package": "web.rubika.ir",
						"lang_code": "fa"
					}
					}))},url="https://messengerg2c17.iranlms.ir/").json()["data_enc"]))
				return blocked
				block = True
			except: block = False
		return blocked
		
	def check_join_group(self, chat_id, text):
		return loads(self.enc.decrypt(post(json={"api_version":"5", "auth": self.auth, "data_enc": self.enc.encrypt(dumps({
			"method": "getGroupAllMembers",
			"input":{
				"group_guid": chat_id,
				"search_text": text
			},
			"client":{
				"app_name":"Main",
				"app_version":"4.0.8",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
			}))},url="https://messengerg2c23.iranlms.ir/").json()["data_enc"]))
			
	def search(self, chat_id, text):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method": "searchChatMessages",
			"input":{
				"object_guid": chat_id,
				"search_text": text,
				"type": "Text"
			},
			"client":{
				"app_name":"Main",
				"app_version":"4.0.8",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
			}))},url="https://messengerg2c17.iranlms.ir/").json()["data_enc"]))
			
	def send_poll(self, chat_id, question, options):
		p = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"createPoll",
			"input":{
				"allows_multiple_answers": False,
				"is_anonymous": True,
				"object_guid":chat_id,
				"options": options,
				"question": question,
				"rnd":f"{randint(100000,999999999)}",
				"type": "Regular"
			},
			"client":{
				"app_name":"Main",
				"app_version":"4.0.8",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
			}))},url="https://messengerg2c64.iranlms.ir/")
		return loads(self.enc.decrypt(p.json()["data_enc"]))
		
