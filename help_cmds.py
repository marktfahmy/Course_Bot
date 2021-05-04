import discord
from discord.ext import commands

class HelpCommands(commands.Cog):
     def __init__(self, bot):
          self.bot = bot

     @commands.command()
     async def invite(self, ctx):
          await ctx.send("You can invite me to your server with this link: <https://discord.com/oauth2/authorize?client_id=830674437723914280&scope=bot>")
          print(f"{ctx.author.name} ran command {ctx.message.content} in {ctx.guild.name}")
