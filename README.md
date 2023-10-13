# TheGoblinsNotebot
A Discord bot to retrieve entries from The Goblin's Notebook and post them to Discord.

# How To Operate

## Create a Discord Bot App
Follow the guides at:
  - https://discordjs.guide/preparations/setting-up-a-bot-application.html
  - https://discordjs.guide/preparations/adding-your-bot-to-servers.html

## Get Your Environment Running

## Python
This bot is writting in Python with use of the Interactions.py library found at https://interactions-py.github.io/interactions.py/
You'll need an operation Python install that is up and available so long as you want your Goblin's Notebot alive.  I suggest a small free VM at any of the major providers.  All you really need is Python3 and the Python libraries included in the single file that makes up the bot. If these aren't already in your Python environment, simply grab them using pip or whichever other method you prefer or your environment employs.
 
### Create An .env File 
You'll alsp need a .env file which conatins the following keys and values used by the script to access the API at https://www.the-goblin.net/.  

GOBLIN_CAMPAIGN_ID = "xxxxxxxx"
GOBLIN_OWNER_API_KEY = "xxxxxxxxxx"
GOBLIN_OWNER_SECRET = "<Secret>"
GOBLIN_PLAYER_API_KEY = "xxxxxxxxxx"
GOBLIN_PLAYER_SECRET = "<Secret>"
DISCORD_BOT_TOKEN = "Put your Bot Token Here"

Make sure to fill these in with the proper values.
