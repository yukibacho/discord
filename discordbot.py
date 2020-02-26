import discord
from bs4 import BeautifulSoup
import requests

url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=110010'

TOKEN = 'Njc5NjQ5ODQ1NjczMTk3NjEx.Xk1DDw.uu2nU8l-jGH0vP4G2lAj-FMpggU'

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
        r = requests.get("https://news.yahoo.co.jp/")
	
        soup = BeautifulSoup(r.content, "html.parser")
	
        #ニュース一覧のテキストのみ抽出
        topics = soup.select('.newsFeed_item_title')

        for topic in topics:
            await message.channel.send("・" +topic.next + "\n\r")
            
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
