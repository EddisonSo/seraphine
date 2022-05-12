from discord.ext import commands
import config
from random import randint
from textblob import TextBlob

# from time import sleep

bot = commands.Bot("$")

phrases = {
    "greet": [],
    "positive": [],
    "negative": []
}

greet = []
positive = []
negative = []


def init_phrases():
    global greet
    global negative
    global positive
    global phrases

    file = open("greet.txt")
    greet = file.read().splitlines()
    file.close()

    file = open("negative.txt")
    negative = file.read().splitlines()
    file.close()

    file = open("positive.txt")
    positive = file.read().splitlines()
    file.close()


async def print_greet(ctx):
    global greet
    await ctx.channel.send(greet[randint(0, len(greet) - 1)])


async def print_negative_message(message):
    global negative
    await message.channel.send(negative[randint(0, len(negative) - 1)])


async def print_positive_message(message):
    global positive
    await message.channel.send(positive[randint(0, len(positive) - 1)])


async def print_error(message):
    await message.channel.send("uwu I don't seem to understand that >.<")


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    init_phrases()


@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.id != 974351951812788274:
        return
    if "seraphine" in message.content.lower() and TextBlob(message.content).sentiment.polarity >= 0 and not message.content.startswith("$"):
        await print_positive_message(message)
    elif "seraphine" in message.content.lower() and not message.content.startswith("$"):
        await print_negative_message(message)

    await bot.process_commands(message)

#Bot command error handling
@bot.event
async def on_command_error(ctx, error):
    await ctx.channel.send("uwu I don't seem to understand that >.<")

#Bot commands
@bot.command()
async def hello(ctx):
    await print_greet(ctx)


if __name__ == "__main__":
    bot.run(config.token)
