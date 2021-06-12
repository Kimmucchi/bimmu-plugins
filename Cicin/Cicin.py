#############################################################
import datetime, time, urllib.parse, re, asyncio, json, pytz, math, random
import discord
import traceback
import praw
import aiocron
from dotenv import load_dotenv
from discord.ext import commands, tasks
from pytz import timezone
from random import randrange

bot = commands.Bot(command_prefix='x/')
bot.remove_command('help')

calls = 0

class Cicin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
#########################
# SIGNORA BOT SHENNANIGANS #
#########################
#-----------------------------------------------
  @commands.command(name='say')
  async def say(self, ctx, channel_mention=None):
  #DEFINE VARIABLES
    img_url = None
    thumbnail_url = None
    footer = None
    valid_selections = [1,2]
  #USER INPUT
    try:
        #CHECK IF MESSAGE SENT IF FROM THE PERSON WHO REQUESTED THE COMMAND
        def check(m):
          return m.author.id == ctx.author.id
        embed = discord.Embed(title="Watchu wanna say?")
        msg1 = await ctx.send(embed=embed)
        response = await self.bot.wait_for("message", timeout=120, check=check)
        message = response.content
        print("message: ", message)
    except asyncio.TimeoutError:
        embed = discord.Embed(colour=discord.Colour(0x60cfb7), description=f"User inactive, command is terminated.")
        #await msg1.edit(embed=embed)
        return    
    except:
        traceback.print_exc()
        app_info = await self.bot.application_info()
        await ctx.send(f'⛔ Something went wrong, try again or ask {app_info.owner.mention} for help!')
    #CUSTOM CHANNEL ASSIGNED?
    channel = discord.utils.get(ctx.guild.channels, mention=channel_mention)
    if channel is None:
        await ctx.send(message)
    elif channel is not None:
        await channel.send(message)

#-----------------------------------------------
  @commands.command(name="bloo")
  async def bloo(self, ctx):

    random = randrange(0,2)
    bloo = ["https://cdn.discordapp.com/attachments/840432140516720676/853341461435908116/IMG_20210511_130204.jpg",
    "https://cdn.discordapp.com/attachments/840432140516720676/853341617990008842/IMG_20210518_140429.jpg",
    "https://cdn.discordapp.com/attachments/840432140516720676/853390201597591602/IMG_20210608_133704.jpg"]

    await ctx.send(bloo[random])


####################################################################
def setup(bot):
  bot.add_cog(Cicin(bot))
