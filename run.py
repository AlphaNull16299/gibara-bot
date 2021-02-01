import os
import traceback
import discord
import asyncio
from discord.ext import commands, tasks
from time import time

prefix = "a)"
token = os.environ['DISCORD_BOT_TOKEN']
c_id = 805349530023231498
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
        await self.get_channel(c_id).send("‌")
        activity = discord.Game(name=f"{prefix}help | {len(self.guilds)}guilds", type=3)
        return await self.change_presence(status=discord.Status.do_not_disturb, activity=activity)

    async def on_message(message):
        if message.channel.id != 717664672626507776:
            return
        elif message.author.id != 804270128048111657:
            return
            title = str(message.embeds[0].title)
        elif "待ち構えている" in title:
            await asyncio.sleep(1)
            await bot.get_channel(717664672626507776).send("::attack")
        await bot.process_commands(message)  
    
    @tasks.loop(seconds=1.0)
    async def wait_for_tao(self):
        if int(time()) >= self.now_time + 10:
            await self.get_channel(c_id).send("‌")
            self.now_time = int(time())
        
if __name__ == '__main__':
    main_task = loop.create_task(run())
    loop.run_until_complete(main_task)
    loop.close()
