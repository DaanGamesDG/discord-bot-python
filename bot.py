import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = commands.Bot(command_prefix="-", help_command=None)

# functions
for i in os.listdir("./cogs"):
    if i.endswith(".py"):
        client.load_extension(f"cogs.{i[:-3]}")

def Map(keys, args: int = 0):
    arr = []
    for k in keys:
        arr.append(k)
    return arr[args:]

# client part
@client.event
async def on_ready():
    client.logs = await client.fetch_channel(os.getenv("LOGS_CHANNEL"))
    print(f'We have logged in as {client.user}')
    
    for id in [304986851310043136, 679240313952403457]:
        client.owner_ids.add(id)

@client.event
async def on_message(message):
    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    if ctx.command is not None:
        response = ""
        if isinstance(error, commands.MissingRequiredArgument):
            arguments = ", ".join(Map(ctx.command.clean_params.keys(), len(ctx.args[2:])))
            response = f">>> 📋 | Sorry, you are missing 1 or more required arguments: `{arguments}`!"
        elif isinstance(error, commands.MissingPermissions):
            missing = ", ".join(Map(error.missing_perms)).replace("_", " ")
            response = f">>> 👮‍♂️ | Oops, you are missing `{missing}` permissions to continue."
        elif isinstance(error, commands.BotMissingPermissions):
            missing = ", ".join(Map(error.missing_perms)).replace("_", " ")
            response = f">>> 👮‍♂️ | Oops, I am missing `{missing}` permissions to continue."
        elif isinstance(error, commands.MemberNotFound):
            response = f">>> 🔎 | Sorry I was unable to find a user with this information: \"{error.argument}\"."
        elif isinstance(error, commands.RoleNotFound):
            response = f">>> 🔎 | Oops, I was unable to find a role with this information: \"{error.argument}\"."
        elif isinstance(error, commands.NotOwner):
            response = ">>> 🖥 | Sorry, this command is only available for developers of this bot!"
        else:
            response = f">>> ❗ | Uhm, we ran into an error. I am reporting this right now, sorry for the inconvience. Error: `{error}`"
            description = f"```{error}```"
            value=f">>> 🏷 | Guild: **{ctx.guild}** / `{ctx.guild.id}`\n👤 | User: **{ctx.author}#{ctx.author.discriminator}** / `{ctx.author.id}`"
            embed = discord.Embed(title=f"We ran into an error - {ctx.command}", description=description, color=discord.Colour.from_rgb(75, 90, 198))
            embed.add_field(name="• Information", value=value)
            await client.logs.send(embed=embed)

        await ctx.send(response)

client.run(os.getenv("BOT_TOKEN"))