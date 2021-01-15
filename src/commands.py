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
            ctx.send("Please provide all necessary arguments. !translate <from> <to> <message>")
            return

        lang_from = args[1]
        lang_to = args[2]
        message = args[2:]

        translator = Translator(from_lang=lang_from, to_lang=lang_to)

        try:
            translation = translator.translate(message)
        except Exception as e:
            await ctx.send("That is an invalid language to translate")
            print(e)
            return

        await ctx.send("Translation:", translation)


def setup(bot):
    bot.add_cog(Commands(bot))
