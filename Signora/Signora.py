#############################################################
import datetime, time, urllib.parse, re, asyncio, json, pytz, math
import discord
import traceback
import praw
import aiocron
from dotenv import load_dotenv
from discord.ext import commands, tasks
from pytz import timezone

bot = commands.Bot(command_prefix='x/')
bot.remove_command('help')

calls = 0

class Signora(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.time.start()
#########################
# SIGNORA BOT SHENNANIGANS #
#########################
#-----------------------------------------------

  # My Time
  def time_to_reset(self, tz):
    now = datetime.datetime.now(timezone('UTC'))
    '''print ("Current date and time : ")
    print (now.strftime("%Y-%m-%d %H:%M:%S"))'''


    now = now.astimezone(timezone(tz))
    reset_time = datetime.time(4, 0, 0)

  #——extract hours and minutes
    check_time = now.hour
  #——if else statement whether or not to add 1 or not
    combine = datetime.datetime.combine(now.date(), reset_time)
    
    tz_obj = timezone(tz)
    reset = tz_obj.localize(combine) 

    diff = reset - now

  #——.seconds strips only the hour/min/seconds in seconds. It discards the days from timedelta
    hrs = math.floor(diff.seconds/3600)
    mins = round((diff.seconds%3600)/60)

  #——weekly reset starts here
    days = 6 - now.weekday()
    if now.hour == 24 or now.hour < 4:
      print('this is right')
      days += 1
    if days == 7:
      days = 0
    return days, hrs, mins

#-----------------------------------------------

  @commands.command(name='console')
  async def console(self, ctx):
    pass

  @tasks.loop(minutes=1)
  async def time(self):

    now = datetime.datetime.now(timezone('UTC'))
    #print ("Current date and time : ")
    #print (now.strftime("%Y-%m-%d %I:%S %p"))

    # Convert to NA
    now_na = now.astimezone(timezone('Etc/GMT+5'))
    day_na, hr_na, min_na = self.time_to_reset('Etc/GMT+5')

    # Convert to EU
    now_eu = now.astimezone(timezone('Etc/GMT-1'))
    day_eu, hr_eu, min_eu = self.time_to_reset('Etc/GMT-1')

    # Convert to ASIA
    now_asia = now.astimezone(timezone('Etc/GMT-8'))
    day_asia, hr_asia, min_asia = self.time_to_reset('Etc/GMT-8')

    # Convert to TW/HK/MO
    now_thm = now.astimezone(timezone('Etc/GMT-8'))

    embed = discord.Embed(title="Server Status", colour=discord.Colour(0xcbffff), description=f'__**Server Time**__:\
    \n```md\n# NA {now_na.strftime("%I:%M %p")}\n```\
    • Daily reset in {hr_na} hours and {min_na} minutes!\
    \n• Weekly reset in {day_na} days, {hr_na} hours and {min_na} minutes\
    \n```# EU {now_eu.strftime("%I:%M %p")}\n```\
    • Daily reset in {hr_eu} hours and {min_eu} minutes!\
    \n• Weekly reset in {day_eu} days, {hr_eu} hours and {min_eu} minutes\
    \n```glsl\n# ASIA {now_asia.strftime("%I:%M %p")}\n```\
    • Daily reset in {hr_asia} hours and {min_asia} minutes!\
    \n• Weekly reset in {day_asia} days, {hr_asia} hours and {min_asia} minutes\
    \n```fix\n# TW/HK/MO {now_thm.strftime("%I:%M %p")}\n```\
    • Daily reset in {hr_asia} hours and {min_asia} minutes!\
    \n• Weekly reset in {day_asia} days, {hr_asia} hours and {min_asia} minutes ')

    embed.set_image(url='https://i.ibb.co/Tt0pZmy/kek.gif')

    '''await ctx.send(f'**ASIA** : ')
    await ctx.send(now_asia.strftime("%Y-%m-%d %H:%M:%S"))

    await ctx.send(f'**TW/HK/MO** : ')
    await ctx.send(now_thm.strftime("%Y-%m-%d %H:%M:%S"))'''
    try:
      channel = await self.bot.fetch_channel(self.bot.config["reset_channel"])
    except discord.errors.HTTPException:
      print("reset channel not set")
    else:
      channel_messages = await channel.history(limit=100).flatten()
      if len(channel_messages) == 0:
        await ctx.send(embed=embed)
      else:
        await channel_messages[-1].edit(content="", embed=embed)

  @commands.command(name='purge')
  @commands.is_owner()
  async def purge(self, ctx):
    deleted = await ctx.channel.purge(limit=100, check=None)
    await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))


  @commands.command(name='rconfig')
  async def rconfig(self, ctx, channelID):

    self.bot.config["reset_channel"] = channelID
    await self.bot.config.update()

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
####################################################################
def setup(bot):
  bot.add_cog(Signora(bot))
