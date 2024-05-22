import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
TOKEN = os.getenv('TOKEN')

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Inisialisasi bot dengan prefix tertentu
bot = commands.Bot(command_prefix='!', intents=intents)

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
# Token bot

default_message = [{'role': 'user', 'parts':  ["Halo, bisakah kamu membantu saya?"]}, {'role': 'model', 'parts': ["Halo! Nama saya StudyBot, saya siap menjawab pertanyaan anda seputar pelajaran sekolah"]}]

history = []

aktif = False
    
@bot.event
async def on_message(ctx):
    if ctx.author.bot:
        return
    global aktif
    global history
    if ctx.content.startswith("!genai"):
        aktif = not aktif
        if aktif:
            await ctx.reply("Genai sekarang aktif")
        else:
            await ctx.reply("Genai sekarang mati")
            history = []
        return
    if not aktif:
        return
    try:
        if len(history) == 0:
            history = default_message.copy()
        if len(history) == 10:
            history.pop(2)
            history.pop(2)
        history.append({'role': 'user', 'parts':  [f"{ctx.author.name}: {ctx.content}"]})
        response = model.generate_content (history)
        history.append({'role': 'model', 'parts': [response.text]})
        await ctx.reply(response.text)
    except genai.Error as e:
        await ctx.reply(f"An error occurred: {e}")


# Jalankan bot dengan token yang sudah disediakan
bot.run(TOKEN)
