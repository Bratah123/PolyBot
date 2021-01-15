from discord.ext import commands
from translate import Translator


class Commands(commands.Cog, name="commands"):
    """Cog class that handle ALL the commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="translate", pass_context=True)
    async def translate(self, ctx):
        args = ctx.message.content.split(" ")
        # arguments we are looking for
        # language from -> to
        # !translate <from> <to> <message>
        if len(args) < 3:
            await ctx.send("Please provide all necessary arguments. !translate <from> <to> <message>")
            return

        lang_from = args[1]
        lang_to = args[2]

        message_list = args[3:]
        message = ""

        for word in message_list:
            message += word + " "

        translator = Translator(from_lang=lang_from, to_lang=lang_to)
        await ctx.send("Translating message please give me a moment...")

        translation = translator.translate(message)

        await ctx.send("Translation: " + translation)


def setup(bot):
    bot.add_cog(Commands(bot))
