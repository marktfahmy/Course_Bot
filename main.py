import discord
import json
from discord.ext import commands
from course_cmds import GetCourses
from help_cmds import HelpCommands

with open('credentials.txt', 'r') as f:
    TOKEN = f.read()

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

bot.add_cog(GetCourses(bot))
bot.add_cog(HelpCommands(bot))

bot.run(TOKEN)
