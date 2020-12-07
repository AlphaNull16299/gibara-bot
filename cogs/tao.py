import discord
import asyncio
import re
from discord.ext import commands,tasks

class TAO(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.modes = ["::attack", "::i f "]
        self.mode = self.modes[0]
        self.channel = 711472768478085130

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.channel.id != self.channel:return
        if message.author.id != 695288604829941781:return
        ch = self.bot.get_channel(self.channel)
        send = ch.send
        embed = message.embeds[0] if message.embeds else None
        content = message.content
        if not embed:
            if content.startswith("```diff") and content.endswith("```"):
                if len(content.split("```")) in [5,7]:
                    line = content.split("```")[1] + "```"
                else:
                    line = content.splitlines()[-1]
                if f"- {self.bot.user}のHP:" in line:
                    await send(self.mode)
                if f"! {self.bot.user}はやられてしまった。。。" in line:
                    if self.monster and self.monster["rank"] == "超激レア":
                        await send("::i e")
                    else:
                        await send("::reset")
        else:
            if content == f"{self.bot.user.mention}これでいいの？\nこの変更で大丈夫な場合は『ok』\nキャンセルの場合は『no』と発言してください。":
                await send("Ok")
            if embed.description == f"{self.bot.user.mention}はエリクサーを使った！このチャンネルの仲間全員が全回復した！\n\nこのチャンネルの全てのPETが全回復した！":
                await asyncio.sleep(30)
                await send(self.mode * 2)
                await send(self.mode)
            if embed.description == "前の人のコマンドがまだ実行中だよ！":
                await asyncio.sleep(5)
                await send(self.mode)
            if embed.description == f"{self.bot.user.mention}はもうやられている！（戦いをやり直すには「::reset」だ）":
                await asyncio.sleep(1.5)
                if self.monster and self.monster["rank"] == "超激レア":
                    mode = "::i e "
                else:
                    mode = "::reset"
                await send(mode)
            if embed.description == f"{self.bot.user.mention}さん...\nゲームにログインしてね！！\n[コマンドは::loginだよ！！]":
                await asyncio.sleep(5)
                await send("::login")
                await asyncio.sleep(7)
                await send(self.mode)
            if embed.description == f"{self.bot.user.mention}さん...\n職業選択してね！\n[コマンドは::roleだよ！！]":
                await send("::role 0")
                await asyncio.sleep(5)
                await send(self.mode)
            if embed.title is not discord.Embed.Empty:
                lines = embed.title.splitlines()
                if len(lines) == 3:
                    attribute_ = [re.search("(属性:\[)((.+)*)(\])", lines[0]), 2]
                    rank_ = [re.search("(ランク:【)((.+)*)(】)", lines[0]), 2]
                    name_ = [re.search("((.+)*)(が待ち構えている...！)", lines[1]), 1]
                    lv_ = [re.search("(Lv.)((.+)*)( )", lines[2]), 2]
                    hp_ = [re.search("(HP:)((.+)*)", lines[2]), 2]
                    if [c for c in [attribute_, rank_, name_, lv_, hp_] if c[0] is None]: return
                    attribute = attribute_[0].group(attribute_[1])
                    rank = rank_[0].group(rank_[1])
                    name = name_[0].group(name_[1])
                    lv = lv_[0].group(lv_[1])
                    hp = hp_[0].group(hp_[1])
                    self.monster = dict(attribute=attribute,rank=rank,name=name,lv=lv,hp=hp)
                    if self.monster["name"] == "雪の精霊　ジャックフロスト":
                        self.mode = self.modes[1]
                    else:self.mode = self.modes[0]
                    await asyncio.sleep(5)
                    await send(self.mode)

def setup(bot):
    bot.add_cog(TAO(bot))
