from gtts import gTTS
t = gTTS(text='Meo con de thuong qua! Cac ban thay the nao?', lang='vi')
t.save('output/music/test_voice2.mp3')
import os
print('SAVED', os.path.getsize('output/music/test_voice2.mp3'))
