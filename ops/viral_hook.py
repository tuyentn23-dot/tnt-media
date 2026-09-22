# viral_hook.py - hook templates toi uu tu du lieu that (tab)
import os, sys, json

# Pattern tu TOP video thuc te (MM2, Goku, Pikachu, BloxFruits)
PATTERNS = [
	'Bi mat {X} ma 99% nguoi choi khong biet',
	'{X} manh den muc nao? Su that khong ngo',
	'Su that dong troi ve {X} ban chua tung nghe',
	'Tai sao {X} lai khien ca the gioi phat cuong',
	'Dieu gi xay ra neu {X}? Cau tra loi se shock ban',
	'3 su that ve {X} se thay doi cach ban nghi',
	'Dung xem {X} cho toi khi ban biet dieu nay',
	'{X} - bi an duoc giau suot nhieu nam',
]

def fill(topic, name):
	n = name or topic
	return [p.replace('{X}', n) for p in PATTERNS]
