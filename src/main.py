import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

print("Loading all commands...")

# Remove the default help command:
bot.remove_command('help')
# Load the class in "commands.py":
bot.load_extension("commands")


# Helper methods for loading custom help & credit command:
def get_commands():
    # Get list of command names & briefs (ordered pairs)
    command_cog = bot.get_cog("commands")
    cmd_list = [command.name for command in command_cog.get_commands()]
    brief_list = [command.brief for command in command_cog.get_commands()]
    return cmd_list, brief_list


def format_help_command_text(cmd_list):
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
    embed_msg.add_field(name="Additional Options", value=detailed, inline=False)
    embed_msg.set_footer(text="PolyBot")
    return embed_msg


def initialise_credit_text():
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
    return embed_msg


# Load custom help command
COMMANDS, COMMAND_DETAILS = get_commands()
MAIN_HELP_TEXT = format_help_command_text(COMMANDS)
# Load credit text
CREDIT_TEXT = initialise_credit_text()
print("Finished loading commands!")


@bot.event
async def on_ready():
    print("Bot is now online!")  # Print this when the bot is online


@bot.command(name='help', pass_context=True)  # Here is our own help command we add
async def help_command(ctx):
    args = ctx.message.content.split(" ")
    if len(args) > 2:  # (Sanity check) Reject odd formats - Added by KOOKIIE
        await ctx.send(
            "The format of !help is either '!help' or '!help <command>'"
        )
        return

    # Give description of command - Added by KOOKIIE
    # Check if it's of the format "!help <command>"
    # short-circuits if there's 1 arg after "!help"
    if len(args) == 2:
        if args[1] in COMMANDS:
            await ctx.send(  # map name to brief:
                f"**!{args[1]}**: {COMMAND_DETAILS[COMMANDS.index(args[1])]}"
            )
            # E.g.: For "!help translate", it sends:
            # !**Translate**: Translates messages between 2 different languages.
            return
        else:
            await ctx.send(f"Could not find the command `!{args[1]}`")
            return

    await ctx.send(embed=MAIN_HELP_TEXT)


@bot.command(name='credit', pass_context=True)  # Here is our own help command we add
async def credit_command(ctx):
    await ctx.send(embed=CREDIT_TEXT)


if __name__ == '__main__':
    print("Loading Bot...")
    bot.run("TOKEN HERE")
