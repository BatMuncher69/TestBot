import discord
import os
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from itertools import cycle
from random import choice
import random
import json
import requests
import youtube_dl
import asyncio





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


client = commands.Bot(command_prefix=get_prefix, intents=intents)
status = cycle(['Halo', 'with children'])


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


@client.command(aliases=['8ball'])
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
    await ctx.send(f'question: {question}\nAnswer: {random.choice(responses)}')


@client.command(name='hello', help='This command says hello', aliases=['hi','hey'])
async def hello(ctx):
    responses = ['Selam','Mingala ba','Nín hao', 'Zdravo', 'Nazdar', 'Hallo', 'Helo', 'Hei', 'Bonjour', 'Guten Tag', 'Shalóm',
    'Namasté', 'Hai', 'Buongiorno', 'Kónnichi wa','Namaste','Hallo','Salâm','Witajcie','Olá','Salut','Hej','Hola','Zdravo','Nazdar']
    await ctx.send(f'{random.choice(responses)}')



# youtube_dl.utils.bug_reports_message = lambda: ''

# ytdl_format_options = {
#     'format': 'bestaudio/best',
#     'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
#     'restrictfilenames': True,
#     'noplaylist': True,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
# }

# ffmpeg_options = {
#     'options': '-vn'
# }

# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)

#         self.data = data

#         self.title = data.get('title')
#         self.url = data.get('url')

#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]

#         filename = data['url'] if stream else ytdl.prepare_filename(data)
#         return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


# queue = []



# @client.command(name='die', help='This command returns a random last words')
# async def die(ctx):
#     responses = ['why have you brought my short life to an end', 'i could have done so much more', 'i have a family, kill them instead']
#     await ctx.send(choice(responses))



# @client.command(name='join', help='This command makes the bot join the voice channel')
# async def join(ctx):
#     if not ctx.message.author.voice:
#         await ctx.send("You are not connected to a voice channel")
#         return
    
#     else:
#         channel = ctx.message.author.voice.channel

#     await channel.connect()

# @client.command(name='queue', help='This command adds a song to the queue')
# async def queue_(ctx, url):
#     global queue

#     queue.append(url)
#     await ctx.send(f'`{url}` added to queue!')

# @client.command(name='remove', help='This command removes an item from the list')
# async def remove(ctx, number):
#     global queue

#     try:
#         del(queue[int(number)])
#         await ctx.send(f'Your queue is now `{queue}!`')
    
#     except:
#         await ctx.send('Your queue is either **empty** or the index is **out of range**')
        
# @client.command(name='play', help='This command plays songs')
# async def play(ctx):
#     global queue

#     server = ctx.message.guild
#     voice_channel = server.voice_client

#     async with ctx.typing():
#         player = await YTDLSource.from_url(queue[0], loop=client.loop)
#         voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

#     await ctx.send('**Now playing:** {}'.format(player.title))
#     del(queue[0])

# @client.command(name='pause', help='This command pauses the song')
# async def pause(ctx):
#     server = ctx.message.guild
#     voice_channel = server.voice_client

#     voice_channel.pause()

# @client.command(name='resume', help='This command resumes the song!')
# async def resume(ctx):
#     server = ctx.message.guild
#     voice_channel = server.voice_client

#     voice_channel.resume()

# @client.command(name='view', help='This command shows the queue')
# async def view(ctx):
#     await ctx.send(f'Your queue is now `{queue}!`')

# @client.command(name='leave', help='This command stops makes the bot leave the voice channel')
# async def leave(ctx):
#     voice_client = ctx.message.guild.voice_client
#     await voice_client.disconnect()

# @client.command(name='stop', help='This command stops the song!')
# async def stop(ctx):
#     server = ctx.message.guild
#     voice_channel = server.voice_client

#     voice_channel.stop()




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
