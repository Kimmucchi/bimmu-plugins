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

bot = commands.Bot(command_prefix='v/')
bot.remove_command('help')

calls = 0

class Venti(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
#########################
# SIGNORA BOT SHENNANIGANS #
#########################
#-----------------------------------------------
  @commands.command(name='say')
  #@checks.has_permissions(PermissionLevel.MODERATOR)
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
  @commands.command(name="lluna")
  async def lluna(self, ctx):

    random = randrange(0,7)
    Lluna = ["https://cdn.discordapp.com/attachments/840432140516720676/853416477062594590/IMG-20180518-WA0030.jpg",
    "https://cdn.discordapp.com/attachments/840432140516720676/853416754896961596/20201111_232601.jpg",
    "https://cdn.discordapp.com/attachments/840432140516720676/853416922736230430/IMG-20190824-WA0012.jpg",
    "https://cdn.discordapp.com/attachments/840432140516720676/853416923245182996/IMG-20200717-WA0005.jpg",
    "https://cdn.discordapp.com/attachments/840432140516720676/853416923575353354/IMG-20180708-WA0183.jpg",
    "https://cdn.discordapp.com/attachments/840432140516720676/853416924091383808/20201111_232600.jpg",
    "https://cdn.discordapp.com/attachments/840432140516720676/853416924482371594/20201124_010711.jpg"]

    await ctx.send(Lluna[random])

#-----------------------------------------------
#SMOL KIK
  @commands.command(name="bully")
  async def bully(self, ctx):
    bully = "https://media.discordapp.net/attachments/851930576520871997/854074818843508776/smolkik.gif"
    msg = ctx.message
    await msg.delete()
    await ctx.send(bully)

#-----------------------------------------------
#PLEASE
  @commands.command(name="please")
  async def please(self, ctx):
    please = "https://i.ibb.co/tQL1xc3/please.gif"
    msg = ctx.message
    await msg.delete()
    await ctx.send(please)
#-----------------------------------------------
#SURPRISED
  @commands.command(name='surprised')
  async def surprised(self, ctx):
    surprised = "https://i.ibb.co/f0j5SVL/surprised.gif"
    msg = ctx.message
    await msg.delete()
    await ctx.send(surprised)
#-----------------------------------------------
#GUN
  @commands.command(name='gun')
  async def gun(self, ctx):
    images = ["https://cdn.discordapp.com/emojis/804245164721176606.png?v=1",
    "https://cdn.discordapp.com/emojis/804246915834445875.png?v=1",
    "https://cdn.discordapp.com/emojis/804248719535898624.png?v=1"]
    random = randrange(0,3)
    msg = ctx.message
    await msg.delete()
    await ctx.send(images[random])
#-----------------------------------------------
#KISS
  @commands.command(name='kiss')
  async def kiss(self, ctx):
    images = ["https://cdn.discordapp.com/emojis/816686446269693992.png?v=1",
    "https://cdn.discordapp.com/emojis/824900569709674496.png?v=1"]
    random = randrange(0,2)
    msg = ctx.message
    await msg.delete()
    await ctx.send(images[random])
#-----------------------------------------------
#WHY
  @commands.command(name='why')
  async def why(self, ctx):
    image = "https://cdn.discordapp.com/emojis/812939539450429471.png?v=1"
    msg = ctx.message
    await msg.delete()
    await ctx.send(image)
#-----------------------------------------------
#DRINK
  @commands.command(name='drink')
  async def drink(self, ctx):
    embed = discord.Embed(title="I drink to forget,", colour=discord.Colour(0x8f097), description="...*but I always remember*.")
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/788031208020770826.png?v=1")
    msg = ctx.message
    await msg.delete()
    await ctx.send(embed=embed)
#-----------------------------------------------
#COMMANDS
  @commands.command(name='venti')
  async def venti(self, ctx):
    embed = discord.Embed(title="Venti's Commands", colour=discord.Colour(0x4ccc6b), description="`v/bully` — *Make Signora proud!*\n`v/drink` — *I drink to forget, but I always remember.*\n`v/gun` — *Bang bang!*\n`v/kiss` — *Mwah~*\n`v/lluna` — *Yoli's beautiful cat.*\n`v/please` — *Pretty please~?*\n`v/surprised` — *O:?*\n`v/why` — *WHY?*")
    embed.set_footer(text="For Server Members")
    await ctx.channel.send(embed=embed)
  
  @commands.command(name='ventimod')
  async def ventimod(self, ctx):
    embed = discord.Embed(title="Venti's Commands", colour=discord.Colour(0x4ccc6b), description="`v/embed` — *Make simple embeds on the fly.*\n`v/say` — *Speak as me!*\n`v/rr` — *Add react roles.*")
    embed.set_footer(text="For Moderators")

    await ctx.channel.send(embed=embed)

#-----------------------------------------------

####################################################################
def setup(bot):
  bot.add_cog(Venti(bot))
