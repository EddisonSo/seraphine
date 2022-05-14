from discord.ext import commands
import config

bot = commands.Bot("$", case_insensitive=True)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# Bot command error handling
@bot.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.channel.send("uwu I don't seem to understand that >.<")


if __name__ == "__main__":
    bot.load_extension("user_commands")
    bot.load_extension("user_message")
    bot.load_extension("admin_commands")
    bot.run(config.token)

