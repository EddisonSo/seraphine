from discord import File, FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
from random import randint
from os import listdir
import requests
import shutil
from asyncio import sleep


class user_commands(commands.Cog):
    # Attributes
    phrases = {}
    songs = {
        "childhood dreams": "./sounds/Childhood Dreams.mp3",
        "champ select": "./sounds/Seraphine_Select.ogg",
        "pop/stars": "./sounds/POP_STARS.mp3",
        "all the things she said": "./sounds/All The Things She Said.mp3",
        "laugh": "./sounds/Seraphine_Original_Laugh_0.ogg",
        "kiss": "./sounds/Seraphine_Original_Q_3.ogg",
        "harmonize": "./sounds/Seraphine_Original_W_2.ogg",
        "stuck": "./sounds/Seraphine_Original_Kill_0.ogg",
        "not a fan": "./sounds/Seraphine_Original_Death_2.ogg",
        "rebirth": "./sounds/rebirth.mp3"
    }


    def __init__(self, bot):
        self.bot = bot

        file = open("texts/greet.txt")
        self.phrases["greet"] = file.read().splitlines()
        file.close()

        file = open("texts/negative.txt")
        self.phrases["negative"] = file.read().splitlines()
        file.close()

        file = open("texts/positive.txt")
        self.phrases["positive"] = file.read().splitlines()
        file.close()

    # Command helper functions
    async def print_greet(self, ctx):
        greets = self.phrases["greet"]
        await ctx.channel.send(greets[randint(0, len(greets) - 1)])

    async def send_kink(self, ctx):
        files = listdir("./dirty")
        numFile = len(files)
        await ctx.channel.send(file=File("./dirty/" + files[randint(0, numFile - 1)]))

    async def play_audio(self, ctx, voice):
        channel = ctx.message.author.voice.channel

        song_req = ctx.message.content[6:]
        if song_req not in self.songs:
            await ctx.channel.send("uwu I appear to not know that song >.<")
            return

        if ctx.voice_client.is_playing():
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.stop()

        song = self.songs[song_req]
        source = FFmpegPCMAudio(executable="C:\FFmpeg/ffmpeg.exe", source=song)

        voice.play(source)
        voice.pause()
        await sleep(1)
        voice.resume()

    def is_connected(self, voice):
        return voice and voice.is_connected()

    # Commands
    @commands.command()
    async def hello(self, ctx):
        await self.print_greet(ctx)

    @commands.command()
    async def kink(self, ctx):
        await self.send_kink(ctx)

    @commands.command()
    async def save(self, ctx):
        try:
            url = ctx.message.attachments[0].url
        except IndexError:
            print("Error no attachments")
            await ctx.send("No attatchments")
        else:
            if url[0:26] == "https://cdn.discordapp.com" and input("Confirm save file: ") == "Y":
                numFile = len(listdir("./dirty"))
                r = requests.get(url, stream=True)
                imageName = str(("dirty%s.jpg") % (str(numFile + 1)))
                with open("./dirty/" + imageName, 'wb') as out_file:
                    print("Saving Image: " + imageName)
                    shutil.copyfileobj(r.raw, out_file)
                await ctx.reply("saved")

    @commands.command()
    async def reload(self, ctx):
        if ctx.message.author.id != 144362248440250368:
            await ctx.channel.send("Nope :3")
            return
        self.bot.reload_extension("user_commands")
        self.bot.reload_extension("user_message")
        self.bot.reload_extension("admin_commands")
        print("Seraphine reloaded >.<")

    @commands.command()
    async def play(self, ctx):
        if not ctx.author.voice:
            await ctx.channel.send("uwu I can't find you!")
            return

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if not self.is_connected(voice):
            voice = await ctx.author.voice.channel.connect()
        else:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                voice.stop()
                await ctx.voice_client.move_to(ctx.author.voice.channel)
        if len(ctx.message.content) == 5:
            if self.bot.user in ctx.channel.members:
                voice.resume()
            return

        await self.play_audio(ctx, voice)

    @commands.command()
    async def pause(self, ctx):
        if self.bot.user in ctx.channel.members:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.pause()

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client.is_playing():
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.stop()

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def playlist(self, ctx):
        songs = ""
        for song in self.songs.keys():
            songs += song + "\n"
        await ctx.channel.send(songs)


def setup(bot):
    bot.add_cog(user_commands(bot))
