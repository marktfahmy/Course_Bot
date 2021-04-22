import discord
from course_finder import Course

client = discord.Client()
course = Course()

with open('credentials.txt', 'r') as f:
    TOKEN = f.read()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
        if message.content[:8] == ".course ":
            course_code = message.content[8:]
            course_data = course.find_course(course_code)
            if course_data == "Error":
                await message.channel.send(f"Failed to retrieve course data for {course_code.upper()}")
            else:
                embed = discord.Embed(title=course_data[0], color=discord.Color.blue(), description=course_data[2]+'\n\n'+course_data[1]+"; "+course_data[3])
                if course_data[4]:
                    embed.add_field(name="Other Info", value=course_data[4])
                await message.channel.send(embed=embed)
            print(f"{message.author.name} ran command {message.content} in {message.guild.name}")

client.run(TOKEN)
