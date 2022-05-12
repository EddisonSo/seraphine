import discord
from random import randint
from textblob import TextBlob
#from time import sleep

client = discord.Client()

greet = []
positive = []
negative = []

def get_greet():
    file = open("greet.txt")
    global first_move
    greet = file.read().splitlines()
    file.close()

async def print_first_move(message):
    global first_move
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
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await print_first_move(message)

    if "seraphine" in message.content and TextBlob(message.content).sentiment.polarity >= 0:
        await print_positive_message(message)
    else:
        await print_negative_message(message)


client.run('')

