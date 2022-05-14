from discord.ext import commands
import config


class admin_commands(commands.Cog):
    # Attributes
    channels = config.channels

    curr_channel_id = channels["personal"]
    curr_channel = "personal"



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


def setup(bot):
    bot.add_cog(admin_commands(bot))
