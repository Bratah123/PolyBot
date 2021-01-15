import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

print("Loading all commands...")

# We remove the help command because we want to add our own fancy one!
bot.remove_command('help')

# load the class in "commands.py"
bot.load_extension("commands")
print("Finished loading commands!")


@bot.event
async def on_ready():
    print("Bot is now online!")  # Print this when the bot is online


@bot.command(name='help', pass_context=True)  # Here is our own help command we add
async def help_command(ctx):
    command_cog = bot.get_cog("commands")

    cmd_list = [command.name + "\n" for command in command_cog.get_commands()]
    cmd_list_str = ""

    # Add every command into the string for the embed we are going to send
    for cmd in cmd_list:
        cmd_list_str += cmd

    # Boiler plate embed message builder
    embed_msg = discord.Embed(
        title="Commands",
        description="All commands for PolyBot",
        color=0x00FFFF,
    )

    embed_msg.add_field(name="User Commands", value=cmd_list_str, inline=False)
    embed_msg.set_footer(text="PolyBot")

    await ctx.send(embed=embed_msg)


if __name__ == '__main__':
    print("Loading Bot..")
    bot.run("TOKEN HERE")
