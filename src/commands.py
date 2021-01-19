from decimal import Decimal

import discord
from discord.ext import commands
from translate import Translator
from forex_python.converter import CurrencyRates, CurrencyCodes
import random


class Commands(commands.Cog, name="commands"):
    """Cog class that handle ALL the commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.eight_ball_responses = (
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt',
            'Yes - definitely',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            'Don\'t count on it.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.',
        )

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

        await ctx.send(f"Hexadecimal: 0x{str(number)[2:].upper()}")

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

    @commands.command(name="8ball", pass_context=True)
    async def eight_ball(self, ctx):
        args = ctx.message.content.split(" ")
        if len(args) < 3:
            await ctx.send("What are you asking, please provide a longer question.")
            return

        random_num = random.randrange(0, len(self.eight_ball_responses) - 1)
        color = 0x00FF00  # Defaults to green

        if 9 < random_num < 14:
            color = 0xFFFF00
        elif 15 <= random_num < 19:
            color = 0xFF0000

        embed = discord.Embed(
            title="Eight Ball",
            color=color
        ).add_field(name="Output",
                    value=f"```{self.eight_ball_responses[random_num]}```")

        embed.set_footer(text="PolyBot")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Commands(bot))
