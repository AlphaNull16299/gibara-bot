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
        activity = discord.Game(name=f"{prefix}help | {len(self.guilds)}guilds", type=1)
        return await self.change_presence(status=discord.Status.do_not_disturb, activity=activity)

    @tasks.loop(seconds=1.0)
    async def wait_for_tao(self):
        if int(time) >= self.now_time + 10:
            await self.get_channel(c_id).send("起動か再起動しました")
            self.now_time = int(time)
            
    async def on_message(self, message):
        user_id = message.author.id
        if message.content.startswith(prefix):
            return await self.process_commands(message)

        if message.channel.id == c_id:
            if user_id == 695288604829941781 and message.embeds and f"{self.user.mention}さん...\nゲームにログインしてね！！\n[コマンドは::loginだよ！！]" == message.embeds[0].description:
                await asyncio.sleep(10)
                await message.channel.send("::login")
                await asyncio.sleep(10)
                await message.channel.send("::t")
                self.now_time = int(time)

            if user_id == 664790025040429057:
                await asyncio.sleep(1)
                await message.channel.send(message.content)
                await self.wait_for("message_edit", check=lambda b, a: a.channel.id == c_id and a.author.id == 695288604829941781)
                await asyncio.sleep(3)
                await message.channel.send("::t")
                self.now_time = int(time)



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
