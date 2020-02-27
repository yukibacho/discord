import discord
from bs4 import BeautifulSoup
import requests

url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=110010'

TOKEN = 'Njc5NjQ5ODQ1NjczMTk3NjEx.XleM2A.WNx_8094PDDAZ0rsZ-_f4-crBrI'

client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.content == 'てんき':
        data = requests.get(url).json()
        for weather in data['forecasts']:
            await message.channel.send(weather['dateLabel'] + 'の天気：' + weather['telop'])

    if message.content == 'きおん':
        data = requests.get(url).json()
        await message.channel.send(data['forecasts'][1]['dateLabel'] + 'の予想最低気温 : ' + data['forecasts'][1]['temperature']['min']['celsius'] + '℃')
        await message.channel.send("------------------------")
        await message.channel.send(data['forecasts'][1]['dateLabel'] + 'の予想最高気温 : ' + data['forecasts'][1]['temperature']['max']['celsius'] + '℃')

    if message.content == 'くわしく':
        data = requests.get(url).json()
        await message.channel.send(data['description']['text']) 

    if message.content == 'にゅーす':
        r = requests.get("https://news.yahoo.co.jp/")
	
        soup = BeautifulSoup(r.content, "html.parser")
	
        #ニュース一覧のテキストのみ抽出
        topics = soup.select('.topicsListItem')
        for topic in topics:
            await message.channel.send("・" + topic.next.next)
            await message.channel.send(str(topic.next.attrs.get("href")))
            
# Botの起動とDiscordサーバーへの接続
try:
    client.run(TOKEN)

except discord.errors.HTTPException:
    print("HTTP error")
except discord.errors.LoginFailure as e :
    print("Login unsuccessful")