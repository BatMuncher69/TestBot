import discord
import os
from discord.ext import commands, tasks
from itertools import cycle
import random
import json
import youtube_dl
import requests

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
async def clear(ctx, amount: int):
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


# @client.command()
# async def play(ctx, url: str):
#     song_there = os.path.isfile("song.mp3")
#     try:
#         if song_there:
#             os.remove("song.mp3")
#     except PermissionError:
#         await ctx.send("Wait for the current playing music to end or use the 'stop' command")
#         return

#     voice_channel = discord.utils.get(ctx.guild.voice_channels, name='Shpek')
#     await voice_channel.connect()
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
#     for file in os.listdir("./"):
#         if file.endswith(".mp3"):
#             os.rename(file, "song.mp3")
#     voice.play(discord.FFmpegPCMAudio("song.mp3"))


# @client.command()
# async def leave(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     if voice.is_connected():
#         await voice.disconnect()
#     else:
#         await ctx.send("The bot is not connected to a voice channel.")


# @client.command()
# async def pause(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     if voice.is_playing():
#         voice.pause()
#     else:
#         await ctx.send("Currently no audio is playing.")


# @client.command()
# async def resume(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     if voice.is_paused():
#         voice.resume()
#     else:
#         await ctx.send("The audio is not paused.")


# @client.command()
# async def stop(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     voice.stop()


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
async def on_member_join(member):
    print(f'{member} has joined a server')


@client.event
async def on_member_remove(member):
    print(f'{member} has fucked off.')


def start_check():
    import startup
    for item in dir(startup):
        item = getattr(startup, item)
        if callable(item):
            item()


start_check()

with open("./data/token", "r") as token_file:
    token = token_file.read()

client.run(token)
