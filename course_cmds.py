import discord
from course_finder import Course
from discord.ext import commands

course_finder = Course()

class GetCourses(commands.Cog):
     def __init__(self, bot):
          self.bot = bot

     @commands.command()
     async def course(self, ctx, dept, code):
          course_data = course_finder.find_course(dept+" "+code)
          if course_data == "Error":
               await ctx.send(f"Failed to retrieve course data for {course_code.upper()}")
          else:
               embed = discord.Embed(title=course_data[0], color=discord.Color.blue(), description=course_data[2]+'\n\n'+course_data[1]+"; "+course_data[3])
               if course_data[4]:
                    embed.add_field(name="Other Info", value=course_data[4])
               await ctx.send(embed=embed)
          print(f"{ctx.author.name} ran command {ctx.message.content} in {ctx.guild.name}")
