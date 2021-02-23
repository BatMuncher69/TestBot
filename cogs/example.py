import discord
from discord.ext import commands

class Example(commands.Cog):

	def __init__(self, client):
		self.client = client

	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		print('Bot is online.')

	# Commands
	@commands.command()
	async def ping(self, ctx):
		await ctx.send('Pong')
		
		
	@commands.command(invoke_without_command=True)
	async def helpp(self, ctx):
		embed = discord.Embed(title = "Help", description = "use .help <command> for more info on a command.", color = ctx.author.color())
		embed.add_field(name = "moderation", value = "clear, kick, ban, whois")
		embed.add_field(name = "fun", value = "8ball" )
		embed.add_field(name = "random", value = "minecraft, hello")
		await ctx(embed=embed)



def setup(client):
	client.add_cog(Example(client))