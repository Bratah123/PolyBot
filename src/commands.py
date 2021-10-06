import random
from decimal import Decimal
from datetime import datetime
from dateutil import tz

import discord
from discord.ext import commands
from translate import Translator
from forex_python.converter import CurrencyRates, CurrencyCodes

import units
import yaml_parser
import struct


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
        self.QUOTE_LIBRARY = yaml_parser.yaml_load("quote_library.yaml")
        self.QUOTABLE_AUTHORS = [entry["name"] for entry in self.QUOTE_LIBRARY.values()]

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
        name="toaob",
        pass_context=True,
        brief="Converts decimal number to array of bytes."
    )
    async def to_aob(self, ctx):
        args = ctx.message.content.split()
        if len(args) < 2:
            await ctx.send("Please provide all necessary arguments. !toaob <decimal_number>")
            return

        try:
            num_to_convert = int(args[1])
        except Exception as e:
            print(e)
            await ctx.send("That is not a valid decimal number")
            return
        # This is so ugly, but basically it removes the b'' part in bytes like objects in python
        # for example b'xff\xff\xff\xff' -> FF FF FF FF
        aob = " ".join("".join(str(struct.pack("i", num_to_convert))[1:]).replace("'", "").replace("\\", "").split("x"))
        await ctx.send("AOB: " + aob.upper())

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
        if unit_from in units.SI_UNITS:
            await ctx.send(units.length_si_to_imperial(unit_from, unit_to, source_value))

        # Imperial to SI
        elif unit_from in units.IMPERIAL_UNITS:
            await ctx.send(units.length_imperial_to_si(unit_from, unit_to, source_value))

        # Sanity-check:
        else:
            await ctx.send("Invalid units!")

    @commands.command(
        name="weight",
        pass_context=True,
        brief="Converts between Imperial (U.S. customary) and SI mass units. E.g. *kg* to *lbs*, or *oz* to *g*."
    )
    async def weight_conversion(self, ctx):
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
        if unit_from in units.SI_UNITS:
            await ctx.send(units.weight_si_imperial(unit_from, unit_to, source_value))

        # Imperial to SI
        elif unit_from in units.IMPERIAL_UNITS:
            await ctx.send(units.weight_imperial_si(unit_from, unit_to, source_value))

        # Sanity-check:
        else:
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
        if unit_from in units.SI_UNITS:
            await ctx.send(units.liquid_si_imperial(unit_from, unit_to, source_value))

        # Imperial to SI
        elif unit_from in units.IMPERIAL_UNITS:
            await ctx.send(units.liquid_imperial_si(unit_from, unit_to, source_value))

        # Sanity-check:
        else:
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
        # Calls the appropriate converter from units.py
        if unit_from == "C" and unit_to == "K":
            output = units.c_to_k(source_value)
        elif unit_from == "K" and unit_to == "C":
            output = units.k_to_c(source_value)
        elif unit_from == "F" and unit_to == "K":
            output = units.f_to_k(source_value)
        elif unit_from == "K" and unit_to == "F":
            output = units.k_to_f(source_value)
        elif unit_from == "F" and unit_to == "C":
            output = units.f_to_k(source_value)
            output = units.k_to_c(output)
        elif unit_from == "C" and unit_to == "F":
            output = units.c_to_k(source_value)
            output = units.k_to_f(output)
        else:
            # Sanity-check:
            await ctx.send("Invalid units!")
            return  # short-circuit for invalid units

        await ctx.send(f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)")

    @staticmethod
    def snowflake_to_unix(snowflake):
        snowflake_bin = bin(snowflake).replace('0b', '')  # 'str' type
        ms_since_epoch_bin = snowflake_bin[:-22]  # strip trailing data
        ms_since_epoch = int(ms_since_epoch_bin, 2)  # cast back to decimal
        ms_since_epoch += 1420070400000  # add Discord Epoch UNIX timestamp
        sec_since_epoch = ms_since_epoch / 1000  # milliseconds to seconds
        return sec_since_epoch

    @commands.command(
        name="timestamp",
        pass_context=True,
        brief=(
                "***NOTE: DEVELOPERS' TOOL!***\n"
                "Gets a Discord message's timestamp (in the form: `Hour:Minute:Second Day/Month/Year`) "
                "from a Discord snowflake ID.\n"
                "Format: either `!timestamp <snowflake ID>` (defaults to Pacific Time) *or* "
                "`!timestamp <Canonical Olson Database Name> <snowflake ID>`\n"
                "Example: `!timestamp Asia/Seoul 814031888037445673`\n"
                "*See here for full list of canonical names*: "
                "https://github.com/Bratah123/PolyBot/blob/main/timezone_names.txt"
        )
    )
    async def get_timestamp(self, ctx):
        args = ctx.message.content.split(" ")
        if (len(args) < 2) or (len(args) > 3):
            await ctx.send(
                "Invalid format - too few/many arguments!\n"
                "See `!help timestamp` for examples of valid inputs."
            )
            return

        # Grab snowflake ID and timezone
        canonical = ""
        if len(args) == 2:
            snowflake_literal = args[1]
        else:
            canonical += args[1]  # Prevent NPE
            snowflake_literal = args[2]
        # Sanity check:
        try:
            snowflake = int(snowflake_literal)  # filter junk input
        except Exception as e:
            print(f"Error encountered whilst casting snowflake ID to 'int':\n  {e}")
            await ctx.send(
                "Invalid arguments!\n"
                "Discord Snowflake IDs should be numbers.\n"
                "See `!help timestamp` for examples of valid inputs."
            )
            return

        # process intermediates
        # see: https://discord.com/developers/docs/reference#convert-snowflake-to-datetime
        sec_since_epoch = self.snowflake_to_unix(snowflake)
        if not canonical:  # canonical empty (i.e. timezone not provided)
            target_tz = tz.gettz("America/Los_Angeles")
        else:
            try:
                target_tz = tz.gettz(canonical)
            except Exception as e:
                print(f"Error encountered whilst fetching tzinfo object:\n  {e}")
                await ctx.send(
                    "I'm afraid I couldn't parse your timezone!\n"
                    "Please use this list of valid canonical names as reference: "
                    "https://github.com/Bratah123/PolyBot/blob/main/timezone_names.txt"
                )
                return
        discord_tz = tz.tzutc()
        datetime_of_message = datetime.fromtimestamp(sec_since_epoch, discord_tz)
        # datetime object is naive:
        datetime_of_message = datetime_of_message
        # convert to appropriate timezone, and format
        try:
            output = datetime_of_message.astimezone(target_tz).strftime("%H:%M:%S %d/%m/%Y")
        except Exception as e:
            print(f"Error encountered whilst formatting datetime object:\n  {e}")
            await ctx.send("An unexpected error has occurred! Check logs for details!")
            return

        await ctx.send(f"The timestamp of the message you requested is: {output}")

    def pick_quote_from_dict(self, person_to_quote):
        quotes = self.QUOTE_LIBRARY[person_to_quote]["quotes"]
        random_quote = quotes[random.randint(0, len(quotes) - 1)]
        return f"\"{random_quote}\"\n  - {self.QUOTE_LIBRARY[person_to_quote]['name']}"

    def author_is_known(self, author):
        """Checks if an author is catalogued in the quote library

        Args:
            author: String, author's name

        Returns:
            String, random quote if the author is known
            String, empty if the author is unknown
        """
        for person_to_quote, entry in self.QUOTE_LIBRARY.items():  # for each known author
            if author.lower() in entry["alias"]:  # alias match
                return self.pick_quote_from_dict(person_to_quote)
        return ""  # No matches

    @staticmethod
    async def pick_quote_from_history(ctx):  # 'ctx' is a discord.py construct
        messages = await ctx.message.channel.history(limit=200).flatten()
        rand_num = random.randint(0, len(messages) - 1)
        # '!quote' and bot messages are not wanted;
        # get a new pseudo-random number if message is undesired
        while (
                (not messages[rand_num].content) or
                (messages[rand_num].content.startswith("!")) or
                messages[rand_num].author.bot
        ):
            rand_num = random.randint(0, len(messages) - 1)
        return f"\"{messages[rand_num].content}\"\n  - {messages[rand_num].author.name}"

    @commands.command(
        name="quote",
        pass_context=True,
        brief="Grabs a random message from the channel that a user typed.\nYou can also do `!quote sun "
              "tzu` for Sun Tzu quotes (more to come).\n*Alternatively, you may use `!quote surprise me` to get "
              "a random quote from any author that PolyBot knows!*"
    )
    async def handle_quote(self, ctx):
        args = ctx.message.content.split()

        # Check for quotes in library, if args provided
        if len(args) > 1:
            # Format author name to lower case
            # Try-catch not needed, since Discord message is parsed as String
            person_to_quote = " ".join([word.lower() for word in args[1:]])

            if person_to_quote == "list":  # List all known authors
                await ctx.send(
                    "**List of quotable authors:**\n> " +
                    ", ".join(self.QUOTABLE_AUTHORS)
                )
                return  # short-circuit

            if person_to_quote in ("surpriseme", "surprise me"):  # give random quote in library
                rand_author = random.choice(list(self.QUOTE_LIBRARY.keys()))
                await ctx.send(self.pick_quote_from_dict(rand_author))
                return  # short-circuit

            # search for particular author
            search_result = self.author_is_known(person_to_quote)
            if search_result:  # If not found, search_result is falsy
                await ctx.send(search_result)
                return

            else:  # catch-all
                await ctx.send("I'm so sorry, but I'm afraid I do not know of any quotes from such a person. :pensive:")
                return

        # Random messages from the channel, if no args provided
        output = await self.pick_quote_from_history(ctx)
        await ctx.send(output)


def setup(bot):
    bot.add_cog(Commands(bot))
