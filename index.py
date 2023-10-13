import interactions
from interactions import slash_command, slash_option, SlashContext, OptionType, SlashCommandChoice, AutocompleteContext, listen, Client
from requests.auth import HTTPBasicAuth
import requests
from interactions.ext.paginators import Paginator
from dotenv import load_dotenv
import os
import re

load_dotenv()

mode = "owner"

if mode == "owner":
    goblinAPIKey = os.getenv("GOBLIN_OWNER_API_KEY")
    goblinAPISecret = os.getenv("GOBLIN_OWNER_SECRET")
elif mode == "player":
    goblinAPIKey = os.getenv("GOBLIN_PLAYER_API_KEY")
    goblinAPISecret = os.getenv("GOBLIN_PLAYER_SECRET")



goblinCampaignID = os.getenv("GOBLIN_CAMPAIGN_ID")
goblinAPIEndpoint = f"https://www.the-goblin.net/api/pub/{goblinCampaignID}"

auth = HTTPBasicAuth(goblinAPIKey, goblinAPISecret)
response = requests.get(goblinAPIEndpoint , auth = auth)

campaign_data = response.json()

# Initialize an empty list to hold the flattened dictionaries
flattened_data = []

# Define the sections to be flattened and combined
sections_to_explore = ['locations', 'creatures', 'organisations', 'quests', 'things']

# Function to recursively extract items from all sections
def recurse_items(section, items):
    for item in items:
        # Create a new dictionary with only the required keys and an additional 'type' key to identify the section
        new_item = {
            'type': section,
            'id': item.get('id', None),
            'name': item.get('name', None),
            'blurb': item.get('blurb', None)
        }
        # Append the new dictionary to the flattened list
        flattened_data.append(new_item)
        
        # Recurse into nested sections if available
        if section in item and isinstance(item[section], list):
            recurse_items(section, item[section])

# Loop through each section and extract the relevant keys ('id', 'name', 'blurb')
for section in sections_to_explore:
    recurse_items(section, campaign_data[section])

all_entries = {f"{item['id']}": item for item in flattened_data}

def replace_aliases(text):
    pattern = re.compile(r'@\[(.*?)\]\((.*?)\)')
    def replacer(match):
        alias, entity_id = match.groups()
        if alias:
            return alias
        else:
            if entity_id in all_entries:
                return all_entries[entity_id]['name']
            else:
                return "Unknown Entity"
    return pattern.sub(replacer, text)

bot = interactions.Client()

@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

@listen()
async def on_message_create(event):
    print(f"message received: {event.message.content}")
    print(f"pulling data from campaign ID: {goblinCampaignID}")


@slash_command(name="gob_grab", description="Grab a page from your notebook.", scopes=[180061259050385408])
@slash_option(
    name="page_name",
    description="Page Name",
    required=True,
    opt_type=OptionType.STRING,
    autocomplete=True,
)
async def gob_grab_function(ctx: SlashContext, page_name: str):
    if page_name in all_entries:
        blurb = all_entries[page_name]['blurb']
        blurb = str.replace(blurb,'$[objectname]',all_entries[page_name]['name'])
        blurb = str.replace(blurb,'---','_ _')
        blurb = replace_aliases(blurb)
        paginator = Paginator.create_from_string(bot, blurb, page_size=1000)
    else:
        paginator = Paginator.create_from_string(bot, "Notebook Entry Not Found", page_size=1000)
    await paginator.send(ctx)

@gob_grab_function.autocomplete("page_name")
async def autocomplete(ctx: AutocompleteContext):
    choices = []
    text = ctx.input_text
    for entry in all_entries:
        if text.casefold() in all_entries[entry]['name'].casefold():
            if len(choices) <= 25:
                choices.append(SlashCommandChoice(all_entries[entry]['name'], all_entries[entry]['id']))
    await ctx.send(
        choices
    )

bot.start(os.getenv("DISCORD_BOT_TOKEN")) 