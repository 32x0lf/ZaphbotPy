import json
import os
import discord 
import random
import requests
import worker
import datetime
import time
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


bot = commands.Bot(command_prefix='!')
#client = discord.Client()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {guild.name} server!')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     brooklyn_99_quotes = [
#         'I\'m the human form of the 💯 emoji.',
#         'Bingpot!',
#         (
#             'Cool. Cool cool cool cool cool cool cool, '
#             'no doubt no doubt no doubt no doubt.'
#         ),
#     ]

#     if message.content == '99!':
#         response = random.choice(brooklyn_99_quotes)
#         await message.channel.send(response)


@bot.command(name='99', help='Resopnds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
         'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
   
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='slp',help='Get the slp')
async def request(ctx,strslp):
    ronin = strslp.split(':')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
    url='https://lunacia.skymavis.com/game-api/clients/0x'+ ronin[1] +'/items/1'
    response = requests.get(url,headers=headers)
    status = response.status_code
    #as_of = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(response.json()['last_claimed_item_at'])))
    #as_of = datetime.datetime.utcfromtimestamp((response.json()['last_claimed_item_at']).replace(tzinfo=datetime.timezone.utc))
    #as_of = time.strftime("%a, %d %b %Y %H:%M:%S +0800", time.ctime(int(response.json()['last_claimed_item_at'])))
    as_of = time.ctime(int(response.json()['last_claimed_item_at']))
    await ctx.send('Your total SLP is' + ' ' +str(response.json()['total']) + ' ' +'as of' +' '+ as_of )


# @has_permissions(manage_messages=True, read_message_history=True)
# @bot_has_permissions(manage_messages=True, read_message_history=True)
@bot.command(name='clear', help='Clear messages')
async def purge(ctx, limit: int = 100, user= None, *, matches: str = None):
    """Purge all messages, optionally from ``user``
    or contains ``matches``."""
    def check_msg(msg):
        if msg.id == ctx.message.id:
            return True
        if user is not None:
            if msg.author.id != user.id:
                return False
        if matches is not None:
            if matches not in msg.content:
                return False
        return True
    deleted = await ctx.channel.purge(limit=limit, check=check_msg)
    msg = await ctx.send(ctx, 'purge', len(deleted))
    await bot.sleep(2)
    await msg.delete()


##client = CustomClient()
bot.run(TOKEN)



# https://api.lunaciarover.com/stats/0xc151798ffca08c8c8f95e247949b5ff1941ad5ec
#https://lunacia.skymavis.com/game-api/clients/0x<RONIN>/items/1