import re

def parse_srt_time_to_seconds(time_str): # 将SRT格式的时间戳转换为秒数
    parts = time_str.replace(',', '.').split(':') # 移除逗号并分割成[小时, 分钟, 秒]
    hours, minutes, seconds = map(float, parts)
    return int(hours * 3600 + minutes * 60 + seconds)

def seconds_to_mmss(seconds): # 将给定的秒数转换为 MM:SS 格式
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

temp = input("标题【系列No】> ")
if temp[-8] == '【' and temp[-1] == '】':
    title = temp[:-8]
    series = temp[-7:-3]
    No = temp[-3:-1]
else:
    input('输入格式错误，按 ENTER 结束')
    exit(0)

temp = input('视频链接> ')
if temp[:33] == 'https://www.bilibili.com/video/BV':
    if len(temp) == 43:
        BV = temp[31:43]
    elif temp[43] in ['/', '?']:
        BV = temp[31:43]
    else:
        input('输入格式错误，按 ENTER 结束')
        exit(0)
else:
    input('输入格式错误，按 ENTER 结束')
    exit(0)

upload_time = input('发布时间> ')
role = input('本期主角> ')
print('视频简介> ')
intro = ''
try:
    while True:
        temp = input()
        intro += (temp + '\n\n')
except KeyboardInterrupt:
    pass

file_in = 'video.srt'
file_out = f'{series}/【{series}{No}】{title}.md'

with open(file_in, 'r', encoding='utf-8') as infile, \
     open(file_out, 'w', encoding='utf-8') as outfile:
    # 写入元信息
    try:
        outfile.write(f'# 【{series}{No}】{title}\n\n')
        outfile.write(f'## 视频信息\n\n')
        outfile.write(f'本期主角：{role}\n\n')
        outfile.write(f'[视频链接](https://www.bilibili.com/video/{BV})\n\n')
        outfile.write(f'BV号：`{BV}`\n\n')
        outfile.write(f'发布时间：`{upload_time}`\n\n')
        outfile.write(f'视频简介：{intro}') ## intro末尾自带两个\n
        outfile.write(f'## 文字稿\n\n')
    except Exception as e:
        print(f"错误: {e}")
        input('已暂停')
    # 写入字幕
    lines = infile.readlines()
    index = 1
    for i in range(0, len(lines), 4):  # 每个字幕项占用4行
        try:
            subtitle_text = lines[i+2].strip()
            if subtitle_text[0] == '#':
                outfile.write(f'{subtitle_text}\n\n')
            else:
                time_line = lines[i+1].strip()
                start_time, _ = time_line.split(' --> ')
                seconds = parse_srt_time_to_seconds(start_time)
                mmss = seconds_to_mmss(seconds)
                outfile.write(f'[[{mmss}](https://www.bilibili.com/{BV}?t={seconds})] {subtitle_text}\n\n')
            index += 1
        except Exception as e:
            print(f"处理行{i}时出错: {e}")
            continue