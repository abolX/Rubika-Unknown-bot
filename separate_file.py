def hasSwear(Msg):
	swData = [False,None]
	Msg = ''.join(filter(str.isalpha, Msg)).replace("-", "")
	for i in open("swear_file.txt").read().split("\n"):
		if i in Msg:
			swData = [True, i]
			break
		else: continue
	return swData
	
answered, msg_id = [], {}