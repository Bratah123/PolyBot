import random
from decimal import Decimal

import discord
from discord.ext import commands
from translate import Translator
from forex_python.converter import CurrencyRates, CurrencyCodes

import utility


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

    @commands.command(
        name="translate",
        pass_context=True,
        brief="Translates messages between 2 different languages."
    )
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

    @commands.command(
        name="tohex",
        pass_context=True,
        brief="Converts decimal numbers to hexadecimal."
    )
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

    @commands.command(
        name="fromhex",
        pass_context=True,
        brief="Converts hexadecimal numbers to decimal."
    )
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

    @commands.command(
        name="currency",
        pass_context=True,
        brief="Converts a monetary value between 2 real currencies. (Forex-based)"
    )
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

    @commands.command(
        name="8ball",
        pass_context=True,
        brief="Answers a yes-no question; Mattel Magic 8-Ball simulator."
    )
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

    @commands.command(
        name="coinflip",
        brief="Coin-flip simulator."
    )
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

    @commands.command(
        name="tobinary",
        pass_context=True,
        brief="Converts decimal numbers to binary."
    )
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

    @commands.command(
        name="frombinary",
        pass_context=True,
        brief="Converts binary numbers to decimal."
    )
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

    @commands.command(
        name="diceroll",
        brief="Dice-roll simulator."
    )
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

    @commands.command(
        name="roll",
        brief="Pseudo-random number generator."
    )
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

    @commands.command(
        name="toascii",
        pass_context=True,
        brief="Converts binary representations to ASCII."
    )
    async def bin_to_ascii(self, ctx):
        # @author KOOKIIE
        args = ctx.message.content.split(" ")
        if len(args) < 2:
            await ctx.send("Please provide all necessary arguments. !toascii <binary string>")
            return
        bin_list = args[1:]  # remove command part
        ascii_data = ""  # initialise
        for element in bin_list:  # use int() to read as base 2:
            ascii_data = ascii_data + chr(int(element, 2))  # (chr) cast to String for concat
        await ctx.send(f"ASCII: {ascii_data}")

    @commands.command(
        name="fromascii",
        pass_context=True,
        brief="Converts ASCII to binary representation."
    )
    async def bin_from_ascii(self, ctx):
        # @author KOOKIIE
        args = ctx.message.content.split(" ")
        if len(args) < 2:
            await ctx.send("Please provide all necessary arguments. !fromascii <ASCII string>")
            return
        ascii_string = " ".join(args[1:])  # remove command part
        # Use bytearray() to convert to binary value
        # Then use format() to pad the front with 0s to make up to 7
        bin_string = "".join("{:0>7b}".format(i) for i in bytearray(ascii_string, encoding='utf-8'))
        bin_list = []  # initialise
        for i in range(0, len(bin_string), 7):
            bin_list.append(bin_string[i:i + 7])  # format into 7 digit chunks
        bin_string = " ".join(bin_list)  # add spaces
        await ctx.send(f"Binary: {bin_string}")

    @commands.command(
        name="length",
        pass_context=True,
        brief="Converts between Imperial (U.S. customary) and SI length units. E.g. *km* to *mi*, or *ft* to *cm*."
    )
    async def length_conversion(self, ctx):
        # @author KOOKIIE
        args = ctx.message.content.split(" ")
        if len(args) < 4:
            await ctx.send(
                "Please provide all necessary arguments. !length <from> <to> <value>\n"
                "Valid units: km, m, cm, mi, ft, in"
            )
            return
        # Takes in args like km, m, cm, mi, ft, in
        unit_from = args[1].lower()
        unit_to = args[2].lower()
        source_value = float(args[3])

        # SI to Imperial
        if unit_from in utility.SI_UNITS:  # do conversions as km-mi
            source_in_km = utility.to_km(source_value, unit_from)
            source_in_mi = source_in_km * 0.621371192
            if unit_to == "mi":
                output = source_in_mi
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            elif unit_to == "ft":
                output_ft_component = source_in_mi * 5280
                if not int(output_ft_component):
                    # if ft component < 1
                    await ctx.send(f"{source_value}*{unit_from}* = {output_ft_component:.2f}*{unit_to}* (2dp)")
                    return
                else:
                    output_in_component = (output_ft_component - int(output_ft_component)) * 12
                    await ctx.send(f"{source_value}*{unit_from}* = {int(output_ft_component)}*{unit_to}* {output_in_component:.2f}*in* (2dp)")
                    return
            elif unit_to == "in":
                output = source_in_mi * 63360
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            else:
                await ctx.send("Invalid units!")
                return

        # Imperial to SI
        if unit_from in utility.IMPERIAL_UNITS:  # do conversions as km-mi
            source_in_mi = utility.to_mi(source_value, unit_from)
            source_in_km = source_in_mi / 0.621371192
            if unit_to == "km":
                output = source_in_km
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            elif unit_to == "m":
                output_m_component = source_in_km * 1000
                if not int(output_m_component):
                    # if m component < 1
                    await ctx.send(f"{source_value}*{unit_from}* = {output_m_component:.2f}*{unit_to}* (2dp)")
                    return
                else:
                    output_cm_component = (output_m_component - int(output_m_component)) * 100
                    await ctx.send(f"{source_value}*{unit_from}* = {int(output_m_component)}*{unit_to}* {output_cm_component:.2f}*cm* (2dp)")
                    return
            elif unit_to == "cm":
                output_cm_component = source_in_km * 100000
                if not int(output_cm_component):
                    # if cm component < 1
                    await ctx.send(f"{source_value}*{unit_from}* = {output_cm_component:.2f}*{unit_to}* (2dp)")
                    return
                else:
                    output_mm_component = (output_cm_component - int(output_cm_component)) * 10
                    await ctx.send(f"{source_value}*{unit_from}* = {int(output_cm_component)}*{unit_to}* {output_mm_component:.2f}*cm* (2dp)")
                    return
            elif unit_to == "mm":
                output = source_in_km * 1000000
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            else:
                await ctx.send("Invalid units!")
                return
        # Sanity-check:
        await  ctx.send("Invalid units!")

    @commands.command(
        name="weight",
        pass_context=True,
        brief="Converts between Imperial (U.S. customary) and SI mass units. E.g. *kg* to *lbs*, or *oz* to *g*."
    )
    async def weight_conversion(self, ctx):
        # @author KOOKIIE
        args = ctx.message.content.split(" ")
        if len(args) < 4:
            await ctx.send(
                "Please provide all necessary arguments. !weight <from> <to> <value>\n"
                "Valid units: kg, g, lbs, oz"
            )
            return
        # Takes in args like kg, g, lbs, oz
        unit_from = args[1].lower()
        unit_to = args[2].lower()
        source_value = float(args[3])

        # SI to Imperial
        if unit_from in utility.SI_UNITS:  # do conversions as kg-lbs
            source_in_kg = utility.to_kg(source_value, unit_from)
            source_in_lbs = source_in_kg / 0.45359237
            if unit_to == "lbs":
                output = source_in_lbs
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            elif unit_to == "oz":
                output = source_in_lbs * 16
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            else:
                await ctx.send("Invalid units!")
                return

        # Imperial to SI
        if unit_from in utility.IMPERIAL_UNITS:  # do conversions as km-mi
            source_in_lbs = utility.to_lbs(source_value, unit_from)
            source_in_kg = source_in_lbs * 0.45359237
            if unit_to == "kg":
                output = source_in_kg
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            elif unit_to == "g":
                output = source_in_kg * 1000
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            else:
                await ctx.send("Invalid units!")
                return
        # Sanity-check:
        await ctx.send("Invalid units!")

    @commands.command(
        name="liquid",
        pass_context=True,
        brief=(
                "Converts between Imperial (U.S. customary) and SI volume units. "
                "E.g. *l* to *pint*, or *oz* to *l*.\n"
                "Note: *oz* is understood as 'US fl oz' here"
        )
    )
    async def liquid_conversion(self, ctx):
        # @author KOOKIIE
        args = ctx.message.content.split(" ")
        if len(args) < 4:
            await ctx.send(
                "Please provide all necessary arguments. !liquid <from> <to> <value>\n"
                "Valid units: ml, l, oz, pint, gallon"
            )
            return
        # Takes in args like ml, l, oz, pint, gallon
        unit_from = args[1].lower()
        unit_to = args[2].lower()
        source_value = float(args[3])

        # SI to Imperial
        if unit_from in utility.SI_UNITS:  # do conversions as ml-oz
            source_in_ml = utility.to_ml(source_value, unit_from)
            source_in_oz = source_in_ml / 29.57
            if unit_to == "oz":
                output = source_in_oz
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            elif unit_to == "pint":
                output = source_in_oz / 16
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            elif unit_to == "gallon":
                output = source_in_oz / 128
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            else:
                await ctx.send("Invalid units!")
                return

        # Imperial to SI
        if unit_from in utility.IMPERIAL_UNITS:
            source_in_oz = utility.to_oz(source_value, unit_from)
            source_in_ml = source_in_oz * 29.57
            if unit_to in ("ml", "cc"):
                output = source_in_ml
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            elif unit_to == "l":
                output = source_in_ml / 1000
                await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")
                return
            else:
                await ctx.send("Invalid units!")
                return

        # Sanity-check:
        await ctx.send("Invalid units!")

    @commands.command(
        name="temp",
        pass_context=True,
        brief=(
                "Converts between various temperature units. "
                "E.g. *F* to *C*, or *C* to *K*.\n"
        )
    )
    async def temp_conversion(self, ctx):
        # @author KOOKIIE
        args = ctx.message.content.split(" ")
        if len(args) < 4:
            await ctx.send(
                "Please provide all necessary arguments. !temp <from> <to> <value>\n"
                "Valid units: C, F, K"
            )
            return
        # Takes in args like C, F, K
        unit_from = args[1].upper()  # Catch for non-cap spellings
        unit_to = args[2].upper()
        source_value = float(args[3])
        output = 0

        # 3P2 = 6 possible permutations
        # Calls the appropriate converter from utility.py
        if unit_from == "C" and unit_to == "K":
            output = utility.c_to_k(source_value)
        elif unit_from == "K" and unit_to == "C":
            output = utility.k_to_c(source_value)
        elif unit_from == "F" and unit_to == "K":
            output = utility.f_to_k(source_value)
        elif unit_from == "K" and unit_to == "F":
            output = utility.k_to_f(source_value)
        elif unit_from == "F" and unit_to == "C":
            output = utility.f_to_k(source_value)
            output = utility.k_to_c(output)
        elif unit_from == "C" and unit_to == "F":
            output = utility.c_to_k(source_value)
            output = utility.k_to_f(output)
        else:
            # Sanity-check:
            await ctx.send("Invalid units!")
            return  # short-circuit for invalid units

        await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")


def setup(bot):
    bot.add_cog(Commands(bot))
