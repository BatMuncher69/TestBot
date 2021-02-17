import discord
import os
from discord.ext import commands
import random
import json


intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='.', intents=intents)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Bonjour'))
    print('Bot is ready.')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Successfully loaded cog {}".format(extension))


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Successfully unloaded cog {}".format(extension))


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Successfully reloaded cog {}".format(extension))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send("Successfully kicked {} for reason {}".format(member, reason))


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send("Successfully banned {} for reason {}".format(member, reason))


@client.command()
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
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


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

with open("./data/token", "r") as f:
    token = f.read()

client.run(token)
