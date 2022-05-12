import discord
from random import randint

client = discord.Client()

firstmove = []

def get_first_move():
    file = open("firstmove.txt")
    global firstmove
    firstmove = file.read().splitlines()
    file.close()

async def print_first_move(message):
    global firstmove
    await message.channel.send(firstmove[randint(0,len(firstmove)-1)])

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await print_first_move(message)

    if message.content.lower() == "i love you seraphine":
        await message.channel.send("I love you too <@" + str(message.author.id) + ">")

    if message.content.lower() == "$kiss":
        await message.channel.send("uwu not now <@" + str(message.author.id) + ">")


client.run('')

