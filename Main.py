import os
import time
import requests
from jsonpath import jsonpath

# Headers for the requests
headers = {
    "Cookie": "pgv_pvid=3587868640; fqm_pvqid=543a7b70-4f6c-4dac-b8cb-a0800c7ae7d8; ts_uid=2372400601; RK=ueWVFTG5GD; ptcz=badd61c16cda8571c854e46dab986b89e9f7a0c845bf793b23906ce4e038da71; music_ignore_pskey=202306271436Hn@vBj; ts_refer=ADTAGmyqq; fqm_sessionid=f393835a-68b7-4e80-8804-db6dce80b299; pgv_info=ssid=s7393084624; _qpsvr_localtk=0.740856308384439; ts_last=y.qq.com/n/ryqq/songDetail/002ZmSyB2zTqE6; login_type=1; tmeLoginType=2; euin=7K-PowSP7i-l; wxunionid=; psrf_qqaccess_token=E865B56DB7FE93003EE6B9D4058B4A48; wxopenid=; wxrefresh_token=; psrf_qqrefresh_token=0A0F02B6A02BF289DDDEFDCD63772D50; psrf_access_token_expiresAt=1709799305; psrf_qqopenid=E5AD0D55A82B5AFC01D1A9B3509FA40B; psrf_musickey_createtime=1702023305; qqmusic_key=Q_H_L_5_C_E6pZJYcNvXFFbG0VCEqG6OeVRNdHeL86daLbgK5o4Uh3FM07B9g; psrf_qqunionid=AAED47B4E3F2D2D6ECD3377FA5B5C142; qm_keyst=Q_H_L_5_C_E6pZJYcNvXFFbG0VCEqG6OeVRNdHeL86daLbgK5o4Uh3FM07B9g; uin=524274727",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

# Input query
query_text = input('请输入需要查询的歌手或歌名：')

# Search URL
search_url = f'https://u.y.qq.com/cgi-bin/musicu.fcg?data={{"comm":{{"g_tk":235530277,"uin":"1152921504916411742","format":"json","inCharset":"utf-8","outCharset":"utf-8","notice":0,"platform":"h5","needNewCode":1,"ct":23,"cv":0}},"req_0":{{"method":"DoSearchForQQMusicDesktop","module":"music.search.SearchCgiService","param":{{"remoteplace":"txt.mqq.all","searchid":"64237725668973550","search_type":0,"query":"{query_text}","page_num":1,"num_per_page":20}}}}}}'

response = requests.get(search_url)
# Extract the music list
music_list = jsonpath(response.json(), '$..data.body.song.list')[0]

# Print the list of music
for i, song in enumerate(music_list, 1):
    music_name = song['name']
    singer_name = ', '.join([singer['name'] for singer in song['singer']])
    print(f"{i}. {music_name} - {singer_name}")

# User input for further action
while True:
    user_input = input('请输入序号查看详情或输入 "下载[序号]" 来下载歌曲：')
    
    if user_input.isdigit():
        index = int(user_input) - 1
        if 0 <= index < len(music_list):
            song = music_list[index]
            music_name = song['name']
            singer_name = ', '.join([singer['name'] for singer in song['singer']])
            music_mid = song['mid']
            album_mid = song['album']['mid']
            album_pic_url = f"https://y.qq.com/music/photo_new/T002R300x300M000{album_mid}.jpg"
            
            # Get download link
            music_data_url = f'https://u.y.qq.com/cgi-bin/musicu.fcg?data={{"comm":{{"cv":4747474,"ct":24,"format":"json","inCharset":"utf-8","outCharset":"utf-8","notice":0,"platform":"yqq.json","needNewCode":1,"uin":"1152921504916411742","g_tk_new_20200303":1849600344,"g_tk":1849600344}},"req_4":{{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{{"guid":"4868259520","songmid":["{music_mid}"],"songtype":[0],"uin":"1152921504916411742","loginflag":1,"platform":"20"}}}}}}'

            music_data_response = requests.get(music_data_url)
            purl = jsonpath(music_data_response.json(), '$.req_4.data.midurlinfo..purl')[index]
            music_url = f'https://dl.stream.qqmusic.qq.com/{purl}'
            
            print(f"歌名: {music_name}\n歌手: {singer_name}\n音乐图片链接: {album_pic_url}\n下载链接: {music_url}")
        else:
            print("无效的序号，请重新输入。")
    elif user_input.startswith("下载"):
        try:
            index = int(user_input[2:]) - 1
            if 0 <= index < len(music_list):
                song = music_list[index]
                music_name = song['name']
                music_mid = song['mid']
                
                # Get download link
                music_data_url = f'https://u.y.qq.com/cgi-bin/musicu.fcg?data={{"comm":{{"cv":4747474,"ct":24,"format":"json","inCharset":"utf-8","outCharset":"utf-8","notice":0,"platform":"yqq.json","needNewCode":1,"uin":"1152921504916411742","g_tk_new_20200303":1849600344,"g_tk":1849600344}},"req_4":{{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{{"guid":"4868259520","songmid":["{music_mid}"],"songtype":[0],"uin":"1152921504916411742","loginflag":1,"platform":"20"}}}}}}'

                music_data_response = requests.get(music_data_url)
                purl = jsonpath(music_data_response.json(), '$.req_4.data.midurlinfo..purl')[index]
                music_url = f'https://dl.stream.qqmusic.qq.com/{purl}'
                
                # Download the song
                music_response = requests.get(music_url, headers=headers)
                
                # Create directory if not exists
                if not os.path.exists('QQ音乐'):
                    os.mkdir('QQ音乐')
                    
                # Save the song with formatted file name
                formatted_name = f"{music_name} - {singer_name}.mp3"
                with open(f'./QQ音乐/{formatted_name}', 'wb') as file:
                    file.write(music_response.content)
                    
                print(f'《{formatted_name}》下载成功')
                time.sleep(1)
            else:
                print("无效的序号，请重新输入。")
        except ValueError:
            print("无效的命令格式，请输入 '下载[序号]' 来下载歌曲。")
    else:
        print("无效的命令，请重新输入。")