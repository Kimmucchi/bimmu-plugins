import os, re, json, asyncio, traceback, datetime, math, pytz
import discord
from pytz import timezone
from discord.ext import commands, tasks


TOKEN = "ODQ5NTEzOTkxMDc1MTM1NDg5.YLcRjg.DlYjTjxwPmKbSguUSemyAh1JxhE"

bot = commands.Bot(command_prefix='a/')
bot.remove_command('help')

#-----------------------------------------------

@bot.event
async def on_message(ctx):
  kimmu = ctx.content.lower()
  if "sweet dreams" in kimmu:
    await ctx.channel.send("https://cdn.discordapp.com/attachments/840432139304304704/854839383919034368/image0.png")

bot.load_extension("Venti.Venti")
#-----------------------------------------------

bot.run(TOKEN)