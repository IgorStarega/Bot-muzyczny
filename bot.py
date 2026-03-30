import os
import asyncio
import logging
import discord
import yt_dlp
from discord.ext import commands

PREFIX = os.getenv("PREFIX", "!")
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
logger = logging.getLogger(__name__)

YTDL_FORMAT_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "default_search": "auto",
}
FFMPEG_OPTIONS = {
    "options": "-vn",
}


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title", "unknown")

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_running_loop()
        ytdl = yt_dlp.YoutubeDL(YTDL_FORMAT_OPTIONS)
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if "entries" in data:
            data = data["entries"][0]
        source_url = data["url"]
        audio = discord.FFmpegPCMAudio(source_url, **FFMPEG_OPTIONS)
        return cls(audio, data=data)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command(name="join")
async def join(ctx):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("Musisz być na kanale głosowym.")
        return

    channel = ctx.author.voice.channel
    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    await ctx.send(f"Dołączono do: {channel.name}")


@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Rozłączono.")
    else:
        await ctx.send("Bot nie jest połączony.")


@bot.command(name="play")
async def play(ctx, *, url: str):
    if not ctx.voice_client:
        await join(ctx)
        if not ctx.voice_client:
            return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    try:
        player = await YTDLSource.from_url(url)
        ctx.voice_client.play(player)
        await ctx.send(f"Teraz gra: {player.title}")
    except Exception:
        logger.exception("Błąd podczas odtwarzania utworu")
        await ctx.send("Nie udało się odtworzyć utworu. Spróbuj ponownie za chwilę.")


@bot.command(name="pause")
async def pause(ctx):
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await ctx.send("Pauza.")
    else:
        await ctx.send("Nic nie jest odtwarzane.")


@bot.command(name="resume")
async def resume(ctx):
    vc = ctx.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await ctx.send("Wznowiono.")
    else:
        await ctx.send("Nic nie jest zapauzowane.")


@bot.command(name="stop")
async def stop(ctx):
    vc = ctx.voice_client
    if vc and (vc.is_playing() or vc.is_paused()):
        vc.stop()
        await ctx.send("Zatrzymano.")
    else:
        await ctx.send("Nic nie jest odtwarzane.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not TOKEN:
        raise RuntimeError("Brak DISCORD_TOKEN w zmiennych środowiskowych")
    bot.run(TOKEN)
