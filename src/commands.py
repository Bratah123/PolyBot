from decimal import Decimal

from discord.ext import commands
from translate import Translator
from forex_python.converter import CurrencyRates, CurrencyCodes


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
        if len(args) < 4:
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

    @commands.command(name="tohex", pass_context=True)
    async def to_hex(self, ctx):
        args = ctx.message.content.split(" ")
        if len(args) < 2:
            await ctx.send("Please provide all necessary arguments. !tohex <decimal_number>")
            return

        try:
            number = hex(int(args[1]))
        except Exception as e:
            print(e)
            await ctx.send("That is not a valid decimal number.")
            return

        await ctx.send(f"Hexadecimal: {number}")

    @commands.command(name="todec", pass_context=True)
    async def to_dec(self, ctx):
        args = ctx.message.content.split(" ")
        if len(args) < 2:
            await ctx.send("Please provide all necessary arguments. !todec <hex_number>")
            return

        try:
            number = int(args[1], 16)
        except Exception as e:
            print(e)
            await ctx.send("That is not a valid hex number.")
            return

        await ctx.send(f"Decimal: {number}")

    @commands.command(name="currency", pass_context=True)
    async def to_currency(self, ctx):
        args = ctx.message.content.split(" ")
        if len(args) < 4:
            await ctx.send("Please provide all necessary arguments. !currency <from> <to> <$amount>")
            return
        # Takes in args like USD, SGD, CAD, EUR

        currency_from = args[1].upper()
        currency_to = args[2].upper()

        try:
            amount = Decimal(args[3])
        except Exception as e:
            print(e)
            await ctx.send("Please provide a valid amount.")
            return

        c = CurrencyRates()
        s = CurrencyCodes()

        try:
            converted_amount = round(c.convert(currency_from, currency_to, amount), 2)
        except Exception as e:
            print(e)
            await ctx.send("Please provide a valid currency code (I.E. USD, SGD, CAD)")
            return

        await ctx.send(f"{currency_from} to {currency_to}: {s.get_symbol(currency_to)}{converted_amount}")


def setup(bot):
    bot.add_cog(Commands(bot))
