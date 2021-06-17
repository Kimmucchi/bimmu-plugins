from .artifact import rate_artifact_jean as raDPS
#############################################################
import datetime, time, urllib.parse, re, asyncio, json
import discord
import traceback
import praw
import aiocron
from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(command_prefix='j/')
bot.remove_command('help')

calls = 0

class Jean(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
#######################################################################################################################################################
#               JEAN-AR             #
#######################################################################################################################################################
  @commands.command(name='rate')
  async def rate(self, ctx):

    if not ctx.message.attachments:
      return
    options = ctx.message.content.split()[1:]
    options = {opt_to_key[option.split('=')[0].lower()] : float(option.split('=')[1]) for option in options}
    if 'Char' in options.keys():
      # If character is included in options, use these fixed weights instead
      if options["Char"].lower() == "mona":
        if options.has_key("Role"):
          if options["Role"].lower() == "dps":
            pass
          elif options["Role"].lower() == "support":
            pass
          else:
            # Spit back error
            pass

        options["CritRate%"] = 1
        options["Energy Recharge%"] = 0.54
    url = ctx.message.attachments[0].url
    def check(m):
      return m.author.id == ctx.author.id
    response = ctx.message
    suc, text = await raDPS.ocr(url)
    global calls
    calls += 1
    print(f'Calls: {calls}')
    app_info = await self.bot.application_info()
    if suc:
      results = raDPS.parse(text)
      score, main_score, sub_score = raDPS.rate(results, options)
      embed = discord.Embed(color=0x60cfb7, title="JEAN | Artifact Rating", description=f'__**Gear Score**__: {score:.2f}% \n__**Main Stat**__: {main_score:.2f}%, \n__**Sub-Stats**__: {sub_score:.2f}%')
      embed.set_thumbnail(url="https://media.discordapp.net/attachments/830585878706520064/837879461059362816/Jean.png")
      embed.set_image(url=ctx.message.attachments[0].url)
      embed.set_footer(text=f'Powered by Teyvat Collective | Kimmu#0007', icon_url="https://i.ibb.co/hfbFt1z/pale-1.png")
    else:
      msg = f'OCR failed. Error: {text}'
      if 'Timed out' in text:
        msg += ', please try again in a few minutes'
    await response.delete()
    await ctx.send(ctx.author.mention)
    await ctx.send(embed=embed)
##################################################################################################################
#########################
# JEAN BOT SHENNANIGANS #
#########################
  @commands.command(name='say')
  @commands.has_role('TC')
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
        embed = discord.Embed(title="What would you like me to say?")
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
  ##########################################################################

  @commands.command()
  @commands.has_role('TC')
  async def embed(self, ctx, channel_mention=None):
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
          embed = discord.Embed(title="🔱 Please enter the embed values as requested!")
          msg1 = await ctx.send(embed=embed)
      #COLOR
          embed = discord.Embed(description="If you want a custom color for your embed, __please enter a hexadecimal value__.\
              \n**🔱 Otherwise, if you don't have one enter `0` and Kimmu's favorite color will be used by default.**")
          msg2 = await ctx.send(embed=embed)
          response = await self.bot.wait_for('message', timeout=30, check=check)
          user_hex = response.content
          if user_hex == "0":
              readableHex = 0x00CCDC
          else:
              try:
                  sixteenIntegerHex = int(user_hex, 16)
                  readableHex = int(hex(sixteenIntegerHex), 0)
              except:
                  embed = discord.Embed(color=16711683, title="⛔ You did not enter a valid __Hexadecimal__ value.", description="Please run the command again.")
                  await ctx.send(embed=embed)
                  return
      #TITLE
          embed = discord.Embed(title="Please enter the embed's title:")
          msg3 = await ctx.send(embed=embed)
          response = await self.bot.wait_for('message', timeout=30, check=check)
          title = response.content
      #DESCRIPTION
          embed = discord.Embed(title="Please enter the embed's description:")
          msg4 = await ctx.send(embed=embed)
          response = await self.bot.wait_for('message', timeout=300, check=check)
          description = response.content
          """for emoji in self.bot.emojis:
              emoji_text = f":{emoji.name}:"
              description = description.replace(emoji_text, emoji)"""
          #description = description.replace("\n", "\\n")
      #THUMBNAIL
          embed = discord.Embed(title="Would you like to add a thumbnail picture to your embed?",
              description="\n`1.` Yes\
              \n`2.` No")
          msg5 = await ctx.send(embed=embed)
          response = await self.bot.wait_for('message', timeout=30, check=check)
          try:
              yn_int1 = int(response.content)
          except:
              await ctx.send(color=16711683, title="⛔ You must select either 1 or 2! Please run the command again.")
          if yn_int1 in valid_selections:
              if yn_int1 == 1:
                  try:
                      embed = discord.Embed(title="Enter the thumbnail image URL:")
                      msg5 = await ctx.send(embed=embed)
                      response = await self.bot.wait_for("message", timeout=60, check=check)
                      thumbnail_url = response.content
                  except:
                      await ctx.send("Invalid URL. Please run the command again.")
          else:
              await ctx.send(color=16711683, title="⛔ You must select either 1 or 2! Please run the command again.")
      #IMAGE
          embed = discord.Embed(title="Would you like to add a large image to your embed?",
              description="\n`1.` Yes\
              \n`2.` No")
          msg6 = await ctx.send(embed=embed)
          response = await self.bot.wait_for('message', timeout=30, check=check)
          yn_int2 = int(response.content)
          if yn_int2 in valid_selections:
              if yn_int2 == 1:
                  try:
                      embed = discord.Embed(title="Enter the image URL:")
                      msg6 = await ctx.send(embed=embed)
                      response = await self.bot.wait_for("message", timeout=60, check=check)
                      img_url = response.content
                  except:
                      await ctx.send("Invalid URL. Please run the command again.")
          else:
              await ctx.send(color=16711683, title="⛔ You must select either 1 or 2! Please run the command again.")
      #FOOTER
          embed = discord.Embed(title="Would you like to add a footer to your embed?",
              description="\n`1.` Yes\
              \n`2.` No")
          msg7 = await ctx.send(embed=embed)
          response = await self.bot.wait_for('message', timeout=30, check=check)
          yn_int3 = int(response.content)
          if yn_int3 in valid_selections:
              if yn_int3 == 1:
                  embed = discord.Embed(title="Enter the footer:")
                  msg6 = await ctx.send(embed=embed)
                  response = await self.bot.wait_for("message", timeout=60, check=check)
                  footer = response.content
          else:
              await ctx.send("You must select either 1 or 2! Please run the command again.")
      except asyncio.TimeoutError:
          embed = discord.Embed(colour=discord.Colour(0x60cfb7), description=f"User inactive, command is terminated.")
          #await msg1.edit(embed=embed)
          return    
      except:
          traceback.print_exc()
          app_info = await self.bot.application_info()
          await ctx.send(f'⛔ Something went wrong, try again or ask {app_info.owner.mention} for help!')
      else:
  #DEFINE EMBED
          print("title: ", title)
          print("description: ", description)
          print("IMG: ", img_url)
          print("Thumb: ", thumbnail_url)
          print("Foot: ", footer)
          embed = discord.Embed(
              title=title, 
              colour=readableHex, 
              description=description)
          if img_url:
              embed.set_image(url=img_url)
          if thumbnail_url:
              embed.set_thumbnail(url=thumbnail_url)
          if footer:
              embed.set_footer(text=footer)
          #CUSTOM CHANNEL ASSIGNED?
          channel = discord.utils.get(ctx.guild.channels, mention=channel_mention)
          if channel is None:
              await ctx.send(embed=embed)
          elif channel is not None:
              await channel.send(embed=embed)
####################################################################
def setup(bot):
  bot.add_cog(Jean(bot))
