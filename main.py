import discord, random, pickle
from discord.ext import commands
# pip install -U git+https://github.com/Rapptz/discord.py.git

bot = commands.Bot(command_prefix="!")
token = "YOUR BOT TOKEN" # YOUR BOT TOKEN

@bot.event
async def on_message(msg):
    await bot.process_commands(msg)

len_range = lambda _list: range(len(_list))

@bot.command()
@commands.has_permissions(administrator=True)
async def backup(ctx):
    code = ""
    for i in range(20):
        code += str(random.randint(0,9))
        
    with open(f"backups/{code}.log", "wb") as file:
        mlist = [] # messages list
        async for i in ctx.channel.history(limit=100): # save 100 messages
            mlist.append(i)
        for i in reversed(mlist):
            pickle.dump({"author": str(i.author)[:-5], "avatar": i.author.avatar.url if i.author.avatar != None else None, "content": i.content, "embeds": [j.to_dict() for j in i.embeds]}, file)
        await ctx.send("Successfully backed up server")
        await ctx.send("Check DM and save load key")
        dmch = await ctx.author.create_dm()
        await dmch.send(f"Your load key: ||{code}||") # send load key to dm
                                                      # `||`: spoiler

@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, loadkey):
    with open(f"backups/{loadkey}.log", "rb") as file:
      webhook = await ctx.channel.create_webhook(name="Message load webhook") # new webhook
      while True:
        try:
         obj = pickle.load(file)
        except:
         break

        try:
            await webhook.send(content=obj["content"], username=obj["author"], avatar_url=obj["avatar"],
                               embeds=[discord.Embed.from_dict(i) for i in obj["embeds"]])
        except: # if message is empty
              await webhook.send(content="(empty message)", username=obj["author"], avatar_url=obj["avatar"], \
                                 embeds=[discord.Embed.from_dict(i) for i in obj["embeds"]])
      await webhook.delete()

bot.run(TOKEN)
