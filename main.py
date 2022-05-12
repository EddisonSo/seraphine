import discord
import config
from random import randint
from textblob import TextBlob
#from time import sleep

client = discord.Client()

greet = []
positive = []
negative = []

def get_greet():
    file = open("greet.txt")
    global greet
    greet = file.read().splitlines()
    file.close()

async def print_greet(message):
    global greet
    await message.channel.send(greet[randint(0,len(greet)-1)])

def get_negative_message():
    file = open("negative.txt")
    global negative
    negative = file.read().splitlines()
    file.close()

async def print_negative_message(message):
    global negative
    await message.channel.send(negative[randint(0,len(negative)-1)])

def get_positive_message():
    file = open("positive.txt")
    global positive
    positive = file.read().splitlines()
    file.close()

async def print_positive_message(message):
    global positive
    await message.channel.send(positive[randint(0,len(positive)-1)])

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    get_greet()
    get_negative_message()
    get_positive_message()

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id != 974351951812788274:
        return

    if message.content.startswith('$hello'):
        await greet(message)
    if "seraphine" in message.content.lower() and TextBlob(message.content).sentiment.polarity >= 0:
        await print_positive_message(message)
    elif "seraphine" in message.content.lower():
        await print_negative_message(message)

if __name__ == "__main__":
    client.run(config.token)

