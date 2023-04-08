import discord
import config
import asyncio
import time

from discord.ext import commands
from discord.ext.commands import Bot


Bot = commands.Bot(command_prefix=config.PREFIX)
Bot.remove_command('help')
# Статус бота + Запуск


@Bot.event
async def on_ready():
     activity = discord.Game(name="Привет мир!", type=2)
     await Bot.change_presence(status=discord.Status.online, activity=activity)
     print("[!] Logged in as:")
     print("[!] Status: ✅")
     print("[!] The bot is ready to work")


# Команды модерации


@Bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, time: int, reason):
    channel = Bot.get_channel(974392998571950150)
    muterole = discord.utils.get(ctx.guild.roles, id = 973548658542907472)
    emb = discord.Embed(color=344462)
    emb.add_field(name="✅ Muted", value='Пользователь {} был замьючен!'.format(member.mention))
    emb.add_field(name="Модератор", value = ctx.message.author.mention, inline = False)
    emb.add_field(name="Причина", value = reason, inline = False)
    await channel.send(embed=emb)
    await member.add_roles(muterole)
    await asyncio.sleep(time * 60)
    await member.remove_roles(muterole)


@Bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    channel = Bot.get_channel(974392998571950150)
    muterole = discord.utils.get(ctx.guild.roles, id = 973548658542907472)
    emb = discord.Embed(color=344462)
    emb.add_field(name="✅ UnMuted", value='Пользователь {} был размьючен!'.format(member.mention))
    emb.add_field(name="Модератор", value = ctx.message.author.mention, inline = False)
    await member.remove_roles(muterole)
    await channel.send(embed = emb)


@Bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason):
    channel = Bot.get_channel(974392998571950150)
    await member.kick(reason = reason)
    await ctx.channel.purge(limit=0)
    emb = discord.Embed(color=344462)
    emb.add_field(name='✅ Kick пользователя', value='Пользователь {} был кикнут!'.format(member.mention))
    await channel.send(embed = emb)


@Bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, days, reason):
    channel = Bot.get_channel(974392998571950150)
    await member.ban(reason=reason)
    await ctx.channel.purge(limit=0)
    emb = discord.Embed(color=344462)
    emb.add_field(name='✅ Ban пользователя', value='Пользователь {} был забанен!'.format(member.mention))
    await channel.send(embed = emb)


@Bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    channel = Bot.get_channel(974392998571950150)
    banned_users = await ctx.guild.bans()
    await ctx.channel.purge(limit=0)

    for ban_entry in banned_users:
        user = ban_entry.user
        await ctx.guild.unban(user)
        emb = discord.Embed(color=344462)
        emb.add_field(name='✅ UnBan пользователя', value='Пользователь {} был разбанен.'.format(member))
        await channel.send(embed = emb)
        return


@Bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amout=1000):
    await ctx.channel.purge(limit=amout)


@Bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx,arg):
        await ctx.send(arg)


@Bot.command()
@commands.has_permissions(administrator=True)
async def info(ctx, member:discord.Member):
        emb = discord.Embed(title='✅ Информация о пользователе', color=344462)
        await ctx.channel.purge(limit=0)
        emb.add_field(name="Дата инвайта на сервер:", value=member.joined_at, inline=False)
        emb.add_field(name="Никнейм:", value=member.display_name, inline=False)
        emb.add_field(name= "Айди:", value=member.id, inline=False)
        emb.add_field(name= "Аккаунт создан:", value=member.created_at.strftime("%a,%#d %B %Y, %I:%M %p UTC"), inline=False)
        emb.set_thumbnail(url=member.avatar_url)
        emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        await ctx.author.send(embed = emb)
        await ctx.send('***Подробная информация о пользоваетеле была отправлена в личные сообщения.***')


@Bot.command()
async def help( ctx ):
        emb = discord.Embed( title = '✅ Информация о командах сервера', color=344462)
        emb.add_field( name = '{}clear'.format( config.PREFIX ), value = 'Очистка чата одной командой', inline = False)
        emb.add_field( name = '{}kick'.format( config.PREFIX ), value = 'Кик участника сервера', inline = False)
        emb.add_field( name = '{}mute'.format( config.PREFIX ), value = 'Выдать мут участнику сервера', inline = False)
        emb.add_field( name = '{}unmute'.format( config.PREFIX ), value = 'Снятие мута на сервере', inline = False)
        emb.add_field( name = '{}ban'.format( config.PREFIX ), value = 'Бан пользователя на сервере')
        emb.add_field( name = '{}say'.format( config.PREFIX ), value = 'Эхо бот(дублирование вашого сообщения)', inline = False)
        emb.set_thumbnail(url = ctx.author.avatar_url)
        emb.add_field( name = '{}info'.format( config.PREFIX ), value = 'Показать подробную информацию об участнике', inline = False)
        await ctx.author.send(embed = emb)
        await ctx.send('*****Отправил вам список команд в личку :D*****')
# Запуск бота
Bot.run(config.TOKEN)
