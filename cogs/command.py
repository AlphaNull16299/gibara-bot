# -*- coding: utf-8 -*-
import traceback
import ast
import asyncio
import random
import datetime
import re
import aiohttp
import json
import discord
import datetime

from discord.ext import commands, tasks
from discord import  Embed, utils, User, File, Attachment

class command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
                           
    @commands.command()
    async def test(self, ctx):
        await ctx.send('OK')
        
        
    @commands.command()
    async def now(self, ctx):
        now = datetime.datetime.now()
        await ctx.send(now)

    @commands.command()
    async def new(self, ctx):
        await ctx.send('┏━━┓┏━━┓┏━━┓ ┏┓ \n┗━┓┃┃┏┓┃┗━┓┃ ┃┃\n┏━┛┃┃┃┃┃┏━┛┃ ┃┃\n┃┏━┛┃┃┃┃┃┏━┛ ┃┃ \n┃┗━┓┃┗┛┃┃┗━┓ ┃┃ \n┗━━┛┗━━┛┗━━┛ ┗┛')

    @commands.command()
    async def code(self, ctx):
        embed = discord.Embed(title="オープンソースなのでここでコードを見れます",description="本当は自分用と言うことは秘密",color=0xe67e22)
p        embed.add_field(name="Github",value="https://github.com/AlphaNull16299/gibara-bot")
        embed.add_field(name="Heroku(自分用)",value="https://dashboard.heroku.com/apps/newgibarabot/logs")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="prefixはa‌)です！",description="勉強になったね〜",color=0xe67e22)
        embed.add_field(name="help",value="コマンド一覧です。このコマンド。")
        embed.add_field(name="code",value="このbotはオープンソースらしい。")
        embed.add_field(name="update",value="このBotの最新情報が見れます！")
        embed.add_field(name="test",value="OKと帰ってくるだけ。開発時の起動確認？")
        embed.add_field(name="ping",value="pingを見れるらしい。")
        embed.add_field(name="say*",value="好きなことを言わせれます。")
        embed.add_field(name="dm*",value="好きな人にdmを送りつけれる。ただ送られたの見れないから一方通行。")
        embed.add_field(name="eval*",value="実験用。言うまでもないね！")
        embed.add_field(name="kick*",value="指定したuserをkickできますか？")
        embed.add_field(name="ban*",value="指定したuserをbanできますか？")
        embed.add_field(name="注意事項！",value="*が付いてるやつはBotOwnerしか実行できません！")
        await ctx.send(embed=embed)
       
    @commands.command()
    async def update(self, ctx):
        embed = discord.Embed(title="最新のアップデート情報",description="Version 2.1.3",color=0xff0000)
        embed.add_field(name="詳細情報",value="nowコマンドを追加しました。ただし、UTCです。各自+5してください")
        await ctx.send(embed=embed)


    @commands.command()
    async def ping(self, ctx):
        ping = '平均速度：{0}ms'.format(round(bot.latency * 1000))
        embed = discord.Embed(title="Nuro光が欲しいいいいいい",description=ping,color=0xffff00)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def kick(self, ctx, user: User = None):
        await ctx.guild.kick(user)
        embed = Embed(title="対象userをkickしました。", color=0xff1000)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="対象", value=user.name, inline=False)
        embed.add_field(name="実行", value=ctx.author.name, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def ban(self, ctx, user: User = None):
        await ctx.guild.ban(user)
        embed = Embed(title="対象userをbanしました。", color=0xff0000)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="対象", value=user.name, inline=False)
        embed.add_field(name="実行", value=ctx.author.name, inline=False)
        await ctx.send(embed=embed)

   
        
    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, *, text):
        await ctx.send(text)
        
    @commands.command(name="ev")
    @commands.is_owner()
    async def eval_(self, ctx, *, cmd):
        def get_role(name):
            return utils.get(ctx.guild.roles, name=name)

        def get_channel(name):
            return utils.get(ctx.guild.channels, name=name)

        def get_member(name):
            return utils.get(ctx.guild.members, name=name)

        try:
            fn_name = "_eval_expr"
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            env = {
                'bot': ctx.bot,
                'discord': discord,
                'asyncio': asyncio, 'random': random, 'datetime': datetime,
                're': re, 'aiohttp': aiohttp, 'json': json,
                'commands': commands, 'tasks': tasks,
                'get_role': get_role, 'get_channel': get_channel, 'get_member': get_member,
                'ctx': ctx,
                '__import__': __import__
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))
            await ctx.message.add_reaction("👍")
            if result is not None:
                if isinstance(result, Embed):
                    await ctx.send(embed=result)
                elif isinstance(result, File):
                    await ctx.send(file=result)
                elif isinstance(result, Attachment):
                    await ctx.send(file=await result.to_file())
                else:
                    await ctx.send(result)
        except:
            embed = Embed(color=0xFFFF00)
            embed.add_field(name="エラってやんのｗｗｗにわかかお前？ｗｗｗ", value="```py\n{}```".format(traceback.format_exc()[:1024:]), inline=False)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction("🖕")

    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, user: User, *, message):
        await user.send(message)
        await ctx.message.add_reaction("✅")
           

            

 
def setup(bot):
    bot.add_cog(command(bot))
