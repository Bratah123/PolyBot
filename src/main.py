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
    args = ctx.message.content.split(" ")
    if len(args) > 2:  # Reject odd formats - Added by KOOKIIE
        await ctx.send(
            "The format of !help is either '!help' or '!help <command>'"
        )

    command_cog = bot.get_cog("commands")
    # Get list of command names & briefs (ordered pairs)
    cmd_list = [command.name for command in command_cog.get_commands()]
    brief_list = [command.brief for command in command_cog.get_commands()]

    # Give description of command - Added by KOOKIIE
    # Check if it's of the format "!help <command>"
    # short-circuits if there's 1 arg after "!help"
    if len(args) == 2:
        if args[1] in cmd_list:
            await ctx.send(  # map name to brief:
                f"**!{args[1]}**: {brief_list[cmd_list.index(args[1])]}"
            )
            # For "!help translate", it sends:
            # !**Translate**: Translates messages between 2 different languages.
            return
        else:
            await ctx.send(f"Could not find the command '{args[1]}'")
            return

    # Flatten command-name list to String, to add to embed
    cmd_list_str = "\n".join(cmd_list)
    detailed = (
        "\nYou may use `!help <command>` for detailed help for "
        "individual commands:\n**E.g.**: `!help quote`"
    )

    # Boiler plate embed message builder
    embed_msg = discord.Embed(
        title="Commands",
        description="All commands for PolyBot",
        color=0x00FFFF,
    )

    embed_msg.add_field(name="User Commands", value=cmd_list_str, inline=False)
    embed_msg.add_field(name="Additioanl Options", value=detailed, inline=False)
    embed_msg.set_footer(text="PolyBot")

    await ctx.send(embed=embed_msg)


@bot.command(name='credit', pass_context=True)  # Here is our own help command we add
async def credit_command(ctx):
    # Boiler plate embed message builder
    embed_msg = discord.Embed(
        title="About",
        description="PolyBot is an all-in-one utility bot created by Brandon",
        color=0x00FFFF,
    )
    links = (
        "GitHub: <https://github.com/Bratah123/> \n"
        "Website: <https://www.bratah.org/> \n"
        "Repository: <https://github.com/Bratah123/PolyBot/>"
    )
    embed_msg.add_field(name="Links", value=links, inline=False)
    embed_msg.set_footer(text="PolyBot")
    await ctx.send(embed=embed_msg)


if __name__ == '__main__':
    print("Loading Bot..")
    bot.run("")
