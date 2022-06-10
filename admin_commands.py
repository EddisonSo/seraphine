from discord.ext import commands
from discord import FFmpegPCMAudio
import config
from os import listdir
import requests
import shutil
from asyncio import sleep
import pyttsx3

class admin_commands(commands.Cog):
    # Attributes
    channels = config.channels
    songs = config.songs

    curr_channel = "personal"
    curr_channel_id = channels[curr_channel]

    voice = None

    def __init__(self, bot):
        self.bot = bot

    # Command helper functions
    def check_command(self, message):
        return str(message.channel.type) == "private" and message.author.id == 144362248440250368

    async def get_channel(self, message):
        await message.channel.send("Current channel: " + self.curr_channel)
        print("Current channel: " + self.curr_channel)
        return self.curr_channel

    async def get_channel_id(self, message):
        await message.channel.send("Current channel ID: " + str(self.curr_channel_id))
        print("Current channel ID: " + str(self.curr_channel_id))
        return self.curr_channel_id

    async def switch_channel(self, message):
        if len(message.content.split()) != 2:
            await message.channel.send("Error: Invalid number of parameters. Usage: 'channel <channel-name>'")
            return
        channel = message.content.split()[1]
        if channel not in self.channels:
            await message.channel.send("Error: Channel not recognized")
            return
        self.curr_channel_id = self.channels[channel]
        self.curr_channel = channel
        await self.get_channel(message)
        await self.get_channel_id(message)

    async def send(self, message):
        if len(message.content) <= 5:
            await message.channel.send("Error: Invalid number of parameters. Usage: 'send <message>'")
            return
        channel = self.bot.get_channel(self.curr_channel_id)
        await channel.send(message.content[4:])

    async def join(self, message):
        if len(message.content.split(" ")) != 2:
            await message.channel.send("Error: Invalid number of parameters. Usage: 'join <voice channel id>'")
            return
        voice_channel_id = int(message.content.split(" ")[1])
        voice_channel = self.bot.get_channel(voice_channel_id)
        await voice_channel.connect()

    async def save(self, message):
        try:
            url = message.attachments[0].url
        except IndexError:
            print("Error no attachments")
            await message.send("No attatchments")
        else:
            if url[0:26] == "https://cdn.discordapp.com":
                numFile = len(listdir("./dirty"))
                r = requests.get(url, stream=True)
                imageName = str(("dirty%s.jpg") % (str(numFile + 1)))
                with open("./dirty/" + imageName, 'wb') as out_file:
                    print("Saving Image: " + imageName)
                    shutil.copyfileobj(r.raw, out_file)
                await message.reply("saved")

    async def join(self, message):
        channel_id = 969969726300246046
        channel = self.bot.get_channel(channel_id)
        self.voice = await channel.connect()

    def is_connected(self, voice):
        return voice and voice.is_connected()

    async def play(self, message):
        if self.voice == None:
            message.channel.send("Error: Unable to get channel!")
            return

        song_req = message.content[5:]
        song = self.songs[song_req]

        source = FFmpegPCMAudio(executable="C:\FFmpeg/ffmpeg.exe", source=song)

        self.voice.play(source)
        self.voice.pause()
        await sleep(1)
        self.voice.resume()

    async def say(self, message):
        if self.voice == None:
            message.channel.send("Error: Unable to get channel!")
            return

        message = message.content[4:]

        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[1].id)
        engine.save_to_file(message, "./sounds/temp.ogg")
        engine.runAndWait()

        source = FFmpegPCMAudio(executable="C:\FFmpeg/ffmpeg.exe", source="./sounds/temp.ogg")

        self.voice.play(source)
        self.voice.pause()
        await sleep(1)
        self.voice.resume()

    # Commands
    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.check_command(message):
            return

        if message.content.startswith("channel"):
            await self.switch_channel(message)
            return

        if message.content.startswith("currchannel"):
            await self.get_channel(message)
            return

        if message.content.startswith("send"):
            await self.send(message)
            return

        if message.content.startswith("join"):
            await self.join(message)
            return

        if message.content.startswith("save"):
            await self.save(message)
            return

        if message.content.startswith("join"):
            await self.join(message)
            return

        if message.content.startswith("play"):
            await self.play(message)
            return

        if message.content.startswith("say"):
            await self.say(message)
            return




def setup(bot):
    bot.add_cog(admin_commands(bot))
