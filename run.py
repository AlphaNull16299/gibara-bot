import os
import traceback
import discord
import asyncio
from discord.ext import commands, tasks
from time import time

prefix = "a)"
token = os.environ['DISCORD_BOT_TOKEN']
c_id = 0
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
        self.now_time = int(time())
        
        
    async def on_ready(self):
        print("起動に成功しました。正常に起動していれば正常に起動します(？)")
        print("------")
        self.wait_for_tao.start()
        ch = self.get_channel(c_id)
        if ch:
            await ch.send("::t <@548058577848238080>")
        activity = discord.Game(name="a)help | Version2.1.", type=3)
        for cog in ["command","tao"]:
            self.load_extension(f"cogs.{cog}")
        return await self.change_presence(status=discord.Status.do_not_disturb, activity=activity)
   


    @tasks.loop(seconds=1.0)
    async def wait_for_tao(self):
        if int(time()) >= self.now_time + 10:
            ch = self.get_channel(c_id)
            if ch:
                await ch.send("::t")
                self.now_time = int(time())
            
    async def on_message(self, message):
        user_id = message.author.id
        if message.content.startswith(prefix):
            return await self.process_commands(message)

        if message.channel.id == c_id:
            if user_id == 695288604829941781 and message.embeds and f"{self.user.mention}さん...\nゲームにログインしてね！！\n[コマンドは::loginだよ！！]" == message.embeds[0].description:
                await asyncio.sleep(7)
                await message.channel.send("::login")
                await asyncio.sleep(7)
                await message.channel.send("::t")
                self.now_time = int(time())

            if user_id == 767728918991732736:
                await asyncio.sleep(1)
                await message.channel.send(message.content)
                await self.wait_for("message_edit", check=lambda b, a: a.channel.id == c_id and a.author.id == 695288604829941781)
                await asyncio.sleep(3)
                await message.channel.send("::t")
                self.now_time = int(time())
                
   
    async def on_command_error(self, ctx, error):
        await ctx.send("오류가 발생했습니다. 자신의 권한을 확인하고 그래도 해결되지 않으면 Alpha Null # 5000로 연락하십시오.")

    async def tao_atk(self):
        await self.wait_until_ready()
        tao = self.get_cog("TAO")
        if tao:
            ch = self.get_channel(tao.channel)
            await ch.send("::attack ")

if __name__ == '__main__':
    main_task = loop.create_task(run())
    loop.run_until_complete(main_task)
    loop.close()
