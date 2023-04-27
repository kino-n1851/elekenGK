import discord
import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from typing import NoReturn

load_dotenv()
app_url = os.environ["APP_URL"]

intents = discord.Intents.all()
TOKEN = "tekitotoken"
client = discord.Client(intents=intents)
task = None

# 起動時に動作する処理
@client.event
async def on_ready():
    print('ログインしました')
    guild = client.guilds[0]
    async def django_message_receiver():
        current_error = None
        current_id = ""
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{app_url}/message") as response:
                        response_dict = await response.json(encoding=None)
                        version_id = str(response_dict.get("version_id"))
                        message_id = int(response_dict.get("message_id"))
                        channel_id = int(response_dict.get("channel_id"))#813247808521502765
                        channel = next(c for c in guild.channels if c.id == int(channel_id))
                        #print(f"{version_id=}") 
                        if(version_id != current_id):
                            #print("id dont match")
                            try:
                                message = channel.get_partial_message(message_id)
                                await message.edit(content=response_dict.get("content"))
                            except Exception as e:
                                print(f"[discord bot/message_edit] {e=}")
                        current_id = version_id
                        await asyncio.sleep(5)
                        current_error = None
            except Exception as e:
                if type(current_error) != type(e):
                    print(f"[discord bot/clientSession] {e=}")
                current_error = e
                await asyncio.sleep(30)
            
    global task           
    task = asyncio.get_event_loop().create_task(django_message_receiver())

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == '/neko':
        await message.channel.send('にゃーん')
    
    if message.content == '/help':
        content = "コマンド一覧:\n"+ \
        "  /help\n"+ \
        "  /create\n"+ \
        "  /register\n"+ \
        "  /register_core\n"+ \
        "  /fetch_name\n"+ \
        "--------------\n"+ \
        "[/help]\n\n"+ \
        "ヘルプを表示します。\n"+ \
        "--------------\n"+ \
        "[/create]\n\n"+ \
        "ボットメッセージの表示を作成します。\n"+ \
        "すでに表示先がある場合は以前のメッセージは無効となり、以降新しいメッセージ上で状態が更新されます。\n"+ \
        "入室状態表示が流れてしまった場合などにご利用ください。\n"+ \
        "--------------\n"+ \
        "[/register]\n\n"+ \
        "discordアカウントのidのみを使用して入室管理アプリに登録します。\n"+ \
        "メールアドレスなどは使用しておりません。\n"+ \
        "コマンド受付後は仮登録となりますので、3分以内にNFCリーダーに登録したいデバイスをタッチしてNFC IDとの紐づけをしてください。\n"+ \
        "この操作で支払いなどが発生することもありません。\n"+ \
        "--------------\n"+ \
        "[/register_core]\n\n"+ \
        "上記 registerコマンドと同様に登録を行います。\n"+ \
        "こちらのコマンドで登録したユーザは、非アクティブ時も状態が表示されます。\n"+ \
        "--------------\n"+ \
        "[/fetch_name]\n\n"+ \
        "discordサーバープロフィールなどの変更後にこのコマンドを使用することで表示名が更新されます。\n"
        await message.channel.send(content)
    
    if message.content == '/create':
        send_message = await message.channel.send("created")
        channel_id = message.channel.id
        message_id = send_message.id
        print(f"{message_id=}")
        print(f"{channel_id=}")
        
        async with aiohttp.ClientSession() as session:
            json_content = {
                'channel_id':channel_id,
                'message_id':message_id,
            }
            async with session.post(f"{app_url}/message", data=json_content)as response:
                if response.status != 200:
                    await send_message.edit(content="[discord bot] push messageID error")
    
    if message.content == '/register':
        await post_register_request(message, "")
    
    if message.content == '/register_core':
        await post_register_request(message, "true")
        
    if message.content == '/fetch_name':
        send_message = await message.channel.send("request was sent")
        async with aiohttp.ClientSession() as session:
            json_content = {
                'name':message.author.display_name,
                'discord_id':message.author.id,
            }
            async with session.post(f"{app_url}/fetch_name", data=json_content)as response:
                if response.status != 200:
                    await send_message.edit(content="[discord bot] server connection error")
                else:
                    response_dict = await response.json(encoding=None)
                    content = response_dict.get("content")
                    await send_message.edit(content=content)
        
async def post_register_request(message, is_core:str):
    async with aiohttp.ClientSession() as session:
        send_message = await message.channel.send("request was sent.")
        json_content = {
            'name':message.author.display_name,
            'discord_id':message.author.id,
            'is_core':is_core,
        }
        async with session.post(f"{app_url}/register_user", data=json_content)as response:
            if response.status != 200:
                await send_message.edit(content="[discord bot] server connection error")
            else:
                response_dict = await response.json(encoding=None)
                content = response_dict.get("content")
                await send_message.edit(content=content)


        
def run()->NoReturn:
    client.run(TOKEN)

if __name__ == "__main__":
    run()
