from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp
import os
import time

TOKEN = "8672164369:AAEsqy5qvD8BqG1KdeFmkf5hkqvHUoVgX6s"

async def tiktok_dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    filename = f"tiktok_{int(time.time())}"

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{filename}.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            ext = info['ext']

        video_file = f"{filename}.{ext}"

        await update.message.reply_video(
            video=open(video_file, 'rb'),
            supports_streaming=True
        )

        os.remove(video_file)

    except Exception as e:
        await update.message.reply_text(f"Tunggu bentarr prend: {e}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, tiktok_dl)
)

print("Bot running...")
app.run_polling()
