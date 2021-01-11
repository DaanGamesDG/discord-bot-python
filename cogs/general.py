import discord
import asyncio
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
      reply = await ctx.send(">>> 🏓 | Pinging...")
      await reply.edit(content=f">>> 🏓 | Pong! Latency: `{round(self.bot.latency * 1000)}ms`!")

    @commands.command()
    async def info(self, ctx, member: discord.Member=None):
        if member is None: member = ctx.author

        description = "\n".join([
            f">>> 👤 | **User**: {member.mention}",
            f"📟 | **User id**: `{member.id}`",
        ])
        embed = discord.Embed(title=f"Information about {member.name}#{member.discriminator}", description=description, color=member.color)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(General(client))

