# インストールした discord.py を読み込む
import discord
from bs4 import BeautifulSoup
import requests

url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=110010'


# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'Njc5NjQ5ODQ1NjczMTk3NjEx.Xk0byQ.P2voHxvvLo_GnW3mRUiQEpMoIFE'

# 接続に必要なオブジェクトを生成
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
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

    if message.content == '/tenki':
        data = requests.get(url).json()
        for weather in data['forecasts']:
            await message.channel.send(weather['dateLabel'] + 'の天気：' + weather['telop'])

    if message.content == '/kion':
        data = requests.get(url).json()
        await message.channel.send(data['forecasts'][1]['dateLabel'] + 'の最低気温 : ' + data['forecasts'][1]['temperature']['min']['celsius'] + '℃')
        await message.channel.send(data['forecasts'][1]['dateLabel'] + 'の最高気温 : ' + data['forecasts'][1]['temperature']['max']['celsius'] + '℃')

    if message.content == '/detail':
        data = requests.get(url).json()
        await message.channel.send(data['description']['text']) 

    if message.content == '/news':
        tlist = []
        r = requests.get("https://news.yahoo.co.jp/")
	
        soup = BeautifulSoup(r.content, "html.parser")
	
        #ニュース一覧のテキストのみ抽出
        topic = soup.find("ul", "newsFeed_list").text
        tlist = topic.split('\u3000')

        for t in tlist:
            await message.channel.send(t + "\n\r")
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)