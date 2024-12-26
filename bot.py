from pyrogram import Client, filters
import os
import asyncio
from traceback import print_exc
from subprocess import PIPE, STDOUT
from time import time

api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']

app = Client('m3u8', api_id, api_hash, bot_token=bot_token)

@app.on_message(filters.command('start'))
async def start(client, message):
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=f"""<b>Hello {message.from_user.mention} 👋,

I'm M3U8 File Uploader. Just send me any m3u8 link and I'll upload file remotely to Telegram..✨

Please send your link in this format : /upload link..❤</b>""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("Updates Channel 📣", url="t.me/StarkIndustriezz"),
            ],[
            InlineKeyboardButton("Developer 👨‍💻", url="t.me/YourStarkk")
            ]]
            )
        )

@app.on_message(filters.command(['upload']))
async def convert(client, message):
    try:
        link = message.text.split(' ', 1)[1]
    except:
        print_exc()
        return await message.reply(f"""<b>Please send your link in this format : /upload link..❤</b>""")
    _info = await message.reply(f'<b>Please wait...⚡</b>')
    filename = f'{message.from_user.id}_{int(time())}'
    proc = await asyncio.create_subprocess_shell(
        f'ffmpeg -i {link} -c copy -bsf:a aac_adtstoasc {filename}.mp4',
        stdout=PIPE,
        stderr=PIPE
    )
    await _info.edit("Dosya mp4'e çevriliyor...")
    out, err = await proc.communicate()
    await _info.edit('Dosya başarıyla çevrildi.')
    print('\n\n\n', out, err, sep='\n')
    try: 
        await _info.edit('Thumbnail ekleniyor...')
        proc2 = await asyncio.create_subprocess_shell(
            f'ffmpeg -i {filename}.mp4 -ss 00:00:30.000 -vframes 5 {filename}.jpg',
            stdout=PIPE,
            stderr=PIPE
        )
        await proc2.communicate()
        await _info.edit('Video süresi çekiliyor...')
        proc3 = await asyncio.create_subprocess_shell(
            f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {filename}.mp4',
            stdout=PIPE,
            stderr=STDOUT
        )
        duration, _ = await proc3.communicate()
        await _info.edit('Telegrama yükleniyor...')

        await _info.edit("Dosya Telegram'a yükleniyor...")
        def progress(current, total):
            print(message.from_user.first_name, ' -> ', current, '/', total, sep='')
        await client.send_video(message.chat.id, f'{filename}.mp4', duration=int(duration.decode()), thumb=f'{filename}.jpg', caption = f'{filename}', progress=progress)
        os.remove(f'{filename}.mp4')
        os.remove(f'{filename}.jpg')
    except:
        print_exc()
        return await _info.edit('`Bir hata oluştu.`')


app.run()
