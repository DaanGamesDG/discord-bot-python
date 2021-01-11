import discord
import ast
import asyncio
from discord.ext import commands


class Developers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval", hidden=True, aliases=["e", "evaluate"], category="General")
    @commands.is_owner()
    async def _eval(self, ctx, *, code: str):
      fn_name = "_eval_expr"

      cmd = code.strip("` ")
      cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
      body = f"async def {fn_name}():\n{cmd}"

      parsed = ast.parse(body)
      body = parsed.body[0].body
      insert_returns(body)

      env = {
          "bot": self.bot,
          "client": self.bot,
          "discord": discord,
          "commands": commands,
          "ctx": ctx,
          "__import__": __import__
      }
      exec(compile(parsed, filename="<ast>", mode="exec"), env)

      result = (await eval(f"{fn_name}()", env))
      embed = discord.Embed(title=f"Evaluated code | {ctx.author.name}#{ctx.author.discriminator}", colour=ctx.author.colour)
      embed.add_field(name="• Input", value=f"```{code}```", inline=False)
      embed.add_field(name="• Output", value=f"```{result}```", inline=False)
      await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Developers(client))


def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)