الاستيراد.os.
import telebot
from yt_dlp import YoutubeDL
import time

# توكن البوت الخاص بك
TOKEN = "8773671583:AAGFyn1zT93mGdbQVFiBepxvqixsMETI-5E"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ البوت يعمل بنجاح على سيرفر Render! أرسل رابط الفيديو.")

@bot.message_handler(func=lambda m: "http" in m.text)
def download(message):
    cid = message.chat.id
    url = message.text
    msg = bot.reply_to(message, "⏳ جاري التحميل... يرجى الانتظار")
    
    try:
        opts = {
            'format': 'best',
            'outtmpl': f'v_{cid}.%(ext)s',
            'quiet': True,
        }
        
        with YoutubeDL(opts) as ydl:
            ydl.download([url])
            info = ydl.extract_info(url, download=False)
            path = ydl.prepare_filename(info)
        
        if os.path.exists(path):
            with open(path, 'rb') as v:
                bot.send_video(cid, v)
            os.remove(path)
            bot.delete_message(cid, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ فشل التحميل: {str(e)[:50]}", cid, msg.message_id)

print("🚀 Bot is starting...")
bot.infinity_polling()

