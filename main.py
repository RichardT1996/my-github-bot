import discord
import requests
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.reply('Missing permissions')

@bot.command()
async def ping(ctx):
    await ctx.reply('Luke is gay!')

@bot.command()
async def Hello(ctx):
    await ctx.reply('Hello!', mention_author=True)

@bot.command()
async def dm(ctx, member: discord.Member, *, message):
    await member.send(message)
    await ctx.send(f'Message sent to {member}')

@bot.command()
async def clear(ctx, amount=3):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked!')

@bot.command(case_insensitive=True)
async def urban(ctx, *, query: commands.clean_content):
    """Searches for an urban dictionary definition of your search."""
    api = 'http://api.urbandictionary.com/v0/define'

    response = requests.get(api, params=[("term", query)]).json()
    if len(response["list"]) == 0:
        return await ctx.send(f'Nothing found.', hidden=True)

    e = discord.Embed(
        title=query
    )
    if len(response['list'][0]['definition']) > 1024:
        definition = response['list'][0]['definition'][:1020] + '...'
    else:
        definition = response['list'][0]['definition']

    if len(response['list'][0]['example']) > 1024:
        example = response['list'][0]['example'][:1020] + '...'
    else:
        example = response['list'][0]['example']

    e.add_field(name='Top definition:', value=definition, inline=False)
    e.add_field(name='Example:', value=example, inline=False)
    await ctx.send("**Results matching your search:**", embed=e)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'Added {role} to {member}')

@bot.command()
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f'Removed {role} from {member}')



if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))
