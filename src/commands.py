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
        self.dice_images = (
            "https://cdn.discordapp.com/attachments/731528944402300977/801529918630002688/dice-six-faces-one.png",
            "https://cdn.discordapp.com/attachments/731528944402300977/801529934744256612/dice-six-faces-two.png",
            "https://cdn.discordapp.com/attachments/731528944402300977/801529945243123712/dice-six-faces-three.png",
            "https://cdn.discordapp.com/attachments/731528944402300977/801529959863549962/dice-six-faces-four.png",
            "https://cdn.discordapp.com/attachments/731528944402300977/801529976372985866/dice-six-faces-five.png",
            "https://cdn.discordapp.com/attachments/731528944402300977/801529992144093194/dice-six-faces-six.png"
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

    @commands.command(name="fromhex", pass_context=True)
    async def to_dec(self, ctx):
        args = ctx.message.content.split(" ")
        if len(args) < 2:
            await ctx.send("Please provide all necessary arguments. !fromhex <hex_number>")
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

    @commands.command(name="coinflip")
    async def coin_flip(self, ctx):
        heads_or_tails = random.randint(1, 2)
        text = ""
        if heads_or_tails == 1:
            # heads
            text = "Heads"
            pic = "https://media.discordapp.net/attachments/631249406775132182/801205446115065926/fMemdeFmPeYAAAAAASUVORK5CYII.png"
        else:
            # tails
            text = "Tails"
            pic = "https://cdn.discordapp.com/attachments/631249406775132182/801205566877728798/Y5vgPrzC7Iazmd78B6LVfyzD7HfwBKvIh3eeptpAAAAABJRU5ErkJggg.png"

        embed = discord.Embed(
            title="Coin Flip",
            description=text,
            color=0x00FF00,
        )
        embed.set_image(url=pic)
        embed.set_footer(text="PolyBot")
        await ctx.send(embed=embed)

    @commands.command(name="tobinary", pass_context=True)
    async def to_binary(self, ctx):
        args = ctx.message.content.split(" ")
        if len(args) < 2:
            await ctx.send("Please provide all necessary arguments. !tobinary <number>")
            return

        try:
            num = int(args[1])
        except Exception as e:
            print(e)
            await ctx.send(e)
            return

        await ctx.send(f"Binary: {bin(num).replace('0b', '')}")

    @commands.command(name="frombinary", pass_context=True)
    async def from_binary(self, ctx):
        args = ctx.message.content.split(" ")
        if len(args) < 2:
            await ctx.send("Please provide all necessary arguments. !frombinary <number>")
            return

        try:
            num = int(args[1], 2)
        except Exception as e:
            print(e)
            await ctx.send(e)
            return

        await ctx.send(f"Decimal: {num}")

    @commands.command(name="diceroll")
    async def dice_roll(self, ctx):
        dice = [1, 2, 3, 4, 5, 6]
        number = random.randint(0, 5)
        image = self.dice_images[number]
        embed = discord.Embed(
            title="Dice roll",
            color=0x00FFFF,
        )
        embed.set_footer(text="PolyBot")
        embed.set_image(url=image)
        embed.add_field(name="Output", value=f"```py\nYou rolled {dice[number]}```")
        await ctx.send(embed=embed)

    @commands.command(name="roll")
    async def roll(self, ctx):
        args = ctx.message.content.split(" ")
        if len(args) < 3:
            await ctx.send("Please provide all necessary arguments. !roll <number> <number2>")
            return
        try:
            number_one = int(args[1])
            number_two = int(args[2])
            if number_one > number_two:
                await ctx.send("The first given number must be lower than the second number.")
                return
        except ValueError:
            await ctx.send("Please use numbers.")
            return
        number = random.randint(number_one, number_two)
        embed = discord.Embed(
            title="Roll",
            color=0x00FFFF,
        )
        embed.set_footer(text="PolyBot")
        embed.add_field(name="Output", value=f"```py\nYou rolled {number}```")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Commands(bot))
