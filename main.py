import discord
from stock_info import Data
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
        if message.content[:7] == ".stock ":
            stock = message.content[7:].upper()
            try:
                data = Data(stock)
                data.make_graph()
                info = data.update()
                file = discord.File("plot.png")
                embed = discord.Embed(title=f"{stock} Stock Prices", color=discord.Color.blue())
                embed.add_field(name="High", value="USD$" + str(round(info[0], 2)))
                embed.add_field(name="Low", value="USD$" + str(round(info[1], 2)))
                embed.add_field(name="Close", value="USD$" + str(round(info[2], 2)))
                if stock == "ARKK":
                    embed.add_field(name="% of $150.19 at close", value=str(round(info[2]/150.19*100,2)) + "%")
                embed.set_footer(text="Most Recently Updated " + info[3].strftime("%A %d, %Y"))
                embed.set_image(url="attachment://plot.png")
                await message.channel.send(embed=embed, file=file)
            except:
                await message.channel.send(f"Failed to retrieve stock data for {stock}")
            print(f"{message.author.name} ran command {message.content} in {message.guild.name}")
        elif message.content[:8] == ".course ":
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
