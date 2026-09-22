# content_gen.py - sinh content moi tu topic templates (tab)
import os, sys, json, random
ROOT = os.getcwd()

# Template fact theo chu de (moi cau la 1 fact that)
BANK = {
	'animal': [
		{'hook': 'Loai chim nay bay cao hon Everest', 'body': 'Ngong dau than bay o do cao 8000m khi di cu', 'payoff': 'Chung ngu tren khong de tranh ke thu', 'search_query': 'goose flying sky birds'},
		{'hook': 'Ca heo ngu mot nua nao', 'body': 'Ca heo tat mot nua ban cau nao de nghi va canh chung', 'payoff': 'Chung van boi va tho trong luc ngu', 'search_query': 'dolphin swimming ocean'},
	],
	'space': [
		{'hook': 'Sao Thuy nho hon Mat Trang', 'body': 'Sao Thuy la hanh tinh nho nhat he Mat Troi', 'payoff': 'No chi lon hon Mat Trang chut it', 'search_query': 'mercury planet space'},
	],
}

def gen_from_bank():
	out = []
	for topic, facts in BANK.items():
		for f in facts:
			f = dict(f); f['topic'] = topic
			f['id'] = topic + 'gen' + str(abs(hash(f['hook'])) % 99999)
			out.append(f)
	return out
