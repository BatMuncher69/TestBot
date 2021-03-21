import discord
import os
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from discord.utils import get
from itertools import cycle
from random import choice
import random
import json
import requests
import youtube_dl
import shutil



DEFAULT_PREFIX = "."
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    try:
        prefix = prefixes[str(message.guild.id)]
        return prefix
    except KeyError:
        return DEFAULT_PREFIX


client = commands.Bot(command_prefix=get_prefix, intents=intents, help=help)
client.remove_command("help")
status = cycle(['Halo', 'with children', 'with Masterchiefs balls'])


@client.event
async def on_ready():
    change_status.start()
    await client.change_presence(status=discord.Status.online)
    print('Bot is ready.')


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command(name="changeprefix")
async def change_prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command.')


def admin(ctx):
    return ctx.author.id == 293019756263374850






@client.command()
@commands.check(admin)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.check(admin)
async def example(ctx):
    await ctx.send(f'Bonjour {ctx.author}')


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')


@tasks.loop(seconds=100)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
@commands.check(admin)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Successfully loaded cog {}".format(extension))


@client.command()
@commands.check(admin)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Successfully unloaded cog {}".format(extension))


@client.command()
@commands.check(admin)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Successfully reloaded cog {}".format(extension))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.command()
@commands.check(admin)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send("Successfully kicked {} for reason {}".format(member, reason))


@client.command()
@commands.check(admin)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send("Successfully banned {} for reason {}".format(member, reason))


@client.command()
@commands.check(admin)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return



# @client.event
# async def on_message(message):
#     if message.author != client.user and message.content.startswith(command_prefix):
#         if len(message.content.replace(command_prefix, '')) >= 1:
#             location = message.content.replace(command_prefix, '').lower()
#             url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'
#             try:
#                 data = parse_data(json.loads(requests.get(url).content)['main'])
#                 await message.channel.send(embed=weather_message(data, location))
#             except KeyError:
#                 await message.channel.send(embed=error_message(location))

@client.command()
async def minecraft(ctx, arg):
    r = requests.get('https://api.minehut.com/server/' + arg + '?byName=true')
    json_data = r.json()

    description = json_data["server"]["motd"]
    online = str(json_data["server"]["online"])
    playerCount = str(json_data["server"]["playerCount"])

    embed = discord.Embed(
        title=arg + " Server Info",
        description='Description: ' + description + '\nOnline: ' + online + '\nOnline Players: ' + playerCount,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url="https://i1.wp.com/www.craftycreations.net/wp-content/uploads/2019/08/Grass-Block-e1566147655539.png?fit=500%2C500&ssl=1")

    await ctx.send(embed=embed)

@client.command(aliases=['user','info'])
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title = member.name, description = member.mention , color = discord.Color.orange())
    embed.add_field(name = "ID", value= member.id, inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url= ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)




@client.command(aliases=['8ball'])  #calculating............... with8balls
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    await ctx.send(f'question: {question}\nAnswer: {random.choice(responses)} :8ball:')

# @client.command()
# async def game(ctx)
#     games = ['']


@client.command(name='hello', help='This command says hello', aliases=['hi','hey'])
async def hello(ctx):
    responses = ['Selam','Mingala ba','Nín hao', 'Zdravo', 'Nazdar', 'Hallo', 'Helo', 'Hei', 'Bonjour', 'Guten Tag', 'Shalóm',
    'Namasté', 'Hai', 'Buongiorno', 'Kónnichi wa','Namaste','Hallo','Salâm','Witajcie','Olá','Salut','Hej','Hola','Zdravo','Nazdar']
    await ctx.send(f'{random.choice(responses)}')


@client.command()
async def flagQuiz(ctx):
    flags = {
  "usa": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/220px-Flag_of_the_United_States.svg.png",
  "china": "https://images-ext-1.discordapp.net/external/OkuHe2vSzVRSBg2c7sFag1GLJEs6xPRo6T48dCyfZbQ/https/upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Flag_of_the_People%2527s_Republic_of_China.svg/1200px-Flag_of_the_People%2527s_Republic_of_China.svg.png?width=705&height=470",
}
    
    await ctx.send(flags)






@client.command()
async def shutdown(ctx):
    with open("./data/auth.json", "r") as auth:
        authorised_users = json.load(auth)

    for user in authorised_users:
        if ctx.author.id == int(user):
            print("triggered")
            if authorised_users[user] == "all" or authorised_users[user] == "shutdown":
                await ctx.send("Bot shutting down...")
                await ctx.bot.logout()
                await client.close()
            else:
                await ctx.send("You do not have permission 'shutdown' or 'all' required to shutdown the bot!")
                return
    await ctx.send("You do not have authorised permissions to use this command!")




@client.event
async def on_member_remove(member):
    print(f'{member} has fucked off.')


def start_check():
    import startup
    for item in dir(startup):
        executed = False
        item = getattr(startup, item)
        if callable(item):
            for function in startup.executed_functions:
                if item == function:
                    executed = True
            if not executed:
                item()


start_check()

with open("./data/token", "r") as token_file:
    token = token_file.read()

client.run(token)
