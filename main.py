import asyncio
import random
import json

import discord
from discord.ext import commands

from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

token = ''

file = open('config.json')
config = json.load(file)


bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

bot.remove_command('help')

"""
@bot.event
async def on_ready():
    print('Бот запущен')

"""


@slash.slash(name='hi', description='поприветствовать',
             options=[{"name": "member", "description": "пользователь", "type": 6, "requied": False}],
             guild_ids=[972979068184170567])
@bot.command(aliase=['hi'])
async def hi(ctx, member: discord.Member = None):
    await ctx.send(f"Передаю привет, {member}!")


@bot.command(name='хелп')  #
async def help(ctx):
    await ctx.reply(f'Сообщение с помощью')


@bot.command(name='юзер')  #
async def user(ctx, member: discord.Member = None):
    stat = None
    if member:
        if member.status == discord.Status.online:
            stat = 'В сети'
        elif member.status == discord.Status.offline:
            stat = 'Не в сети'
        elif member.status == discord.Status.idle:
            stat = 'Не активен'
        elif member.status == discord.Status.dnd:
            stat = 'Не беспокоить'
        emb = discord.Embed(description=f'**Основная информация**'
                                        f'\n**Имя пользователя:** {member}'
                                        f'\n**Статус:** {stat}'
                                        f'\n**Присоединился:** {member.joined_at.strftime("%#d %B %Y г.")}'
                                        f'\n**Дата регистрации:** {member.created_at.strftime("%#d %B %Y г.")}',
                                        color=0xFFA550)
        emb.set_author(name=f'Информация о {member.name}', icon_url=member.avatar_url)
        emb.set_thumbnail(url=member.avatar_url)
        emb.set_footer(text=f'ID: {member.id}')
        await ctx.reply(embed=emb)
    else:
        if ctx.message.author.status == discord.Status.online:
            stat = 'В сети'
        elif ctx.message.author.status == discord.Status.offline:
            stat = 'Не в сети'
        elif ctx.message.author.status == discord.Status.idle:
            stat = 'Не активен'
        elif ctx.message.author.status == discord.Status.dnd:
            stat = 'Не беспокоить'
        emb = discord.Embed(
            description=f'**Основная информация**'
                        f'\n**Имя пользователя:** {ctx.message.author}'
                        f'\n**Статус:** {stat}'
                        f'\n**Присоединился:** {ctx.message.author.joined_at.strftime("%#d %B %Y г.")}'
                        f'\n**Дата регистрации:** {ctx.message.author.created_at.strftime("%#d %B %Y г.")}',
            color=0xFFA550)
        emb.set_author(name=f'Информация о {ctx.message.author.name}', icon_url=ctx.message.author.avatar_url)
        emb.set_thumbnail(url=ctx.message.author.avatar_url)
        emb.set_footer(text=f'ID: {ctx.message.author.id}')
        await ctx.reply(embed=emb)


@bot.command(name='мьют')  # ✅
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None, time=None, reason: str = None):
    muterole = discord.utils.get(ctx.guild.roles, id=973548658542907472)
    if member:
        emb = discord.Embed(description=f'✅ Пользователь **{member.name}** был замьючен!', color=0xFFA550)
        emb.add_field(name="Модератор", value=ctx.message.author.mention, inline=True)
        if time:
            time_letter = time[-1:]
            time_number = int(time[:-1])
            if time_letter == 's':
                time_letter = 1
            elif time_letter == 'с':
                time_letter = 1
            elif time_letter == 'm':
                time_letter = 60
            elif time_letter == 'м':
                time_letter = 60
            elif time_letter == 'h':
                time_letter = 3600
            elif time_letter == 'ч':
                time_letter = 3600
            elif time_letter == 'd':
                time_letter = 86400
            elif time_letter == 'д':
                time_letter = 86400

            emb.add_field(name="Срок", value=str(time), inline=True)

            if reason:
                emb.add_field(name="Причина", value=reason, inline=False)
                await ctx.reply(embed=emb)
                await member.add_roles(muterole)
                await asyncio.sleep(time_number*time_letter)
                await member.remove_roles(muterole)
            else:
                await ctx.reply(embed=emb)
                await member.add_roles(muterole)
                await asyncio.sleep(time_number*time_letter)
                await member.remove_roles(muterole)
        else:
            await ctx.reply(embed=emb)
            await member.add_roles(muterole)
    else:
        await ctx.reply(f'Пользователь не найден')


@bot.command(name='размьют')  # ✅
@commands.has_permissions(administrator=True)
async def un_mute(ctx, member: discord.Member = None):
    if member:
        muterole = discord.utils.get(ctx.guild.roles, id=973548658542907472)
        emb = discord.Embed(description=f'✅ Пользователь {member.mention} был размьючен!', color=0xFFA550)
        emb.add_field(name="Модератор", value=ctx.message.author.mention, inline=False)
        await member.remove_roles(muterole)
        await ctx.reply(embed=emb)
    else:
        await ctx.reply('Пользователь не найден')


@bot.command(name='бан')  #
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member = None, time=None, reason: str = None):
    if member:
        emb = discord.Embed(description=f'✅ Пользователь **{member.name}** был забанен!', color=0xFFA550)
        emb.add_field(name="Модератор", value=ctx.message.author.mention, inline=True)
        users = await ctx.guild.bans()
        if time:
            time_letter = time[-1:]
            time_number = int(time[:-1])
            if time_letter == 's':
                time_letter = 1
            elif time_letter == 'с':
                time_letter = 1
            elif time_letter == 'm':
                time_letter = 60
            elif time_letter == 'м':
                time_letter = 60
            elif time_letter == 'h':
                time_letter = 3600
            elif time_letter == 'ч':
                time_letter = 3600
            elif time_letter == 'd':
                time_letter = 86400
            elif time_letter == 'д':
                time_letter = 86400

            emb.add_field(name="Срок", value=str(time), inline=True)

            if reason:
                emb.add_field(name="Причина", value=reason, inline=False)
                await ctx.reply(embed=emb)
                await member.ban(reason=reason)
                await asyncio.sleep(time_number*time_letter)
                for ban_user in users:
                    if ban_user.user == member:
                        await ctx.guild.unban(ban_user.user)
            else:
                await ctx.reply(embed=emb)
                await member.ban()
                await asyncio.sleep(time_number*time_letter)
                for ban_user in users:
                    if ban_user.user == member:
                        await ctx.guild.unban(ban_user.user)
        else:
            await ctx.reply(embed=emb)
            await member.ban()
    else:
        await ctx.reply(f'Пользователь не найден')


@bot.command(name='разбан')  #
@commands.has_permissions(administrator=True)
async def un_ban(ctx, member: discord.Member = None):
    if member:
        users = await ctx.guild.bans()
        for ban_user in users:
            if ban_user.user == member:
                emb = discord.Embed(description=f'✅ Пользователь {member.mention} был разбанен!', color=0xFFA550)
                emb.add_field(name="Модератор", value=ctx.message.author.mention, inline=False)
                await ctx.guild.unban(ban_user.user)
                await ctx.reply(embed=emb)
            else:
                print('не то')
    else:
        await ctx.reply(f'Пользователь не найден')


@bot.command(name='монетка')  # ✅
async def coin(ctx):
    side = random.randint(1, 2)
    if side == 1:
        emb = discord.Embed(description='Орёл', color=0xFFA550)
    else:
        emb = discord.Embed(description='Решка', color=0xFFA550)
    await ctx.reply(embed=emb)


@bot.command(name='шар')  # ✅
async def ball(ctx, question=None):
    if question:
        emb = discord.Embed(description=question, color=0xFFA550)
        r = random.randint(1, 20)

        # Положительные ответы
        if r == 1:
            answer = 'Бесспорно 👍'
        elif r == 2:
            answer = 'Предрешено 👍'
        elif r == 3:
            answer = 'Никаких сомнений 👍'
        elif r == 4:
            answer = 'Определённо да 👍'
        elif r == 5:
            answer = 'Можешь быть уверен(а) в этом 👍'

        # Нерешительно положительные ответы
        elif r == 6:
            answer = 'Мне кажется — да 👌'
        elif r == 7:
            answer = 'Вероятнее всего 👌'
        elif r == 8:
            answer = 'Хорошие перспективы 👌'
        elif r == 9:
            answer = 'Знаки говорят — да 👌'
        elif r == 10:
            answer = 'Да 👌'

        # Нейтральные ответы
        elif r == 11:
            answer = 'Пока не ясно, попробуй снова ❔'
        elif r == 12:
            answer = 'Спроси позже ❔'
        elif r == 13:
            answer = 'Лучше промолчу ❔'
        elif r == 14:
            answer = 'Сейчас не могу предсказать ❔'
        elif r == 15:
            answer = 'Сконцентрируйся и спроси ещё раз ❔'

        # Отрицательные ответы
        elif r == 16:
            answer = 'Даже не думай ❌'
        elif r == 17:
            answer = 'Мой ответ — нет 🚫'
        elif r == 18:
            answer = 'По моим данным — нет 🚫'
        elif r == 19:
            answer = 'Перспективы не очень хорошие ⛔'
        else:
            answer = 'Весьма сомнительно ❓'

        emb.add_field(name="Ответ:", value=answer, inline=False)
        await ctx.reply(embed=emb)
    else:
        await ctx.repl('Нет вопроса - нет ответа')


@bot.command(name='аватар')  # ✅
async def avatar(ctx, member: discord.Member = None):
    if member:
        emb = discord.Embed(title=f'Аватар {member.name}', color=0xFFA550)
        emb.set_image(url=member.avatar_url)
        await ctx.reply(embed=emb)
    else:
        emb = discord.Embed(title=f'Аватар {ctx.message.author.name}', color=0xFFA550)
        emb.set_image(url=ctx.message.author.avatar_url)
        await ctx.reply(embed=emb)


@bot.command(name='рандом')  # ✅
async def rand(ctx, first: int, second: int):
    await ctx.reply(random.randint(first, second))


@bot.command(name='решить')  # ✅
async def solve(ctx, example):
    result = eval(example)
    emb = discord.Embed(description=f'Результат вычисления выражения `{example}`:'
                                    f'\n```{result}```',
                        color=0xFFA550)
    await ctx.reply(embed=emb)


@bot.command(name='очистить')  #
async def clear(ctx, count: int):
    await ctx.channel.purge(limit=count+1)
    await ctx.send(f'✅ Очищено {count} сообщений!')


bot.run(config[token])
