import discord
from arkk_info import Data


client = discord.Client()
data = Data()


with open('credentials.txt', 'r') as f:
    TOKEN = f.read()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.guild.id == 709810612296876046:
        if message.content == ".arkk":
            data.make_graph()
            info = data.update()
            file = discord.File("plot.png")
            embed = discord.Embed(title="ARKK Stock Prices", color=discord.Color.blue())
            embed.set_thumbnail(url="https://i.imgur.com/MirvZiJ.png")
            embed.add_field(name="High", value="USD$" + str(round(info[0], 2)))
            embed.add_field(name="Low", value="USD$" + str(round(info[1], 2)))
            embed.add_field(name="Close", value="USD$" + str(round(info[2], 2)))
            embed.add_field(name="% of $150.19 at close", value=str(round(info[2]/150.19*100,2)) + "%")
            embed.set_footer(text="Most Recently Updated " + info[3].strftime("%A %d, %Y"))
            embed.set_image(url="attachment://plot.png")
            await message.channel.send(embed=embed, file=file)


client.run(TOKEN)
