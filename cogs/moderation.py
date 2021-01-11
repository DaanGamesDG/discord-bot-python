import discord
import asyncio
import datetime
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(category="Moderation")
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason: str = "no reason given"):
      if user.id == ctx.author.id:
        return await ctx.send(">>> 🤷‍♂️ | Why do you want to kick yourself?")
      if user.id == ctx.me.id:
        return await ctx.send(">>> 😢 | I am doing a lot of hard work for you and you still want to kick me?")
      if user.id == ctx.guild.owner_id:
        return await ctx.send(">>> 👑 | Sorry, you can not kick the owner from their own server!")
      if user.roles[len(user.roles) - 1].position >= ctx.author.roles[len(ctx.author.roles) - 1].position:
        return await ctx.send(">>> 🛑 | You cannot kick this user due to role hierarchy.")
      if user.roles[len(user.roles) - 1].position >= ctx.me.roles[len(ctx.me.roles) - 1].position:
        return await ctx.send(">>> 🛑 | I cannot kick this user due to role hierarchy.")

      dmed = True
      try:
        await user.send(content=f">>> 👢 | **Kicked - {ctx.guild}**\n> 📃 | Reason: **${reason}**")
      except:
        dmed = False
      
      await user.kick(reason=reason)
      if dmed:
        response = f">>> 👢 | Successfully kicked **{user.name}#{user.discriminator}**, reason: `{reason}`."
      else:
        response = f">>> 👢 | Successfully kicked **{user.name}#{user.discriminator}**, reason: `{reason}`.\nℹ | I was unable to DM this user."
      await ctx.send(response)

def setup(client):
    client.add_cog(Moderation(client))

