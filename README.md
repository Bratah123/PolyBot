# PolyBot
PolyBot initially started as a simple Discord bot that provided conversions between many different data types (i.e. language, units of measurements, etc).  

We hope that with the help of Poly, users will be able to perform a myriad of actions whilst in Discord, without needing to reach for the web browser - be it converting between currencies like USD and CAD, finding the timestamp of an old Discord message from its snowflake ID, or more!  

Over time, Poly has slowly grown to encompass a wide variety of functions. To see the full list of commands, issue `!help` to Poly.  
You may also use the format `!help <command>` to see details for what a particular command does.  

~~Poly is hosted via AWS: Click here to add the bot to your server now!

## Features (non-exhaustive)
- Currency Conversion
- Hexadecimal Conversion
- Binary Conversion
- Translations
- Eight ball
- Coin Flip
- Dice roll
- Roll Command

## Gallery
![gallery](https://media.discordapp.net/attachments/631249406775132182/799770724591468604/3443bba7bace8052f9f17eeabf15d653.png)

![help_command](https://cdn.discordapp.com/attachments/631249406775132182/799771101143498752/8fe54bc717cdd0cd489f164f149ac32f.png)

## Set-up For Testing & Developing
Windows:  
1. Install Python 3.6+
2. Run `setup.bat`
    - This creates a local virtual environment, and adds the required dependencies
3. Either run `src/main.py` manually, or use `start.bat`

## About Commit 334c4f1
[CVE-2021-21330 - GitHub Advisory Database](https://github.com/advisories/GHSA-v6wp-4m6f-gcjg)  
Following the release of the advisory (see above), we have updated dependencies to include the security patch(es).  

#### If you cloned/downloaded PolyBot prior to this commit, please update ASAP!

*Note: `aiohttp` is a library used by `discord.py`, which is the basis for most Python-based bots for Discord, including `PolyBot`*.  
### To grab the updates (Applicable for all kinds of dependency updates)
1. Perform `git pull`
2. Grab the new dependencies  
    - For Global Environment:  
      - `pip install -r requirements.txt`  
    - For Virtual Environment:  
      - `venv/scripts/activate`  
      - `pip install -r requirements.txt`  
