import discord
from discord.ext import commands
from arxiv import ArXivFinder
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()


GUILD_ID = discord.Object(id = os.getenv("ID"))

class Bot(commands.Bot):
    async def on_ready(self):
        report = ("Logged in as %s") % (self.user)
        print(report)
        try: 
            synced = await self.tree.sync(guild = GUILD_ID)
            print(f"Synced {len(synced)} commands to guild {GUILD_ID.id}")
        except Exception as e: 
            print(f'Error syncing command(s): {e}')

    async def on_message(self, message: discord.Message):
        if message.author == self.user: 
            return 
        
        if message.content.startswith('hello'):
            report = ("Hi there %s") % (message.author)
            await message.channel.send(report)

intents = discord.Intents.default()
intents.message_content = True 
client = Bot(command_prefix="!", intents = intents)

@client.tree.command(name="hello", description="Say hello", guild = GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")

@client.tree.command(name="find", description="Goes through the arXiv website and finds the paper corresponding to the search query", guild = GUILD_ID)
async def printer(interaction: discord.Interaction, query: str, max_results: int):
    arxiv = ArXivFinder()
    results = arxiv.fetch_query(query, max_results)
    print(results)
    
    embeds = []
    for item in results: 
        embed = discord.Embed(title = item['title'], url = item['link'], color = discord.Color.red())
        embed.add_field(name = 'Authors', value = item['authors'])
        embed.add_field(name = 'Date of Publication', value = item['published'])
        embeds.append(embed)

    if embeds: 
        await interaction.response.send_message(embeds = embeds)
    else: 
        await interaction.response.send_message("No papers found")
   
client.run(os.getenv("TOKEN"))