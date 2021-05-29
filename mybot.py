try:
    import conf
except ImportError:
    pass

import discord
from discord.ext import commands
import img_handler as imhl
import os,random
import img_handler as imhl
import fight as f



intense = discord.Intents.default()
intense.members = True
bot = commands.Bot(command_prefix="!", intents=intense)
whitelist = {
    822806350886207538: {825339772032778281:"bots/danilulan-bot"}
}
def allowed_channel():
    async def predicate(ctx:commands.Context):
        if ctx.guild.id in whitelist:
            if ctx.channel.id in whitelist[ctx.guild.id].keys():
                return True
        return False
    return commands.check(predicate)

    

@bot.command(name = "about")
@allowed_channel()
async def command_about(ctx, *args):
    msg = f'he your {ctx.author.name}, {ctx.author.id}'
    await ctx.channel.send(msg)

@bot.command(name = "mka")
@allowed_channel()
async def command_mka(ctx, f1:discord.Member=None, f2:discord.Member=None  ):
    msg=None

    if f1 and f2:
        await imhl.vs_create_animated(f1.avatar_url,f2.avatar_url,f1.name,f2.name)
        await ctx.channel.send( file=discord.File(os.path.join("./img/result.gif")))

@bot.command(name="join")
@allowed_channel()
async def vc_join(ctx):
    msg =""
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        msg = f"подключаюсь к {voice_channel.name}"
        await voice_channel.connect()
        await ctx.channel.send(msg)

@bot.command(name="leave")
@allowed_channel()
async def vc_leave(ctx):
    msg =""
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        msg = f"отключаюсь к {voice_channel.name}"
        await ctx.voice_client.disconnect()
        await ctx.channel.send(msg)

@bot.command(name="batle")
@allowed_channel()
async def vc_ost(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await ctx.channel.send("fight")
    # await voice_client.play(   discord.FFmpegPCMAudio( executable="ffmpeg.exe", source="./sound/mk.mp3"))
    await voice_client.play(   discord.FFmpegPCMAudio( source="./sound/mk.mp3"))


# @bot.command(name = "fight")
# @allowed_channel()
# async def command_fight(ctx):
    msg = ""
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        if len(ctx.author.voice.channel.members) >= 1:
            await voice_channel.connect()
            f1 = ctx.author.voice.channel.members[0]
            f2 = ctx.author.voice.channel.members[1]
            await imhl.vs_create(f1.avatar_url,f2.avatar_url,f1.name,f2.name)
            msg = f'В бой вступают {f1.name} {f"({f1.nick})" if f1.nick else ""} и {f2.name} {f"({f2.nick})" if f2.nick else ""}'
            await ctx.channel.send(msg)
            await ctx.channel.send( file=discord.File(os.path.join("./img/result.png")))
            await imhl.vs_create_animated(f1.avatar_url, f2.avatar_url,f1.name,f2.name)
            await ctx.channel.send(file=discord.File(os.path.join("./img/result.gif")))
            voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            await voice_client.play(discord.FFmpegPCMAudio(executable="./sound/ffmpeg.exe", source="./sound/mk.mp3"))
        if len(ctx.author.voice.channel.members)-1 >2:
            mass1 = ctx.author.voice.channel.members
            a = random.randint(0, len(mass1) - 1)
            f1 = mass1[a]
            mass1.pop(a)
            b = random.randint(0, len(mass1) - 1)

            f2 = mass1[b]
            await voice_channel.connect()
            msg = f'В бой вступают {f1.name} {f"({f1.nick})" if f1.nick else ""} и {f2.name} {f"({f2.nick})" if f2.nick else ""}'
            await ctx.channel.send(msg)
            await ctx.channel.send( file=discord.File(os.path.join("./img/result.png")))
            await imhl.vs_create_animated(f1.avatar_url, f2.avatar_url,f1.name,f2.name)
            await ctx.channel.send(file=discord.File(os.path.join("./img/result.gif")))
            voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            await voice_client.play(discord.FFmpegPCMAudio(executable="./sound/ffmpeg.exe", source="./sound/mk.mp3"))

@bot.command(name="ost")
async def vs_ost(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    await ctx.channel.send(f'MORTAL COMBAAT')
    await voice_client.play(discord.FFmpegPCMAudio(source="./mp3/mk.mp3"))

@bot.command(name="fight")
@allowed_channel()
async def fight(ctx:commands.Context):
    # Первый претендент
    f1:discord.Member = None
    # Второй претендент
    f2:discord.Member = bot.user
    # Voice-канал участника
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        await vc_join(ctx)
        # Список активных пользователей
        voice_members = voice_channel.members
        # Фильтруем пользователей, оставляя только людей
        voice_members = [member for member in voice_members if member.bot == False]
        # Отбираем претендентов
        if len(voice_members) > 1:
            # a,b = [1, 2]   => a = 1    b = 2
            f1, f2 = [voice_members.pop(random.randint(0, len(voice_members)-1)), voice_members.pop(random.randint(0, len(voice_members)-1))]
        else:
            f1 = ctx.author
        # СОЗДАТЬ VS_SCREEN
        await imhl.vs_create_animated(f1.avatar_url, f2.avatar_url)

        embed = discord.Embed(
            title = "Let's Mortal Kombat Begins!",
            description = f'{f1.display_name} бьётся с {f2.display_name}',
            colour = discord.Colour.dark_purple(),
        )

        message = await ctx.channel.send(embed = embed, file=discord.File(os.path.join("./img/result.gif")))
        # ЗАПУСТИТЬ МУЗЫКУ
        voice_client = discord.utils.get(bot.voice_clients, guild = ctx.guild)
        # await voice_client.play(discord.FFmpegPCMAudio(source="./mp3/mk.mp3"))

        await f.create_fighters(f1, f2, message)


        await voice_client.stop()

        
    else: 
        await ctx.channel.send("Зайдите в voice-канал пожажя")

bot.run(os.environ["BOT_TOKEN"])