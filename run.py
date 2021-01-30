import os
import traceback
import discord
import asyncio
from discord.ext import commands, tasks
from time import time

prefix = "a)"
token = os.environ['DISCORD_BOT_TOKEN']
c_id = 776328743458832384
loop = asyncio.get_event_loop()



async def run():
    bot = MyBot()
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        await bot.logout()

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(prefix), loop=loop, case_insensitive=True, help_command=None)
        self.load_extension("cogs.command")
        self.now_time = int(time())
        
    async def on_ready(self):
        print("起動に成功しました")
        self.wait_for_tao.start()
        await self.get_channel(c_id).send("起動か再起動しました")
        activity = discord.Game(name=f"またがたちました | {prefix}help | {len(self.guilds)}guilds", type=1)
        return await self.change_presence(status=discord.Status.do_not_disturb, activity=activity)




    async def on_command_error(ctx,exception):
        if isinstance(exception,commands.CommandNotFound):
            await ctx.send("そのコマンドは存在しない")
        elif isinstance(exception,commands.MissingRequiredArgument):
            await ctx.send("引数が足りてない")
        else:
            await ctx.send("例外発生 | {}".format(exception))
if __name__ == '__main__':
    main_task = loop.create_task(run())
    loop.run_until_complete(main_task)
    loop.close()
