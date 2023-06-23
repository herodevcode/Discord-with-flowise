import os
import discord
import requests
from discord import app_commands

API_URL = os.environ["URL"]
headers = {"Authorization": os.environ["API_KEY"]}
my_secret = os.environ['DISCORD_BOT_SECRET']


class CustomClient(discord.Client):

  def __init__(self, *, intents: discord.Intents):
    super().__init__(intents=intents)
    self.tree = app_commands.CommandTree(self)

  async def setup_hook(self):
    await self.tree.sync()


client = CustomClient(intents=discord.Intents.all())


def query(payload):
  try:
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
  except Exception as e:
    return {"error": str(e)}


@client.event
async def on_ready():
  print("I'm in")
  print(client.user)


@client.tree.command(name="flowise", description="Ask a question to Flowise")
async def flowise(interaction: discord.Interaction, question: str):
  await interaction.response.defer()
  output = query({"question": question})
  await interaction.followup.send(output)


client.run(my_secret)
