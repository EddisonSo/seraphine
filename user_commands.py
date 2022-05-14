from discord import File
from discord.ext import commands
from random import randint
from os import listdir
import requests
import shutil


class user_commands(commands.Cog):
    # Attributes
    phrases = {}

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

    @commands.command()
    async def reload(self, ctx):
        if ctx.message.author.id != 144362248440250368:
            await ctx.channel.send("Nope :3")
            return
        self.bot.reload_extension("user_commands")
        self.bot.reload_extension("user_message")
        self.bot.reload_extension("admin_commands")
        print("Seraphine reloaded >.<")

def setup(bot):
    bot.add_cog(user_commands(bot))
