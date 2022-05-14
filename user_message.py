from discord import File
from discord.ext import commands
from random import randint
from os import listdir
import requests
import shutil
from textblob import TextBlob

class user_message(commands.Cog):
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

    def check_invalid_message(self, message):
        return message.author == self.bot.user

    async def is_command(self, message):
        return str(message.channel.type) == "private"

    async def print_negative_message(self, message):
        negatives = self.phrases["negative"]
        await message.channel.send(negatives[randint(0, len(negatives) - 1)])

    async def print_positive_message(self, message):
        positives = self.phrases["positive"]
        await message.channel.send(positives[randint(0, len(positives) - 1)])

    async def handle_message(self, message):
        if "seraphine" in message.content.lower() and TextBlob(message.content).sentiment.polarity >= 0 and not message.content.startswith("$"):
            await self.print_positive_message(message)
        elif "seraphine" in message.content.lower() and not message.content.startswith("$"):
            await self.print_negative_message(message)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.check_invalid_message(message):
            return
        if await self.is_command(message):
            return
        await self.handle_message(message)

def setup(bot):
    bot.add_cog(user_message(bot))
