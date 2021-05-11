#############################################################
import datetime, time, urllib.parse, re, asyncio, json
import discord
import traceback
import praw
import aiocron
from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(command_prefix='mu/')
bot.remove_command('help')

calls = 0

class Kimmu(commands.Cog):
  """Test Help Message?"""
  def __init__(self, bot):
    self.bot = bot
#############################################    


#########################
# XIAO BOT SHENNANIGANS #
#########################
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
####################################################################
def setup(bot):
  bot.add_cog(Kimmu(bot))
