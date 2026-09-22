import json
p='config/scripts_vi.json'
d=json.load(open(p,encoding='utf-8'))
new={
'anime':{'hook':'Thế Giới Anime','lines':['Thế giới anime đầy màu sắc và phiêu lưu.','Mỗi nhân vật đều có một ước mơ thật đẹp.','Từ tình bạn đến lòng dũng cảm, tất cả đều truyền cảm hứng.','Hãy cùng khám phá những câu chuyện tuyệt vời nhé!']},
'roblox':{'hook':'Thế Giới Roblox','lines':['Roblox là thế giới sáng tạo không giới hạn.','Bạn có thể xây nhà, chơi game và kết bạn.','Mỗi trò chơi là một cuộc phiêu lưu mới.','Hãy cùng nhau khám phá và sáng tạo nhé!']},
'cute_animals':{'hook':'Những Bạn Thú Cute','lines':['Những chú thú nhỏ đáng yêu luôn làm ta vui.','Chúng có bộ lông mềm và đôi mắt tròn xoe.','Mỗi cử chỉ đều đáng yêu hết mực.','Hãy yêu thương các bạn nhỏ này nhé!']},
'meme':{'hook':'Meme Vui Nhộn','lines':['Meme mang lại tiếng cười cho mọi người.','Chỉ cần một bức ảnh cũng khiến ta vui cả ngày.','Tiếng cười là liều thuốc tinh thần tuyệt vời.','Hãy chia sẻ tiếng cười đến bạn bè nhé!']},
'gacha':{'hook':'Thế Giới Gacha','lines':['Gacha là nơi bạn tạo nhân vật của riêng mình.','Mỗi nhân vật có kiểu tóc và trang phục đẹp.','Bạn có thể kể những câu chuyện thú vị.','Hãy cùng nhau sáng tạo thế giới mơ ước nhé!']}}
for k,v in new.items():
    d[k]=v
json.dump(d, open(p,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('OK total', len(d))
