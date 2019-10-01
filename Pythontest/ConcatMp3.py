# -*- coding: utf-8 -*-
import io

import pydub
from pydub import AudioSegment  # 先导入这个模块
from pydub.audio_segment import AudioSegment
# 加载需要合并的两个mp3音频
pydub.AudioSegment.ffmpeg = "C:\\Temp\\FormatFactory\\ffmpeg.exe"
pydub.AudioSegment.converter ='C:\\Temp\\FormatFactory\\ffmpeg.exe'

with open("D:\\Works\\Pythontest\\c.mp3", 'rb') as fh:
    data = fh.read()

aud = io.BytesIO(data)

input_music_1 = AudioSegment.from_file("D://Works//Pythontest//c.mp3",format='MP3')
input_music_2 = AudioSegment.from_mp3("D:/Works/Pythontest/c.mp3")
#获取两个音频的响度（音量）
input_music_1_db = input_music_1.dBFS
input_music_2_db = input_music_2.dBFS
# 获取两个音频的时长，单位为毫秒
input_music_1_time = len(input_music_1)
input_music_2_time = len(input_music_2)
# 调整两个音频的响度一致
db = input_music_1_db- input_music_2_db
if db > 0:
    input_music_1 += abs(dbplus)
elif db < 0:
    input_music_2 += abs(dbplus)
# 合并音频
output_music = input_music_1 + input_music_2
# 简单输入合并之后的音频
output_music.export("d:/output_music.mp3", format="mp3")# 前面是保存路径，后面是保存格式
#复杂输入合并之后的音频
# bitrate：比特率，album：专辑名称，artist：歌手，cover：封面图片
output_music.export("d:/temp/output_music.mp3", format="mp3", bitrate="192k", tags={"album": "专辑", "artist": "歌手"}, cover="d:/封面.jpg")
print(len(output_music), output_music.channels)# 合并音频的时长，音频的声道，1是单声道，2是立体声
