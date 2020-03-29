import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import colorsys
import random
import time
import os
import json
import aiohttp
import datetime
from discord import Game, Embed, Color, Status, ChannelType
import logging
import requests
import urllib.request

bot = commands.Bot(command_prefix=commands.when_mentioned_or('e!','E!'),case_insensitive=True)
bot.remove_command("help")

helpm = discord.Embed(description='**[HELP MENU](https://discord.gg/kuWVFpR)**\n● To get detailed help on an category, type `e!help 1`,`e!help 2` Etc. accordingly!', color = 0xFFBF00) 
helpm.set_author(name='ELECTRO',url='https://discord.gg/kuWVFpR', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
helpm.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/679975327698649109/ElectroCommandsCategories.gif')
helpm.add_field(name = '<:ElectroGeneralBadge:680783367247364097> GENERAL COMMANDS - (21)',value ='`ping`, `userinfo`, `serverinfo`, `ownerinfo`, `avatar`, `membercount`, `math`, `invite`, `upvote`, `pokemon`, `shinypokemon`, `pokefuse`, `8ball`, `electroav`, `brilliance`, `bravery`, `balance`, `coronaav`, `coronaav-green`, `coronaav-purple`, `coronaav-pink`, `corona`',inline = False)
helpm.add_field(name = '<:ElectroModerationBadge:680783390999314466> MODERATION COMMANDS - (17)',value ='`kick`, `ban`, `setnick`, `role`, `say`, `embed`, `DM`, `english`, `rolecolor`, `lockdown`, `unlock`, `menro`, `mute`, `unmute`, `joinchannel`, `leavechannel`, `testwelcomer`',inline = False)
helpm.add_field(name = '<:ElectroFunBadge:680783413065941002> FUN COMMANDS - (26)',value ='`triggered`, `brazzers`, `burn`, `gay`, `missionpassed`, `thanos`, `rip`, `meme`, `pat`, `love`, `slap`, `kiss`, `hug`, `cuddle`, `spank`, `tweet`, `phubcomment`, `howgay`, `whowouldwin`, `captcha`, `magik`, `deepfry`,`iphonex`, `threats`, `clyde`, `trash`',inline = False)
helpm.add_field(name = '<:ElectroMusicBadge:680783435123654657> MUSIC COMMANDS - (8)',value ='`play`, `skip`, `stop`, `NP`, `queue`, `pause`, `resume`, `volume`',inline = False)
helpm.add_field(name = '<:ElectroNSFWBadge:680783452563439774> NSFW COMMANDS - (26)',value ='Human:\n|| `boobs`, `pussy`, `ass`, `thighs`, `porngif`, `4k`, `anal` ||\nAnime:\n|| `classic`, `blowjob`, `hentai`, `hentaianal`, `hentaithigh`, `hentaineko`, `hentaikitsune`, `girlsolo`, `pussygif`, `feet`, `femdom`, `pussyart`, `smallboobs`, `girlsologif`, `classic`, `cumsluts`, `randomhentaigif`, `bjgif`, `lesbian` ||\n\n<:ElectroBookmark:668018207549816833> **USEFUL LINKS:**\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)',inline = False)
helpm.set_footer(text ='© 2020 ELECTRO, Inc. | ADIB HOQUE')

def is_premium(ctx):
        return ctx.message.author.id == "496978159724396545"     

async def status_task():
    while True:
        await bot.change_presence(game=discord.Game(name='e!help | '+str(len(bot.servers))+' Servers | '+str(len(set(bot.get_all_members())))+' Users'))
        await asyncio.sleep(12)
        await bot.change_presence(game=discord.Game(name='e!help | '+str(len(bot.servers))+' servers | '+str(len(set(bot.get_all_members())))+' Users'))
        await asyncio.sleep(12)

async def is_nsfw(channel: discord.Channel):
    try:
        _gid = channel.server.id
    except AttributeError:
        return False
    data = await bot.http.request(
        discord.http.Route(
            'GET', '/guilds/{guild_id}/channels', guild_id=_gid))
    channeldata = [d for d in data if d['id'] == channel.id][0]
    return channeldata['nsfw']

@bot.event
async def on_ready():
    print('ONLINE')
    bot.loop.create_task(status_task())
    global amounts
    try:
        with open('test.json') as f:             
            amounts = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        amounts = {}

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        embed=discord.Embed(description="<a:ElectroError:646994154152525845> **Command On Cooldown.**\nPlease try again in **%.2fs**!"% error.retry_after, color=0xFFBF00)
        await bot.send_message(ctx.message.channel, embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        embed=discord.Embed(description="<a:ElectroError:646994154152525845> **Command Not Found.**\nPlease type `e!help` or join [Support Server](https://discord.gg/kuWVFpR) to know the existing commands!", color=0xFFBF00)
        await bot.send_message(ctx.message.channel, embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(description="<a:ElectroError:646994154152525845> **Missing Required Argument.**\nPlease type `e!help` or join [Support Server](https://discord.gg/kuWVFpR) to know how to use this command properly!", color=0xFFBF00)
        await bot.send_message(ctx.message.channel, embed=embed)
    elif isinstance(error, commands.CheckFailure):
        embed=discord.Embed(description="<a:ElectroPremium:686469174528442379> **ELECTRO PREMIUM**\nThis is a premium or developer only command. Join our [Support Server](https://discord.gg/kuWVFpR) for more info!", color=0xFFBF00)
        await bot.send_message(ctx.message.channel, embed=embed)
    raise error
        
@bot.command(pass_context = True)
async def prefix(ctx):
	embed=discord.Embed(description="The prefix for the bot is **e!** or mention.", color=0xFFBF00)
	await bot.say(embed=embed) 

def is_owner(ctx):
    return ctx.message.author.id == "496978159724396545"     

def predicate(message, l, r):
    def check(reaction, user):
        if reaction.message.id != message.id or user == client.user:
            return False

    return check

@bot.command(pass_context = True)
@commands.check(is_owner)
async def servers(ctx):
  servers = list(bot.servers)
  await bot.say(f"Connected on {str(len(servers))} servers:")
  await bot.say('\n'.join(server.name for server in servers))
  for server in bot.servers:
        try:
                randomchannel = random.choice(server.channels)
                invitelink = await bot.create_invite(destination = randomchannel, xkcd = True, max_uses = 100)
                await bot.say("**SERVER NAME:** {}\n**MEMBERCOUNT:** {}\n{}\n{]".format(server.name,server.member_count,server.icon_url,invitelink))
        except:
                await bot.say("{} - {}".format(server.name,server.member_count))

@bot.command(pass_context = True)
@commands.cooldown(1, 1800, commands.BucketType.server)
async def revive(ctx):
        role = discord.utils.get(ctx.message.server.roles, name='#ActiveSquad')
        embed = discord.Embed(description = "{} wants you to revive the chat!".format(ctx.message.author), color=0xFFBF00)
        await bot.send_message(ctx.message.channel,role.mention,embed=embed)

@bot.command(pass_context=True)
@commands.check(is_premium)
@commands.has_permissions(manage_messages=True)
async def richembedadfT(ctx):
    q1 = await bot.send_message(ctx.message.channel, "What should be the embed Author?")
    a1 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    q2 = await bot.send_message(ctx.message.channel, "What should be the embed Description?")
    a2 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    q3 = await bot.send_message(ctx.message.channel, "What should be the embed Thumbnail url?")
    a3 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    q4 = await bot.send_message(ctx.message.channel, "What should be the embed Footer?")
    a4 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    embed = discord.Embed(author='{}'.format(a1.content), description='{}'.format(a2.content),color=0xFFBF00)
    embed.set_thumbnail(url = '{}'.format(a3.content))
    embed.set_footer(text='{}'.format(a4.content))
    await bot.send_message(ctx.message.channel, embed=embed)
    await bot.delete_message(ctx.message) 
    await bot.delete_message(a1)
    await bot.delete_message(q1)
    await bot.delete_message(a2)
    await bot.delete_message(q2)
    await bot.delete_message(a3)
    await bot.delete_message(q3)
    await bot.delete_message(a4) 
    await bot.delete_message(q4)
	
@bot.command(pass_context=True)
@commands.check(is_premium)
@commands.has_permissions(manage_messages=True)
async def richembedadfi(ctx):
    q1 = await bot.send_message(ctx.message.channel, "What should be the embed Author?")
    a1 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    q2 = await bot.send_message(ctx.message.channel, "What should be the embed Description?")
    a2 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    q3 = await bot.send_message(ctx.message.channel, "What should be the embed Image url?")
    a3 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    q4 = await bot.send_message(ctx.message.channel, "What should be the embed Footer?")
    a4 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    embed = discord.Embed(title='{}'.format(a1.content), description='{}'.format(a2.content),color=0xFFBF00)
    embed.set_image(url = '{}'.format(a3.content))
    embed.set_footer(text='{}'.format(a4.content))
    await bot.send_message(ctx.message.channel, embed=embed)
    await bot.delete_message(ctx.message) 
    await bot.delete_message(a1)
    await bot.delete_message(q1)
    await bot.delete_message(a2)
    await bot.delete_message(q2)
    await bot.delete_message(a3)
    await bot.delete_message(q3)
    await bot.delete_message(a4) 
    await bot.delete_message(q4)

@bot.command(pass_context=True)
@commands.check(is_premium)
@commands.has_permissions(manage_messages=True)
async def richembedtdfT(ctx):
    q1 = await bot.send_message(ctx.message.channel, "What should be the embed Title?")
    a1 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    q2 = await bot.send_message(ctx.message.channel, "What should be the embed Description?")
    a2 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    q3 = await bot.send_message(ctx.message.channel, "What should be the embed Thumbnail url?")
    a3 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    q4 = await bot.send_message(ctx.message.channel, "What should be the embed Footer?")
    a4 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    embed = discord.Embed(title='{}'.format(a1.content), description='{}'.format(a2.content),color=0xFFBF00)
    embed.set_thumbnail(url = '{}'.format(a3.content))
    embed.set_footer(text='{}'.format(a4.content))
    await bot.send_message(ctx.message.channel, embed=embed)
    await bot.delete_message(ctx.message) 
    await bot.delete_message(a1)
    await bot.delete_message(q1)
    await bot.delete_message(a2)
    await bot.delete_message(q2)
    await bot.delete_message(a3)
    await bot.delete_message(q3)
    await bot.delete_message(a4) 
    await bot.delete_message(q4)
	
@bot.command(pass_context=True)
@commands.check(is_premium)
@commands.has_permissions(manage_messages=True)
async def richembedtdfi(ctx):
    q1 = await bot.send_message(ctx.message.channel, "What should be the embed Title?")
    a1 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    q2 = await bot.send_message(ctx.message.channel, "What should be the embed Description?")
    a2 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    q3 = await bot.send_message(ctx.message.channel, "What should be the embed Image url?")
    a3 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    q4 = await bot.send_message(ctx.message.channel, "What should be the embed Footer?")
    a4 = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
    embed = discord.Embed(title='{}'.format(a1.content), description='{}'.format(a2.content),color=0xFFBF00)
    embed.set_image(url = '{}'.format(a3.content))
    embed.set_footer(text='{}'.format(a4.content))
    await bot.send_message(ctx.message.channel, embed=embed)
    await bot.delete_message(ctx.message) 
    await bot.delete_message(a1)
    await bot.delete_message(q1)
    await bot.delete_message(a2)
    await bot.delete_message(q2)
    await bot.delete_message(a3)
    await bot.delete_message(q3)
    await bot.delete_message(a4) 
    await bot.delete_message(q4)
													
@bot.command(pass_context = True, aliases=['pong','PING'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(ctx):
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await bot.send_typing(channel)
    t2 = time.perf_counter()
    embed=discord.Embed(description="Pong! **{}ms**".format(round((t2-t1)*1000)), color=0xFFBF00) 
    await bot.say(embed=embed)

@bot.command(pass_context = True)
@commands.has_permissions(manage_nicknames=True)     
async def setnick(ctx, user: discord.Member, *, nickname):
    await bot.change_nickname(user, nickname)
    await bot.say("<a:ElectroSuccess:656772759812046851> | {}'s nickname was changed to {}!".format(user, nickname))
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
async def invite():
	embed=discord.Embed(description="Here are some useful links! If you have any questions about the bot, feel free to join the support guild and ask!.\nThank you for using the bot! 💛 from the bot developer `ADIB HOQUE#6969`", color=0xFFBF00)
	embed.set_author(name="ELECTRO's Invite URL", icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
	embed.add_field(name = 'Invite URL',value ='[https://invite.electro.xyz](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=2146827775&scope=bot)',inline = False)
	embed.add_field(name = 'Support Server',value ='[https://support.electro.xyz](https://discord.gg/kuWVFpR)',inline = False)
	embed.set_footer(text='We hope you have fun with the bot!', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
	await bot.say('https://discord.gg/kuWVFpR', embed=embed)
	
@bot.command(pass_context=True)
async def link():
	embed=discord.Embed(description="Here are some useful links! If you have any questions about the bot, feel free to join the support guild and ask!.\nThank you for using the bot! 💛 from the bot developer `ADIB HOQUE#6969`", color=0xFFBF00)
	embed.set_author(name="ELECTRO's Invite URL", icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
	embed.add_field(name = 'Invite URL',value ='[https://invite.electro.xyz](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=2146827775&scope=bot)',inline = False)
	embed.add_field(name = 'Support Server',value ='[https://support.electro.xyz](https://discord.gg/kuWVFpR)',inline = False)
	embed.set_footer(text='We hope you have fun with the bot!', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
	await bot.say('https://discord.gg/kuWVFpR', embed=embed)
	
@bot.command(pass_context=True)
async def server():
	embed=discord.Embed(description="Here are some useful links! If you have any questions about the bot, feel free to join the support guild and ask!.\nThank you for using the bot! 💛 from the bot developer `ADIB HOQUE#6969`", color=0xFFBF00)
	embed.set_author(name="ELECTRO's Support Server", icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
	embed.add_field(name = 'Invite URL',value ='[https://invite.electro.xyz](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=2146827775&scope=bot)',inline = False)
	embed.add_field(name = 'Support Server',value ='[https://support.electro.xyz](https://discord.gg/kuWVFpR)',inline = False)
	embed.set_footer(text='We hope you have fun with the bot!', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
	await bot.say('https://discord.gg/kuWVFpR', embed=embed)
	
@bot.command(pass_context=True)  
@commands.has_permissions(kick_members=True)     
async def kick(ctx, user:discord.Member, *, reason:str):
    if user is None or reason is None:
      await bot.say('<a:ElectroFail:656772856184832025> | **Please mention a user to kick & specify a reason for kicking out!**\nEXAMPLE:`e!kick <@user or id> <reason>`')
    if user.server_permissions.kick_members:
      await bot.say("<a:ElectroFail:656772856184832025> | **He is a Mod/Admin, I can't do that!**")
      return
    else:
      await bot.send_message(user, 'You were kicked out from **{}**, {}!'.format(ctx.message.server.name, reason))
      await bot.kick(user)
      await bot.say('<a:ElectroSuccess:656772759812046851> | {} was kicked, {}!'.format(user, reason))
      await bot.delete_message(ctx.message)
      for channel in ctx.message.author.server.channels:
        if channel.name == '⚡electro-logs':
            embed=discord.Embed(title="KICK COMMAND USED", description="**User:** {0}\n**Moderator:** {1}".format(user, ctx.message.author), color=0xFFBF00)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text ='USER KICKED')
            await bot.send_message(channel, embed=embed)
    
@bot.command(pass_context=True)  
@commands.has_permissions(ban_members=True)     
async def ban(ctx, user:discord.Member, *, reason:str=None):
    if user is None or reason is None:
      await bot.say('<a:ElectroFail:656772856184832025> | **Please mention a user to ban & specify a reason for banning!\nExample:`e!ban <@user or id> <reason>**')
    if user.server_permissions.kick_members:
      await bot.say("<a:ElectroFail:656772856184832025> | **He is a Mod/Admin, I can't do that!**")
      return
    else:
      await bot.send_message(user, 'You were banned from **{ctx.message.server.name}**, {reason}!'.format(ctx.message.server.name, reason))
      await bot.kick(user)
      await bot.say('<a:ElectroSuccess:656772759812046851> | {} was banned, {}!'.format(user, reason))
      await bot.delete_message(ctx.message)
      for channel in ctx.message.author.server.channels:
        if channel.name == '⚡electro-logs':
            embed=discord.Embed(title="BAN COMMAND USED", description="**User:** {0}\n**Moderator:** {1}".format(user, ctx.message.author), color=0xFFBF00)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text ='USER BANNED')
            await bot.send_message(channel, embed=embed)        

@bot.command(pass_context=True)  
@commands.has_permissions(ban_members=True)     
async def unban(ctx, identification:str):
    user = await bot.get_user_info(identification)
    await bot.unban(ctx.message.server, user)
    try:
        await bot.say(f'<a:ElectroSuccess:656772759812046851> | **{user} was unbanned!**')
        for channel in ctx.message.server.channels:
          if channel.name == '⚡electro-logs':
              embed=discord.Embed(title="UNBAN COMMAND USED", description="**User:** {0}\n**Moderator:**{1}**".format(user, ctx.message.author), color=0xFFBF00)
              embed.timestamp = datetime.datetime.utcnow()
              embed.set_footer(text ='USER BANNED')
              await bot.send_message(channel, embed=embed)
    except:
        await bot.say(f'I am unable to unban `{user}`, Please check my role permissions!')
        pass					

@bot.command(pass_context = True)  
async def userinfo(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title="{}'s info".format(user.name), description="HERE WHAT I FOUND!", color = 0xFFBF00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)	

@bot.command(pass_context = True ,aliases=['serverav','avserver'])  
async def serveravatar(ctx):
	url = ctx.message.server.icon_url
	await bot.say(url)

@bot.command(pass_context = True, aliases=['av','Av','Avatar'])
async def avatar(ctx, user: discord.Member=None):
    if user is None:
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title='Your Avatar', color = 0xFFBF00)
        embed.set_image(url = ctx.message.author.avatar_url)
        await bot.say(embed=embed)
    else:
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title="{}'s Avatar".format(user.name), color = 0xFFBF00)
        embed.set_image(url = user.avatar_url)
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def ownerinfo():
    embed = discord.Embed(description = '**Created by:**\n<a:adib:643372389224153089>ADIB HOQUE#2212', color = 0xFFBF00)
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/643421220108501002/643421321266462731/20191111_143116.gif')
    await bot.say(embed=embed)
    
@bot.command(pass_context=True)
async def owner():
    embed = discord.Embed(description = '**Created by:**\n<a:adib:643372389224153089>ADIB HOQUE#2212', color = 0xFFBF00)
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/643421220108501002/643421321266462731/20191111_143116.gif')
    await bot.say(embed=embed)    
    
@bot.command(pass_connext=True,aliases=['se'])
async def emoji(ctx, emoji: discord.Emoji):
    await bot.say(emoji.url)    		
	  		   	   	
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def dm(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    await bot.send_message(user, message)
    await bot.say('<a:ElectroSuccess:656772759812046851>YOUR DM WAS SENT!')
    await bot.delete_message(ctx.message)
    
@bot.command(pass_context = True)
async def customembed(ctx, msg:str, *, msg2:str):
    channel = ctx.message.channel
    if member.server_permissions.administrator == False:
    	await bot.say('**Your role must have admin permission to use this command!**')
    	return
    else:
    	r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    	embed=discord.Embed(title="{}".format(msg), description="{}".format(msg2), color = discord.Color((r << 16) + (g << 8) + b))
    	embed.set_footer(text ='© 2020 ELECTRO, Inc.')
    	await bot.send_message(channel, embed=embed)

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def say(ctx, *, message=None):
    message = message or "Please specify a message to say!"
    await bot.say(message)
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True) 
async def purge(ctx, number):
    mgs = [] 
    number = int(number) 
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await bot.delete_messages(mgs)
    await bot.say('<a:ElectroSuccess:656772759812046851> | {} MESSAGES WERE DELETED!'.format(number))

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def english(ctx, *, msg = None):
	channel = ctx.message.channel
	await bot.say(msg + ', Please do not use any other languages than **English.**')
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True)
@commands.check(is_owner)
async def masstype(ctx, *, message=None):
    message = message or "Please specify a word to masstype!"
    await bot.delete_message(ctx.message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)	
    
@bot.command(pass_context = True)
async def meme(ctx):
        async with aiohttp.ClientSession() as session:
          async with session.get("https://api.reddit.com/r/memes/random") as r:
            data = await r.json()
            embed = discord.Embed(title = data[0]["data"]["children"][0]["data"]["title"], color = 0xFFBF00)
            embed.set_image(url=data[0]["data"]["children"][0]["data"]["url"])
            await bot.say(embed=embed)

@bot.command(pass_context = True) 
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, user: discord.Member, *, role: discord.Role = None):
	if role is None:
		return await bot.say("Please specify a role to give! ")
	if role not in user.roles:
		await bot.add_roles(user, role)
		return await bot.say("<a:ElectroSuccess:656772759812046851> **{}** role has been added to **{}**.".format(role, user))

@bot.command(pass_context = True)
@commands.has_permissions(manage_roles=True)
async def menro(ctx, *, role: discord.Role):
	if role.mentionable==True:
		await bot.say('{}'.format(role.mention))
		await bot.edit_role(server=ctx.message.server, role=role, mentionable=False)
	else:
		await bot.edit_role(server=ctx.message.server, role=role, mentionable=True)
		await bot.say('{}'.format(role.mention))
		await bot.edit_role(server=ctx.message.server, role=role, mentionable=False)
	     
@bot.command(pass_context = True)
@commands.has_permissions(manage_roles=True)
async def mentionrole(ctx, *, role: discord.Role):
	if role.mentionable==True:
		await bot.say('{}'.format(role.mention))
		await bot.edit_role(server=ctx.message.server, role=role, mentionable=False)
	else:
		await bot.edit_role(server=ctx.message.server, role=role, mentionable=True)
		await bot.say('{}'.format(role.mention))
		await bot.edit_role(server=ctx.message.server, role=role, mentionable=False)	 
		
@bot.command(pass_context = True)
@commands.has_permissions(manage_roles=True)
async def mentionable(ctx, *, role: discord.Role):
	if role.mentionable==True:
		await bot.say('<a:ElectroFail:656772856184832025>**That role is already mentionable!**')
	else:
		await bot.edit_role(server=ctx.message.server, role=role, mentionable=True)
		await bot.say('<a:ElectroSuccess:656772759812046851>**Made the role mentionable!**')
		
@bot.command(pass_context = True)
@commands.has_permissions(manage_roles=True)
async def unmentionable(ctx, *, role: discord.Role):
	if role.mentionable==False:
		await bot.say('<a:ElectroFail:656772856184832025>**That role is already unmentionable!**')
	else:
		await bot.edit_role(server=ctx.message.server, role=role, mentionable=True)
		await bot.say('<a:ElectroSuccess:656772759812046851>**Made the role unmentionable!**')		
		
@bot.command(pass_context = True) 
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, user: discord.Member, *, role: discord.Role = None):
	if role is None:
		return await bot.say('Please specify a role to remove!')
	if role in user.roles:
		return await bot.remove_roles(user, role)
		return await bot.say("<:ElectroSucess:527118398753079317> **{}** role has been removed from **{}**.".format(role, user))

@bot.command(pass_context=True, aliases=['serveri'])
async def serverinfo(ctx):
    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50:
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = 0xFFBF00);
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = 'Owner', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = 'ID', value = str(server.id))
    join.add_field(name = 'Member Count', value = str(server.member_count));
    join.add_field(name = 'Text/Voice Channels__', value = str(channelz));
    join.add_field(name = 'Roles (%s)'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await bot.say(embed = join);
		   	   	     
@bot.command(pass_context=True)
async def tweet(ctx, usernamename:str, *, txt:str):
    url = f"  nekobot.xyz/api/imagegen?type=clickforhentai&image=https://cdn.discordapp.com/avatars/455322915471097857/d61b75a2318e59076dbd245981e5f0be.webp?size=1024&fontsize=7"
    async with aiohttp.ClientSession() as cs:
    	async with cs.get(url) as r:
            res = await r.json()
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = 0xFFBF00) 
            embed.set_image(url=res['message'])
            embed.title = "{} tweeted: {}".format(usernamename, txt)
            embed.set_footer(text ='© 2020 ELECTRO, Inc.')
            await bot.say(embed=embed)
		   	   	 
 
@bot.command(pass_context=True, aliases=['ship','shipuser'])
async def love(ctx, user: discord.Member = None, *, user2: discord.Member = None):
    shipuser1 = user.name
    shipuser2 = user2.name
    useravatar1 = user.avatar_url
    useravatar2s = user2.avatar_url
    self_length = len(user.name)
    first_length = round(self_length / 2)
    first_half = user.name[0:first_length]
    usr_length = len(user2.name)
    second_length = round(usr_length / 2)
    second_half = user2.name[second_length:]
    finalName = first_half + second_half
    score = random.randint(0, 100)
    filled_progbar = round(score / 100 * 10)
    counter_ = '■' * filled_progbar + '□' * (10 - filled_progbar)
    url = f"https://nekobot.xyz/api/imagegen?type=ship&user1={useravatar1}&user2={useravatar2s}"
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            res = await r.json()
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(title=f"💛Love Meter💛", description=f"**💖{shipuser1}**\n**💖{shipuser2}**\n{score}% [{counter_}](https://discord.gg/kuWVFpR)", color = 0x429CFF) 
            embed.set_image(url=res['message'])
            await bot.say(embed=embed)
 
@bot.command(pass_context=True, aliases=['gayrate','howmuchgay','g8','lesborate'])
async def howgay(ctx, user: discord.Member=None):
        if user is None:
                score = random.randint(0, 100)
                filled_progbar = round(score / 100 * 10)
                counter_ = '■' * filled_progbar + '□' * (10 - filled_progbar)
                embed = discord.Embed(title=f'Gayrate of {ctx.message.author}',description=f':couple:[{counter_}](https://discord.gg/kuWVFpR):couple_mm: (**{score}%**)',color=0xFFBF00)
                await bot.say(embed=embed)
        else:
                score = random.randint(0, 100)
                filled_progbar = round(score / 100 * 10)
                counter_ = '■' * filled_progbar + '□' * (10 - filled_progbar)
                embed = discord.Embed(title=f'Gayrate of {user}',description=f' :couple:[{counter_}](https://discord.gg/kuWVFpR):couple_mm: (**{score}%**)',color=0xFFBF00)
                await bot.say(embed=embed)

@bot.command(pass_context = True)
async def rolldice(ctx):
    choices = ['1', '2', '3', '4', '5', '6']
    em = discord.Embed(title='Rolled! (1 6-sided dice)', description='{}'.format(random.choice(choices)),color=0xFFBF00)
    await bot.say(embed=em)

@bot.command(pass_context=True)
async def membercount(ctx, *args):
    g = ctx.message.server

    gid = g.id
    membs = str(len(g.members))
    membs_on = str(len([m for m in g.members if not m.status == Status.offline]))
    users = str(len([m for m in g.members if not m.bot]))
    users_on = str(len([m for m in g.members if not m.bot and not m.status == Status.offline]))
    bots = str(len([m for m in g.members if m.bot]))
    bots_on = str(len([m for m in g.members if m.bot and not m.status == Status.offline]))
    created = str(g.created_at)
    
    em = Embed(title="Membercount", color = 0xFFBF00)
    em.description =    "\n" \
                        "**Total Members:** %s (%s online)\n" \
                        "**User Count:** %s (%s online)\n" \
                        "**Bot Count:** %s (%s online)\n" \
                        "**Created at:** %s\n" \
                        "" % (membs, membs_on, users, users_on, bots, bots_on, created)

    await bot.send_message(ctx.message.channel, embed=em)
    await bot.delete_message(ctx.message)
    
@bot.group(pass_context=True, invoke_without_command=True)
@commands.has_permissions(manage_roles=True)  
async def role(ctx, user:discord.Member=None,*, role:discord.Role=None):
    if user is None or role is None:
        await bot.say('There was a error executing this command!\n**PROPER USAGE:** `e!role @user @role`')
        return
    if role in user.roles:
        await bot.remove_roles(user, role)
        await bot.say("<a:ElectroSuccess:656772759812046851> Changed roles for {}, -{}".format(user, role))
        return
    if role not in ctx.message.server.roles:
        await bot.say(f"There isn't any role named {role}.Please specify a valid role!")
        return
    else:
        await bot.add_roles(user, role)
        await bot.say("<a:ElectroSuccess:656772759812046851> Changed roles for {}, +{}".format(user, role))
        return
        
@bot.command(pass_context=True)
async def fortnite(ctx):
	await asyncio.sleep(1)
	await bot.say('<a:fortnite1:57116722369593365> <a:fortnite2:527116726249193472> <a:fortnite1:527116722369593365>')
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True)
async def hundred(ctx):
	await asyncio.sleep(1)
	await bot.say('<a:100:527116694506700819>')
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True)
async def party(ctx):
	await asyncio.sleep(1)
	await bot.say('<a:PartyGlasses:527116697791102977>')
	await bot.delete_message(ctx.message)	
	
@bot.command(pass_context=True)
async def dogdance(ctx):
	await asyncio.sleep(1)
	await bot.say('<a:dogdance:527116702580867092>')
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True)
async def hype(ctx):
	await asyncio.sleep(1)
	await bot.say('<a:DiscordHype:527116695253286933>')
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True, aliases=["Adib","ADib","ADIb","ADIB","adibhoque"])
async def adib(ctx):
	await bot.say('<a:NeonAdib:674927898100236308>')
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context = True)
async def help(ctx, page: str=None):
        if page is None:
            author = ctx.message.author
            await bot.send_message(ctx.message.channel, embed=helpm) 
        elif page == '1':
            help1 = discord.Embed(description='**[GENERAL COMMANDS](https://discord.gg/kuWVFpR)**', color = 0xFFBF00)
            help1.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/681510041790185561/ElectroHelp1.png')
            help1.set_author(name='ELECTRO',url='https://discord.gg/kuWVFpR', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
            help1.add_field(name = ':robot: Ping',value ='Returns ping lantency!\n> Usage: ``e!ping``\n> Aliases: `pong`,`lantency`',inline = False)
            help1.add_field(name = ':spy: Userinfo',value ='Shows info about user!\n> Usage: ``e!info @user``',inline = False)
            help1.add_field(name = '📊 Serverinfo',value ='Shows info about the server!\n> Usage: ``e!serverinfo``\n> Aliases: `serverstats`',inline = False)
            help1.add_field(name = '🛠 Ownerinfo',value ='Shows info about the bot owner!\n> Usage: ``e!ownerinfo``\n> Aliases: `developer`',inline = False)
            help1.add_field(name = '🗿 Avatar',value ='Shows avatar of the mentioned user!\n> Usage: ``e!avatar @user``\n> Aliases: `av`',inline = False)
            help1.add_field(name = '📈 Membercount',value ='Shows member count of the server!\n> Usage: ``e!membercount``\n> Aliases: `mc`',inline = False)
            help1.add_field(name = '🔗 Invite',value ='Sends bot invite link!\n> Usage: ``e!invite``\n> Aliases: `support`,`server`',inline = False)
            help1.add_field(name = '📤 Upvote',value ='Sends bot upvote link!\n> Usage: ``e!upvote``\n> Aliases: `vote`',inline = False)
            help1.add_field(name = '🇪 ElectroAvatar',value ='Claim your ELECTRO badge, a gift for using our bot!\n> Usage:`e!electroav` || `e!electroav <@user>`',inline = False)
            help1.add_field(name = '🎱 8ball',value ='Ask whatever you want!\n> Usage:`e!8ball [question]`',inline = False) 
            help1.add_field(name = '♋ Brilliance',value ='Generate your hypesquad brilliance badge!\n> Usage:`e!brilliance` || `e!brilliance <@user>`',inline = False) 
            help1.add_field(name = '♒ Balance',value ='Generate your hypesquad balance badge!\n> Usage:`e!balance` || `e!balance <@user>`',inline = False) 
            help1.add_field(name = '♌ Bravery',value ='Generate your hypesquad bravery badge!\n> Usage:`e!bravery` || `e!bravery <@user>`',inline = False) 
            help1.add_field(name = '🔢 Math',value ='Do all kinds of math in 1 command!\n> **Usage:** \n> Add: `e!math 69+69` || `e!math 69+69+69`\n> Deduct: `e!math 69-69` || `e!math 696-69-69`\n> Multiply: `e!math 3*3` || `e!math pi×4`\n> Divide: `e!math 10÷2` || `e!math 10/2`\n<:ElectroBookmark:668018207549816833> **[ADDITIONAL LINKS:](https://discord.gg/kuWVFpR)**\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)',inline = False)
            help1.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/656517276832366595/677936454202294272/ElectroGeneralBadge.png')
            help1.set_footer(text ='© 2020 ELECTRO, Inc.')
            await bot.send_message(ctx.message.author ,embed=help1)
            await bot.say('📨 Check Your DMs For General Commands!')
        elif page == '2':
            help2 = discord.Embed(description='**[MODERATION COMMANDS](https://discord.gg/kuWVFpR)**', color = 0xFFBF00)
            help2.set_author(name='ELECTRO',url='https://discord.gg/kuWVFpR', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
            help2.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/681510041471156226/ElectroHelp2.png')
            help2.add_field(name = '👞 Kick',value ='Kicks out mentioned user from the server!\n> Usage: ``e!kick @user``',inline = False)
            help2.add_field(name = '🔨 Ban',value ='Bans mentioned user from the server!\n> Usage: ``e!ban @user``',inline = False) 
            help2.add_field(name = '👒 Unban',value ='Unbans user from the server!\n> Usage: ``e!unban <User ID>``',inline = False) 
            help2.add_field(name = '🐵 Setnick',value ='Changes nickname of mentioned user!\n> Usage: ``e!setnick @user [new nickname]``',inline = False)
            help2.add_field(name = '🎯 Role',value ='Gives or removes role from mentioned user!\n> Usage: ``e!role @user @role``',inline = False)
            help2.add_field(name = '🎈 Say',value ='Make ELECTRO say anything you want!\n> Usage: ``e!say [your text]``',inline = False)
            help2.add_field(name = '🤼‍♀️ DM',value ='Make ELECTRO DM mentioned user anything you want!\n> Usage: ``e!dm @user [your text]``',inline = False) 
            help2.add_field(name = '🚫 English',value ='Softwarns mentioned user to talk in English!\n> Usage: ``e!english @user``',inline = False) 
            help2.add_field(name = '🗑 Purge',value ='Bulk deletes messages!\n> Usage: ``e!purge [amount]``',inline = False)
            help2.add_field(name = '🛢 RoleColor',value ='Give custom color to mentioned role!\n> Usage: ``e!rolecolor @role hexcode``',inline = False)
            help2.add_field(name = '⚡ SetupLogs',value ='Creates a log channel where electro posts some audit logs!\n> Usage: ``e!setuplogs``',inline = False)
            help2.add_field(name = '🔮 Embed',value ='Embeds your text!\n> Usage: ``e!embed [text]``',inline = False)
            help2.add_field(name = '🔒 Lockdown',value ='Locks the channel, only admins can chat after locking!\n> Usage: ``e!lockdown``',inline = False)
            help2.add_field(name = '🔓 Unlock',value ='Unlocks the channel for everyone to chat in!\n> Usage: ``e!unlock``',inline = False)
            help2.add_field(name = '🙂 Unbanall',value ='Unbans all the banned users!\n> Usage: ``e!unbanall``',inline = False)
            help2.add_field(name = '➕ Joinchannel',value ='Sets up the welcome image channel!\n> Usage: ``e!joinchannel [#channel]``',inline = False)
            help2.add_field(name = '➖ Leavechannel',value ='Sets up the goodbye image channel!\n> Usage: ``e!leavechannel [#channel]``',inline = False) 
            help2.add_field(name = '🔆 Testwelcomer',value ='Tests the welcome/goodbye image!\n> Usage: ``e!testwelcomer``',inline = False) 
            help2.add_field(name = '👋 Menro',value ='Mentions the role!\n> Usage: ``e!menro [role name]``',inline = False)
            help2.add_field(name = '🤐 Mute',value ='Mutes mentioned user from chatting in the server!\nUsage:``e!mute <@user>``',inline = False)
            help2.add_field(name = '😐 Unmute',value ='Unmutes mentioned user!\n> Usage:``e!unmute <@user>``\n<:ElectroBookmark:668018207549816833> **[ADDITIONAL LINKS:](https://discord.gg/kuWVFpR)**\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)',inline = False)
            help2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/656517276832366595/677936454470467617/ElectroModerationBadge.png')
            help2.set_footer(text ='© 2020 ELECTRO, Inc.')
            await bot.send_message(ctx.message.author ,embed=help2)
            await bot.say('📨 Check Your DMs For Moderation Commands!')
        elif page == '3':
            help3 = discord.Embed(description='**[FUN COMMANDS](https://discord.gg/kuWVFpR)**', color = 0xFFBF00)
            help3.set_author(name='ELECTRO',url='https://discord.gg/kuWVFpR', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
            help3.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/681510041228279813/ElectroHelp3.png')
            help3.add_field(name = 'Triggered',value ='Generate a triggered gif!\n**USAGE:**`e!triggered` || `e!triggered <@user>`',inline = False)
            help3.add_field(name = 'Love',value ='Detect love percentage between two users!\n**USAGE:**``e!love <@user> <@user>``',inline = False) 
            help3.add_field(name = 'Slap',value ='Slaps mentioned user!\n> Usage:``<e!slap @user>``',inline = False)
            help3.add_field(name = 'Kiss',value ='Kisses mentioned user!\> Usage:``<e!kiss @user>``',inline = False)
            help3.add_field(name = 'Hug',value ='Hugs mentioned user!\n> Usage:``e!hug <@user>``',inline = False)
            help3.add_field(name = 'Spank',value ='Spanks mentioned user!\n> Usage:``e!spank <@user>``',inline = False)
            help3.add_field(name = 'Cuddle',value ='Cuddles mentioned used!\n> Usage:``e!cuddle <@user>``',inline = False) 
            help3.add_field(name = 'Pat',value ='Pats mentioned user!\n> Usage:``e!pat <@user>``',inline = False) 
            help3.add_field(name = 'Tweet',value ='Generate a fake Twitter tweet!\n> Usage:``e!tweet [twitter name] [text]``',inline = False)
            help3.add_field(name = 'PhubComment',value ='Generate a fake Pornhub comment!\n> Usage:``e!phubcomment [text]``',inline = False)
            help3.add_field(name = 'Brazzers',value ='Generate a brazzers logo in users avatar!\n> Usage:`e!brazzers` || `e!brazzers <@user>`',inline = False)
            help3.add_field(name = 'Burn',value ='Get a user avatar on fire!\n> Usage:`e!burn` || `e!burn <@user>`',inline = False) 
            help3.add_field(name = 'Gay',value ='Make it look gay!\n> Usage:`e!gay` || `e!gay <@user>`',inline = False)
            help3.add_field(name = 'Missonpassed',value ='Generate a GTA mission passed stamp in user avatar!\n> Usage:`e!missionpassed` || `e!missionpassed <@user>`',inline = False) 
            help3.add_field(name = 'Thanos',value ='Snap mentioned users avatar!\n> Usage:`e!thanos` || `e!thanos <@user>`',inline = False) 
            help3.add_field(name = 'RIP',value ='Generate a rip image!\n> Usage:`e!rip` || `e!rip <@user>`',inline = False)  
            help3.add_field(name = 'Howgay',value ='Checks gayrate of mentioned user!\n> Usage:``e!howgay @user or e!howgay``',inline = False)
            help3.add_field(name = 'Magik',value ='Gives magik effect to users avatar!\n> Usage:``e!magik @user or e!magik``',inline = False)
            help3.add_field(name = 'Deepfry',value ='Gives deepfry effect to users avatar!\n> Usage:``e!deepfry @user or e!deepfry``',inline = False)
            help3.add_field(name = 'WhoWouldWin',value ='Sends a who would win image made with users avatars!\n> Usage:``e!whowouldwin @user1 @user2``',inline = False)
            help3.add_field(name = 'Captcha',value ='Does a fake recaptcha with users avatar!\n> Usage:`e!captcha <@user>` || `e!captcha`',inline = False)
            help3.add_field(name = 'IPhoneX',value ='Fits your avatar image in Iphone X!\n> Usage:`e!iphonex <@user>` || `e!iphonex`',inline = False)
            help3.add_field(name = 'Threats',value ='Does a threats meme with users avatar!\n> Usage:`e!threats <@user>` || `e!threats`',inline = False)
            help3.add_field(name = 'Clyde',value ='Make clyde say things in a image!\n> Usage:``e!clyde [text]``',inline = False)
            help3.add_field(name = 'Trash',value ='Make fun of users by trashing their avatar!\n> Usage:`e!trash <@user>` || `e!trash`',inline = False)
            help3.add_field(name = 'Meme',value ='Sends a random meme from Reddit!\n> Usage:`e!meme`\n<:ElectroBookmark:668018207549816833> **[ADDITIONAL LINKS:](https://discord.gg/kuWVFpR)**\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)' ,inline = False)
            help3.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/656517276832366595/677936454638370826/ElectroFunBadge.png')
            help3.set_footer(text ='© 2020 ELECTRO, Inc.') 
            await bot.send_message(ctx.message.author ,embed=help3)
            await bot.say('📨 Check Your DMs For Fun Commands!')
        elif page == '4':
            help4 = discord.Embed(description='**[MUSIC COMMANDS](https://discord.gg/kuWVFpR)**', color = 0xFFBF00) 
            help4.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/681510040644878396/ElectroHelp4.png')
            help4.add_field(name = '▶ Play',value ='Plays music from YouTube!\n> Usage:`e!play <music name> or <url>`',inline = False)
            help4.add_field(name = '🤷‍♀️ Skip',value ='Skips the current playing music!\n> Usage:`e!skip',inline = False)
            help4.add_field(name = '⏸ Stop',value ='Stops playing music and leaves the vc!\n> Usage:`e!stop` ',inline = False)
            help4.add_field(name = '🌍 NP',value ='Shows the now playing music!\n> Usage:`e!np`',inline = False)
            help4.add_field(name = '🎎 Queue',value ='Shows the music queue!\n> Usage:`e!queue`',inline = False)
            help4.add_field(name = '⏸ Pause',value ='Pauses the current playing song!\n> Usage:`e!pause`',inline = False)
            help4.add_field(name = '▶ Resume',value ='Resumes the current paused song!\n> Usage:`e!resume`',inline = False)
            help4.add_field(name = '🎚 Volume',value ='Change volume of the song!\n> Usage:`e!volume <1-200>`\n<:ElectroBookmark:668018207549816833> **[ADDITIONAL LINKS:](https://discord.gg/kuWVFpR)**\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)',inline = False)
            help4.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/656517276832366595/677936454869188608/ElectroMusicBadge.png')
            help4.set_footer(text ='© 2020 ELECTRO, Inc. | ADIB HOQUE#2212')
            await bot.send_message(ctx.message.author ,embed=help4)
            await bot.say('📨 Check Your DMs For Music Commands!')
        elif page == '5':
            help4 = discord.Embed(description='**[NSFW COMMANDS](https://discord.gg/kuWVFpR)**\n**REQUIRED:** A NSFW marked channel.', color = 0xFFBF00) 
            help4.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/681510040372379688/ElectroHelp5.png')
            help4.add_field(name = '<:boobs:686604888011964480> Boobs',value ='Image of women boobs!\n> Usage: `e!boobs`',inline = False)
            help4.add_field(name = '<:pussy:686603137796014281> Pussy',value ='Image of women vagina!\n> Usage: `e!pussy`',inline = False)
            help4.add_field(name = '<:ass:686604800930086990> Ass',value ='Image of women ass!\n> Usage: `e!ass`',inline = False)
            help4.add_field(name = '<:thighs:686601878867673100> Thighs',value ='Image of women thighs!\n> Usage: `e!thigh` ',inline = False)
            help4.add_field(name = '▶ Porngif',value ='A porn gif!\n> Usage: `e!porngif`',inline = False)
            help4.add_field(name = '🎦 4k',value ='Ultra HD(4k) porn image!\n> Usage: `e!4k`',inline = False)
            help4.add_field(name = '<:doggy:686601370043940921> Anal',value ='Image/gif of anal sex!\n> Usage: `e!anal`',inline = False)
            help4.add_field(name = '<:hentai:686601945330614289> Hentai',value ='Everyones favorite Hentai gifs & images!\n> Usage: `e!hentai`',inline = False)
            help4.add_field(name = '<:doggy:686601370043940921> Hentaianal',value ='Hentai image/gif of anal sex!\n> Usage:`e!hentaianal`',inline = False)
            help4.add_field(name = '<:thighs:686601878867673100> Hentaithigh',value ='Hentai women thighs!\n> Usage: `e!hentaithigh`',inline = False)
            help4.add_field(name = '<:hentaineko:686601982546673684> Hentaineko',value ='Hentai character neko(catgirl) images!\n> Usage: `e!hentaineko`',inline = False)
            help4.add_field(name = '<:hentaikitsune:686602019808739338> Hentaikitsune',value ='Hentai character kitsune images!\n> Usage: `e!hentaikitsune`\n<:ElectroBookmark:668018207549816833> **[ADDITIONAL LINKS:](https://discord.gg/kuWVFpR)**\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)',inline = False)
            help4.set_thumbnail(url ='https://cdn.discordapp.com/attachments/656517276832366595/680674342731907072/ElectroNSFWBadge.png')
            help4.set_footer(text ='© 2020 ELECTRO, Inc. | ADIB HOQUE#2212')
            await bot.send_message(ctx.message.author ,embed=help4)
            await bot.say('📨 Check Your DMs For NSFW Commands!')
        else:
            Return
		
@bot.command(pass_context = True, aliases=['help 1','help_1'] )
async def help1(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(description='**[GENERAL COMMANDS](https://discord.gg/kuWVFpR)**', color = 0xFFBF00)
    embed.set_author(name='ELECTRO',url='https://discord.gg/kuWVFpR', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/656760777973432330/ELECTRO_HELP1.gif')
    embed.add_field(name = 'Ping',value ='Returns ping lantency!\n**USAGE:**``e!ping``',inline = False)
    embed.add_field(name = 'Userinfo',value ='Shows info about mentioned user!\n**USAGE:**``e!userinfo @user``',inline = False)
    embed.add_field(name = 'Serverinfo',value ='Shows info about the server!\n**USAGE:**``e!serverinfo``',inline = False)
    embed.add_field(name = 'Ownerinfo',value ='Shows info about the bot owner!\n**USAGE:**``e!ownerinfo``',inline = False)
    embed.add_field(name = 'Avatar',value ='Shows avatar of the mentioned user!\n**USAGE:**``e!avatar @user``',inline = False)
    embed.add_field(name = 'Membercount',value ='Shows member count of the server!\n**USAGE:**``e!membercount``',inline = False)
    embed.add_field(name = 'Invite',value ='Sends bot invite link!\n**USAGE:**``e!invite``',inline = False)
    embed.add_field(name = 'Upvote',value ='Sends bot upvote link!\n**USAGE:**``e!upvote``',inline = False)
    embed.add_field(name = 'Emoji',value ='Sends url of the emoji!\n**USAGE:**``e!emoji :emoji: ``\n<:ElectroBookmark:668018207549816833> **Additional Links:**\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)',inline = False)
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/656517276832366595/677936454202294272/ElectroGeneralBadge.png')
    embed.set_footer(text ='© 2020 ELECTRO, Inc.')
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For General Commands!')
    
@bot.command(pass_context = True)
async def help2(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(description='**[MODERATION COMMANDS](https://discord.gg/kuWVFpR)**', color = 0xFFBF00)
    embed.set_author(name='ELECTRO',url='https://discord.gg/kuWVFpR', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/656760817852874752/ELECTRO_HELP2.gif')
    embed.add_field(name = 'Kick',value ='Kicks out mentioned user from the server!\n**USAGE:**``e!kick @user``',inline = False)
    embed.add_field(name = 'Ban',value ='Bans mentioned user from the server!\n**USAGE:**``e!ban @user``',inline = False) 
    embed.add_field(name = 'Unban',value ='Unbans user from the server!\n**USAGE:**``e!unban <User ID>``',inline = False) 
    embed.add_field(name = 'Setnick',value ='Changes nickname of mentioned user!\n**USAGE:**``e!setnick @user [new nickname]``',inline = False)
    embed.add_field(name = 'Role',value ='Gives or removes role from mentioned user!\n**USAGE:**``e!role @user @role``',inline = False)
    embed.add_field(name = 'Say',value ='Make ELECTRO say anything you want!\n**USAGE:**``e!say [your text]``',inline = False)
    embed.add_field(name = 'DM',value ='Make ELECTRO DM mentioned user anything you want!\n**USAGE:**``e!dm @user [your text]``',inline = False) 
    embed.add_field(name = 'English',value ='Softwarns mentioned user to talk in English!\n**USAGE:**``e!english @user``',inline = False) 
    embed.add_field(name = 'Purge',value ='Bulk deletes messages!\n**USAGE:**``e!purge [amount]``',inline = False)
    embed.add_field(name = 'RoleColor',value ='Give custom color to mentioned role!\n**USAGE:**``e!rolecolor @role hexcode``',inline = False)
    embed.add_field(name = 'SetupLogs',value ='Creates a log channel where electro posts some audit ligs!\n**USAGE:**``e!setuplogs``',inline = False)
    embed.add_field(name = 'Embed',value ='Embeds your text!\n**USAGE:**``e!embed [text]``',inline = False)
    embed.add_field(name = 'Lockdown',value ='Locks the channel, only admins can chat after locking!\n**USAGE:**``e!lockdown``',inline = False)
    embed.add_field(name = 'Unlock',value ='Unlocks the channel for everyone to chat in!\n**USAGE:**``e!unlock``',inline = False)
    embed.add_field(name = 'Unbanall',value ='Unbans all the banned users!\n**USAGE:**``e!unbanall``',inline = False)
    embed.add_field(name = 'Menro',value ='Mentions the role!\n**USAGE:**``e!menro [role name]``',inline = False)
    embed.add_field(name = 'Mute',value ='Mutes mentioned user from chatting in the server!\n**USAGE:**``e!mute <@user>``',inline = False)
    embed.add_field(name = 'Unmute',value ='Unmutes mentioned user!\n**USAGE:**``e!unmute <@user>``\n<:ElectroBookmark:668018207549816833> **Additional Links:**\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)',inline = False)
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/656517276832366595/677936454470467617/ElectroModerationBadge.png')
    embed.set_footer(text ='© 2020 ELECTRO, Inc.')
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Moderation Commands!') 
    
@bot.command(pass_context = True)
async def help3(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(description='**[FUN COMMANDS](https://discord.gg/kuWVFpR)**', color = 0xFFBF00)
    embed.set_author(name='ELECTRO',url='https://discord.gg/kuWVFpR', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/656760847917514775/ELECTRO_HELP3.gif')
    embed.add_field(name = 'Joke',value ='Sends a random joke!\n**USAGE:**``e!joke``',inline = False)
    embed.add_field(name = 'Love',value ='Detect love percentage between two users!\n**USAGE:**``e!love @user @user``',inline = False) 
    embed.add_field(name = 'Slap',value ='Slaps mentioned user!\n**USAGE:**``e!slap @user``',inline = False)
    embed.add_field(name = 'Kiss',value ='Kisses mentioned user!\n**USAGE:**``e!kiss @user``',inline = False)
    embed.add_field(name = 'Hug',value ='Hugs mentioned user!\n**USAGE:**``e!hug @user``',inline = False)
    embed.add_field(name = 'Virgin',value ='ELECTRO checks virginity of mentioned user!\n**USAGE:**``e!virgin @user``',inline = False)
    embed.add_field(name = 'Gender',value ='ELECTRO detects gender of mentioned user!\n**USAGE:**``e!gender @user``',inline = False) 
    embed.add_field(name = 'Tweet',value ='Make a fake twitter tweet!\n**USAGE:**``e!tweet [twitter name] [text]``',inline = False) 
    embed.add_field(name = 'Rolldice',value ='ELECTRO rolls dice and sends random number 1-6!\n**USAGE:**``e!rolldice``',inline = False)
    embed.add_field(name = 'Flipcoin',value ='ELECTRO flips coin!\n**USAGE:**``e!flipcoin``',inline = False)
    embed.add_field(name = 'Howgay',value ='Checks gayrate of mentioned user!\n**USAGE:**``e!howgay @user or e!howgay``',inline = False)
    embed.add_field(name = 'Magik',value ='Gives magik effect to users avatar!\n**USAGE:**``e!magik @user or e!magik``',inline = False)
    embed.add_field(name = 'Deepfry',value ='Gives deepfry effect to users avatar!\n**USAGE:**``e!deepfry @user or e!deepfry``',inline = False)
    embed.add_field(name = 'WhoWouldWin',value ='Sends a who would win image made with users avatars!\n**USAGE:**``e!whowouldwin @user1 @user2``',inline = False)
    embed.add_field(name = 'Captcha',value ='Does a fake recaptcha with users avatar!\n**USAGE:**``e!captcha @user or e!captcha``',inline = False)
    embed.add_field(name = 'IPhoneX',value ='Fits your avatar image in Iphone X!\n**USAGE:**``e!iphonex @user or e!iphonex``',inline = False)
    embed.add_field(name = 'Threats',value ='Does a threats meme with users avatar!\n**USAGE:**``e!threats @user or e!threats``',inline = False)
    embed.add_field(name = 'Clyde',value ='Make clyde say things in a image!\n**USAGE:**``e!clyde [text]``',inline = False)
    embed.add_field(name = 'Trash',value ='Make fun of users by trashing their avatar!\n**USAGE:**``e!trash @user or e!trash``',inline = False)
    embed.add_field(name = 'Meme',value ='Sends a random meme from Reddit!\n**USAGE:**``e!meme``\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)' ,inline = False)
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/656517276832366595/677936454638370826/ElectroFunBadge.png')
    embed.set_footer(text ='© 2020 ELECTRO, Inc.')
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Fun Commands!')   
    
@bot.command(pass_context = True)
async def help4(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(description='**[MUSIC COMMANDS](https://discord.gg/kuWVFpR)**', color = 0xFFBF00) 
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/656760860085321748/ELECTRO_HELP4.gif')
    embed.add_field(name = 'Play',value ='Plays music from YouTube!\n**USAGE:**`e!play <music name> or <url>`',inline = False)
    embed.add_field(name = 'Skip',value ='Skips the current playing music!\n**USAGE:**`e!skip',inline = False)
    embed.add_field(name = 'Stop',value ='Stops playing music and leaves the vc!\n**USAGE:**`e!stop` ',inline = False)
    embed.add_field(name = 'NP',value ='Shows the now playing music!\n**USAGE:**`e!np`',inline = False)
    embed.add_field(name = 'Queue',value ='Shows the music queue!\n**USAGE:**`e!queue`',inline = False)
    embed.add_field(name = 'Pause',value ='Pauses the current playing song!\n**USAGE:**`e!pause`',inline = False)
    embed.add_field(name = 'Resume',value ='Resumes the current paused song!\n**USAGE:**`e!resume`',inline = False)
    embed.add_field(name = 'Volume',value ='Change volume of the song!\n**USAGE:**`e!volume <1-200>`\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)',inline = False)
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/656517276832366595/677936454869188608/ElectroMusicBadge.png')
    embed.set_footer(text ='© 2020 ELECTRO, Inc.')
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Music Commands!')    

@bot.command(pass_context = True)
@commands.check(is_owner)
async def dmserver(ctx, *, msg: str):
    for server_member in ctx.message.server.members:
    	await bot.send_message(server_member, msg)
        
@bot.command(pass_context = True)
async def rolecolor(ctx, role:discord.Role=None, value:str=None):
    if discord.utils.get(ctx.message.server.roles, name="{}".format(role)) is None:
        await bot.say("Please specify a valid role!")
        return
    if value is None:
        await bot.say("Please specify a color hex code!")
        return
    if ctx.message.author.server_permissions.manage_roles == False:
        await bot.say('**You do not have permission to use this command!**')
        return
    else:
        new_val = value.replace("#", "")
        colour = '0x' + new_val
        colo = '0x' + value
        user = ctx.message.author
        await bot.edit_role(ctx.message.server, role, color = discord.Color(int(colour, base=16)))
        embed=discord.Embed(description="<:ElectroSucess:527118398753079317> {} ROLE COLOR HAS BEEN CHANGED!".format(role.mention), color=0x429CFF)
        await bot.say(embed=embed) 
        
@bot.command(pass_context = True)
async def rolecolour(ctx, role:discord.Role=None, value:str=None):
    if discord.utils.get(ctx.message.server.roles, name="{}".format(role)) is None:
        await bot.say("Please specify a valid role!")
        return
    if value is None:
        await bot.say("Please specify a color hex code!")
        return
    if ctx.message.author.server_permissions.manage_roles == False:
        await bot.say('**You do not have permission to use this command!**')
        return
    else:
        new_val = value.replace("#", "")
        colo = '0x' + value
        colour = '0x' + new_val
        user = ctx.message.author
        await bot.edit_role(ctx.message.server, role, color = discord.Color(int(colour, base=16)))
        embed=discord.Embed(description="<:ElectroSucess:527118398753079317> {} ROLE COLOR HAN BEEN CHANGED!".format(role.mention), color=0x429CFF)
        await bot.say(embed=embed) 
    			
@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unbanall(ctx):
    if ctx.message.author.bot:
      return
    else:
      server=ctx.message.server
      ban_list=await bot.get_bans(server)
      channel = ctx.message.channel
      embed=discord.Embed(description="<a:ElectroSuccess:656772759812046851> Unbanning {} Users!".format(len(ban_list)), color=0xFFBF00)
      await bot.send_message(channel, embed=embed)
      for member in ban_list:
      	await bot.unban(server,member)
  
@bot.command(pass_context = True)
@commands.has_permissions(administrator=True) 
async def embed(ctx, channel: discord.Channel=None, *, msg: str):
	embed=discord.Embed(description="{}".format(msg), color=0xFFBF00)
	await bot.send_message(channel, embed=embed)
	await bot.delete_message(ctx.message)

@bot.command(pass_context = True)
@commands.has_permissions(manage_messages=True) 
async def poll(ctx, *, msg: str):
        embed=discord.Embed(title="<:ElectroPoll:689859743141068871> POLL",description="{}".format(msg), color=0xFFBF00)
        m = await bot.send_message(ctx.message.channel, embed=embed)
        await bot.delete_message(ctx.message)
        up = ':ElectroThumbsUp:689855938320007226'
        down = ':ElectroThumbsDown:689855969945321523'
        await bot.add_reaction(m, up)
        await bot.add_reaction(m, down)

@bot.command(pass_context = True)
@commands.has_permissions(administrator=True) 
async def announce(ctx, channel: discord.Channel=None, *, msg: str):
	embed=discord.Embed(title="ANNOUNCEMENT", description="{}".format(msg), color=0xFFBF00)
	embed.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
	embed.set_thumbnail(url=ctx.message.server.icon_url)
	embed.timestamp = datetime.datetime.utcnow()
	await bot.send_message(channel, embed=embed)
	await bot.delete_message(ctx.message)
      
@bot.command(pass_context = True)
@commands.has_permissions(kick_members=True) 
async def lockdown(ctx, channelname: discord.Channel=None):
    overwrite = discord.PermissionOverwrite(send_messages=False, read_messages=True)
    if not channelname:
        role = discord.utils.get(ctx.message.server.roles, name='@everyone')
        await bot.edit_channel_permissions(ctx.message.channel, role, overwrite)
        await bot.say("<a:ElectroSuccess:656772759812046851>**Channel Locked**\nUse `e!unlock` to unlock it!")
    else:
        role = discord.utils.get(ctx.message.server.roles, name='@everyone')
        await bot.edit_channel_permissions(channelname, role, overwrite)
        await bot.say("<a:ElectroSuccess:656772759812046851>**Channel Locked**\nUse `e!unlock` to unlock it!")
	
@bot.command(pass_context = True)
@commands.has_permissions(kick_members=True) 
async def unlock(ctx, channelname: discord.Channel=None):
    overwrite = discord.PermissionOverwrite(send_messages=None, read_messages=True)
    if not channelname:
        role = discord.utils.get(ctx.message.server.roles, name='@everyone')
        await bot.edit_channel_permissions(ctx.message.channel, role, overwrite)
        await bot.say("<a:ElectroSuccess:656772759812046851>**Channel Unlocked**\nUse `e!lockdown` to lock it!")
    else:
        role = discord.utils.get(ctx.message.server.roles, name='@everyone')
        await bot.edit_channel_permissions(channelname, role, overwrite)
        await bot.say("<a:ElectroSuccess:656772759812046851>**Channel Unlocked**\nUse `e!lockdown` to lock it!")
       	
@bot.event
async def on_message_edit(before, after):
    if before.content == after.content:
      return
    if before.author == bot.user:
      return
    else:
      user = before.author
      member = after.author
      for channel in user.server.channels:
        if channel.name == '⚡electro-logs':
            logchannel = channel 
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(title = "MESSAGE EDITED", color = 0xFFBF00)
            embed.add_field(name = 'Message Author:',value ='{}'.format(user),inline = False)
            embed.add_field(name = 'Before:',value ='{}'.format(before.content),inline = False)
            embed.add_field(name = 'After:',value ='{}'.format(after.content),inline = False)
            embed.add_field(name = 'Channel:',value ='{0}\n[Jump To Message](https://discordapp.com/channels/{1}/{2}/{3})'.format(before.channel.mention, before.server.id, before.channel.id, before.id),inline = False)
            embed.set_thumbnail(url=user.server.icon_url) 
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text ='MESSAGE EDITED')
            await bot.send_message(logchannel, embed=embed)
         
@bot.event
async def on_reaction_add(reaction, user):
	if user != bot.user:
                if reaction.emoji.id == '666202936929681418':
                                embed = discord.Embed(description='**[GENERAL COMMANDS](https://discord.gg/kuWVFpR)**', color = 0xFFBF00)
                                embed.set_author(name='ELECTRO',url='https://discord.gg/kuWVFpR', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
                                embed.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/656760777973432330/ELECTRO_HELP1.gif')
                                embed.add_field(name = 'Ping',value ='Returns ping lantency!\n**USAGE:**``e!ping``',inline = False)
                                embed.add_field(name = 'Userinfo',value ='Shows info about mentioned user!\n**USAGE:**``e!userinfo @user``',inline = False)
                                embed.add_field(name = 'Serverinfo',value ='Shows info about the server!\n**USAGE:**``e!serverinfo``',inline = False)
                                embed.add_field(name = 'Ownerinfo',value ='Shows info about the bot owner!\n**USAGE:**``e!ownerinfo``',inline = False)
                                embed.add_field(name = 'Avatar',value ='Shows avatar of the mentioned user!\n**USAGE:**``e!avatar @user``',inline = False)
                                embed.add_field(name = 'Membercount',value ='Shows member count of the server!\n**USAGE:**``e!membercount``',inline = False)
                                embed.add_field(name = 'Invite',value ='Sends bot invite link!\n**USAGE:**``e!invite``',inline = False)
                                embed.add_field(name = 'Upvote',value ='Sends bot upvote link!\n**USAGE:**``e!upvote``',inline = False)
                                embed.add_field(name = 'Emoji',value ='Sends url of the emoji!\n**USAGE:**``e!emoji :emoji: ``\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)',inline = False)
                                await bot.send_message(user, embed=embed)
                if reaction.emoji.id == '666920202818027531':
                                embed = discord.Embed(description='**[MODERATION COMMANDS](https://discord.gg/kuWVFpR)**', color = 0xFFBF00)
                                embed.set_author(name='ELECTRO',url='https://discord.gg/kuWVFpR', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
                                embed.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/656760817852874752/ELECTRO_HELP2.gif')
                                embed.add_field(name = 'Kick',value ='Kicks out mentioned user from the server!\n**USAGE:**``e!kick @user``',inline = False)
                                embed.add_field(name = 'Ban',value ='Bans mentioned user from the server!\n**USAGE:**``e!ban @user``',inline = False)
                                embed.add_field(name = 'Unban',value ='Unbans user from the server!\n**USAGE:**``e!unban <User ID>``',inline = False)
                                embed.add_field(name = 'Setnick',value ='Changes nickname of mentioned user!\n**USAGE:**``e!setnick @user [new nickname]``',inline = False)
                                embed.add_field(name = 'Role',value ='Gives or removes role from mentioned user!\n**USAGE:**``e!role @user @role``',inline = False)
                                embed.add_field(name = 'Say',value ='Make ELECTRO say anything you want!\n**USAGE:**``e!say [your text]``',inline = False)
                                embed.add_field(name = 'DM',value ='Make ELECTRO DM mentioned user anything you want!\n**USAGE:**``e!dm @user [your text]``',inline = False)
                                embed.add_field(name = 'English',value ='Softwarns mentioned user to talk in English!\n**USAGE:**``e!english @user``',inline = False)
                                embed.add_field(name = 'Purge',value ='Bulk deletes messages!\n**USAGE:**``e!purge [amount]``',inline = False)
                                embed.add_field(name = 'RoleColor',value ='Give custom color to mentioned role!\n**USAGE:**``e!rolecolor @role hexcode``',inline = False)
                                embed.add_field(name = 'SetupLogs',value ='Creates a log channel where electro posts some audit ligs!\n**USAGE:**``e!setuplogs``',inline = False)
                                embed.add_field(name = 'Embed',value ='Embeds your text!\n**USAGE:**``e!embed [text]``',inline = False)
                                embed.add_field(name = 'Lockdown',value ='Locks the channel, only admins can chat after locking!\n**USAGE:**``e!lockdown``',inline = False)
                                embed.add_field(name = 'Unlock',value ='Unlocks the channel for everyone to chat in!\n**USAGE:**``e!unlock``',inline = False)
                                embed.add_field(name = 'Unbanall',value ='Unbans all the banned users!\n**USAGE:**``e!unbanall``',inline = False)
                                embed.add_field(name = 'Menro',value ='Mentions the role!\n**USAGE:**``e!menro [role name]``',inline = False)
                                embed.add_field(name = 'Mute',value ='Mutes mentioned user from chatting in the server!\n**USAGE:**``e!mute <@user>``',inline = False)
                                embed.add_field(name = 'Unmute',value ='Unmutes mentioned user!\n**USAGE:**``e!unmute <@user>``\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)',inline = False)
                                await bot.edit_message(reaction.message, embed=embed)
                else:
                                for channel in user.server.channels:
                                        if channel.name == '⚡electro-logs':
                                                logchannel = channel
                                                r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
                                                embed = discord.Embed(title = "REACTION ADDED", color = 0xFFBF00)
                                                embed.add_field(name = 'Reaction by:',value ='{}'.format(user),inline = False)
                                                embed.add_field(name = 'Message:',value ='{}'.format(reaction.message.content),inline = False)
                                                embed.add_field(name = 'Channel:',value ='{}'.format(reaction.message.channel.mention),inline = False)
                                                embed.add_field(name = 'Emoji:',value ='{}'.format(reaction.emoji),inline = False)
                                                embed.set_thumbnail(url=reaction.message.server.icon_url)
                                                embed.timestamp = datetime.datetime.utcnow()
                                                embed.set_footer(text ='REACTION ADDED')
                                                await bot.send_message(logchannel, embed=embed)
        
@bot.event
async def on_reaction_remove(reaction, user):
  for channel in user.server.channels:
    if channel.name == '⚡electro-logs':
        logchannel = channel
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title = "REACTION REMOVED", color = 0xFFBF00)
        embed.add_field(name = 'Reaction by:',value ='{}'.format(user),inline = False)
        embed.add_field(name = 'Message:',value ='{}'.format(reaction.message.content),inline = False)
        embed.add_field(name = 'Channel:',value ='{}'.format(reaction.message.channel.mention),inline = False)
        embed.add_field(name = 'Emoji:',value ='{}'.format(reaction.emoji),inline = False)
        embed.set_thumbnail(url=reaction.message.server.icon_url) 
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text ='REACTION REMOVED')
        await bot.send_message(logchannel, embed=embed)   
        
@bot.event
async def on_message(message):
	if not message.author.bot:
		await bot.process_commands(message)
	if '<@496978159724396545>' in message.content:
		emoji = 'a:NeonAdib:674927898100236308'
		await bot.add_reaction(message, emoji) 
		channe = bot.get_channel('656535174548553730')
	if message.server is None and message.author != bot.user:
                electrosucess = 'a:ElectroSuccess:656772759812046851'
                await bot.add_reaction(message, electrosucess)
                embed=discord.Embed(title="{}".format(message.author), description="{}".format(message.content), color = 0xFFBF00)
                embed.set_thumbnail(url= message.author.avatar_url)
                embed.set_image(url = message.discord.Attachment_url)
                await bot.send_message(bot.get_channel('656535174548553730'), '{} ID: {}'.format(message.author, message.author.id))
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text ='ELECTRO MAIL', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
                await bot.send_message(bot.get_channel('656535174548553730'), embed=embed)    	 
    	 
@bot.event
async def on_member_unban(server, user):
	for channel in user.guild.channels:
		if channel.name == '⚡electro-logs':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(title = "USER UNBANNED", color = 0xFFBF00)
			embed.add_field(name = 'User Name:',value ='{}'.format(user.name),inline = False)
			embed.add_field(name = 'User ID:',value ='{}'.format(user.id),inline = False)
			await bot.send_message(logchannel,  embed=embed)
			
@bot.event
async def on_member_ban(guild, user):
	for channel in user.guild.channels:
		if channel.name == '⚡electro-logs':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(title = "USER BANNED", color = 0xFFBF00)
			embed.add_field(name = 'User Name:',value ='{}'.format(user.name),inline = False)
			embed.add_field(name = 'User ID:',value ='{}'.format(user.id),inline = False)
			await bot.send_message(logchannel,  embed=embed)	
			
@bot.event
async def on_message_delete(message):
    if not message.author.bot:
      channelname = '⚡electro-logs'
      logchannel=None
      for channel in message.server.channels:
        if channel.name == channelname:
          user = message.author
      for channel in message.author.server.channels:
        if channel.name == '⚡electro-logs':
          logchannel = channel
          r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
          embed = discord.Embed(title = "MESSAGE DELETED", color = 0xFFBF00)
          embed.add_field(name = 'User: **{0}**'.format(user),value ='User ID: **{}**'.format(user.id),inline = False)
          embed.add_field(name = 'Message:',value ='{}'.format(message.content),inline = False)
          embed.add_field(name = 'Channel:',value ='{}'.format(message.channel.mention),inline = False)
          embed.set_thumbnail(url=message.server.icon_url)
          embed.timestamp = datetime.datetime.utcnow()
          embed.set_footer(text ='MESSAGE DELETED')
          await bot.send_message(logchannel,  embed=embed)
			
@bot.event
async def on_server_join(server):
	channel = bot.get_channel('656536432500015186')
	r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
	embed = discord.Embed(title="IM IN A NEW SERVER", color = 0xFFBF00)
	embed.add_field(name = 'Server Name:',value ='{}'.format(server.name),inline = False)
	embed.add_field(name = 'Membercount:',value ='{}'.format(str(server.member_count)),inline = False)
	embed.set_thumbnail(url = server.icon_url)
	embed.set_footer(text ='Type e!invite for invite link!')
	await bot.send_message(channel, embed=embed)		
			
@bot.event
async def on_server_remove(server):
		channel = bot.get_channel('656536492977553438')
		r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
		embed = discord.Embed(title="I WAS REMOVED FROM A SERVER", color = 0xFFBF00)
		embed.add_field(name = 'Server Name:',value ='{}'.format(server.name),inline = False)
		embed.add_field(name = 'Membercount:',value ='{}'.format(str(server.member_count)),inline = False)
		embed.set_thumbnail(url = server.icon_url)
		embed.set_footer(text ='Type e!invite for invite link!')
		await bot.send_message(channel,  embed=embed)
			
@bot.event
async def on_server_role_create(role, server):
	for channel in role.server.channels:
		if channel.name == '⚡electro-logs':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
			embed.set_author(name='ROLE CREATED')
			embed.add_field(name = 'Role Name:',value ='{}'.format(role.name),inline = False)
			embed.add_field(name = 'Role ID:',value ='{}'.format(role.id),inline = False)
			await bot.send_message(logchannel,  embed=embed)
			
@bot.event
async def on_server_role_delete(role, server):
	for channel in role.server.channels:
		if channel.name == '⚡electro-logs':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(title = 'ROLE CREATED', color = discord.Color((r << 16) + (g << 8) + b))
			embed.set_author(name='ROLE CREATED')
			embed.add_field(name = 'Role Name:',value ='{}'.format(role.name),inline = False)
			embed.add_field(name = 'Role ID:',value ='{}'.format(role.id),inline = False)
			await bot.send_message(logchannel,  embed=embed)	
			
@bot.event
async def on_server_channel_create(channel, server):
	for channel in channel.server.channels:
		if channel.name == '⚡electro-logs':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
			embed.set_author(name='CHANNEL CREATED')
			embed.add_field(name = 'Channel Name:',value ='{}'.format(channel.name),inline = False)
			embed.add_field(name = 'Channel ID:',value ='{}'.format(channel.id),inline = False)
			embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
			await bot.send_message(logchannel,  embed=embed)								
								 
@bot.command(pass_context = True)
@commands.has_permissions(administrator=True) 
async def setuplog(ctx):
    server = ctx.message.guild
    everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
    everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
    await bot.create_channel(server, '⚡electro-logs', everyone)
    await bot.say("<a:ElectroSuccess:656772759812046851> **LOG CHANNEL CREATED!**\nDon't rename it or it won't work!'")
								 
@bot.command(pass_context=True)
async def magik(ctx, user: discord.Member=None):
	if user is None:
		url = f"https://nekobot.xyz/api/imagegen?type=magik&image={ctx.message.author.avatar_url}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)
	else:
		url = f"https://nekobot.xyz/api/imagegen?type=magik&image={user.avatar_url}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)
				
@bot.command(pass_context=True)
async def captcha(ctx, user: discord.Member=None):
	if user is None:
		url = f"https://nekobot.xyz/api/imagegen?type=captcha&url={ctx.message.author.avatar_url}&username={ctx.message.author.name}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)
	else:
		url = f"https://nekobot.xyz/api/imagegen?type=captcha&url={user.avatar_url}&username={user.name}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)
				
@bot.command(pass_context=True)
async def deepfry(ctx, user: discord.Member=None):
	if user is None:
		url = f"https://nekobot.xyz/api/imagegen?type=deepfry&image={ctx.message.author.avatar_url}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)
	else:
		url = f"https://nekobot.xyz/api/imagegen?type=deepfry&image={user.avatar_url}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)
				
@bot.command(pass_context=True)
async def whowouldwin(ctx, user1: discord.Member, *, user2:discord.Member):
	if user2 is None:
		url = f"https://nekobot.xyz/api/imagegen?type=whowouldwin&user1={user1.avatar_url}&user2={user1.avatar_url}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)
	else:
		url = f"https://nekobot.xyz/api/imagegen?type=whowouldwin&user1={user1.avatar_url}&user2={user2.avatar_url}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)

@bot.command(pass_context=True)
async def iphonex(ctx, user: discord.Member=None):
	if user is None:
		url = f"https://nekobot.xyz/api/imagegen?type=iphonex&url={ctx.message.author.avatar_url}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)
	else:
		url = f"https://nekobot.xyz/api/imagegen?type=iphonex&url={user.avatar_url}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)  	

@bot.command(pass_context=True)
async def trash(ctx, user: discord.Member=None):
	if user is None:
		url = f"https://nekobot.xyz/api/imagegen?type=trash&url={ctx.message.author.avatar_url}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)
	else:
		url = f"https://nekobot.xyz/api/imagegen?type=trash&url={user.avatar_url}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)
				
@bot.command(pass_context=True)
async def threats(ctx, user: discord.Member=None):
	if user is None:
		url = f"https://nekobot.xyz/api/imagegen?type=threats&image={ctx.message.author.avatar_url}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)
	else:
		url = f"https://nekobot.xyz/api/imagegen?type=threats&image={user.avatar_url}"
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as r:
				res = await r.json()
				r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
				embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
				embed.set_image(url=res['message'])
				await bot.say(embed=embed)
				
@bot.command(pass_context=True)
async def clyde(ctx, *, msg:str):
	url = f"https://nekobot.xyz/api/imagegen?type=clyde&text={msg}"
	async with aiohttp.ClientSession() as cs:
		async with cs.get(url) as r:
			res = await r.json()
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
			embed.set_image(url=res['message'])
			await bot.say(embed=embed)
@bot.command(pass_context=True)
async def phcomment(ctx, *, msg:str):
        url = f"https://nekobot.xyz/api/imagegen?type=phcomment&image={ctx.message.author.avatar_url}&text={msg}&username={ctx.message.author.name}" 
        async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://nekobot.xyz/api/imagegen?type=phcomment"
                                  f"&image={ctx.message.author.avatar_url}"
                                  f"&text={msg}&username={ctx.message.author.name}") as r:
                        res = await r.json()
                        embed = discord.Embed(color=0xFFBF00)
                        embed.set_image(url=res['message'])
                        await bot.say(embed=embed)
				 
@bot.command(pass_context = True)
@commands.has_permissions(kick_members=True) 
async def mute(ctx, member: discord.Member=None):
	if member is None:
		await bot.say('<a:ElectroFail:656772856184832025> **PLEASE SPECIFY A USER TO MUTE!**')
	if member.server_permissions.kick_members:
		await bot.say("<a:ElectroFail:656772856184832025> **THAT USER IS A MOD/ADMIN, I CAN'T DO THAT!**")
	if discord.utils.get(member.server.roles, name='Muted') is None:
		await bot.say('<a:ElectroFail:656772856184832025> **NO MUTED ROLE FOUND**')
	else:
		role = discord.utils.get(member.server.roles, name='Muted')
		await bot.add_roles(member, role)
		await bot.say("<a:ElectroSuccess:656772759812046851> **{} WAS MUTED!**".format(member.name))
		await bot.send_message(member, "You were muted by **{0}** from **{1}**!".format(ctx.message.author, ctx.message.server.name))
 
@bot.command(pass_context = True)
@commands.has_permissions(kick_members=True) 
async def unmute(ctx, member: discord.Member=None):
    if member is None:
      await bot.say('<a:ElectroSuccess:656772759812046851> **PLEASE SPECIFY A USER TO UNMUTE!**')
    if ctx.message.author.bot:
      return
    else:
      role = discord.utils.get(member.server.roles, name='Muted')
      await bot.remove_roles(member, role)
      await bot.say("<a:ElectroSuccess:656772759812046851> **{} WAS UNMUTED!**".format(member))
      
@commands.group(invoke_without_command=True)
async def invoice(ctx):
	await bot.say("`e!invoice sponsor/role/channel/cc/membership @buyer price`")

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def sponsor(ctx, user: discord.Member, *,price: str):
        await bot.delete_message(ctx.message)
        embed = discord.Embed(title="ITEM PURCHASED", color=0xFFBF00)
        embed.add_field(name="Purchased by:", value="{}".format(user))
        embed.add_field(name="Item:", value="Sponsored Giveaway")
        embed.add_field(name="Price:", value="{}".format(price))
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text='Sold by: {}'.format(ctx.message.author))
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def customrole(ctx, user: discord.Member, *,price: str):
        await bot.delete_message(ctx.message)
        embed = discord.Embed(title="ITEM PURCHASED", color=0xFFBF00)
        embed.add_field(name="Purchased by:", value="{}".format(user))
        embed.add_field(name="Item:", value="Custom Role")
        embed.add_field(name="Price:", value="{}".format(price))
        await bot.say(embed=embed)
        
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def channel(ctx, user: discord.Member, *,price: str):
        await bot.delete_message(ctx.message)
        embed = discord.Embed(title="ITEM PURCHASED", color=0xFFBF00)
        embed.add_field(name="Purchased by:", value="{}".format(user))
        embed.add_field(name="Item:", value="Custom Channel")
        embed.add_field(name="Price:", value="{}".format(price))
        embed.set_thumbnail(url = ctx.message.server.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="Sold by: {}".format(ctx.message.author))
        await bot.say(embed=embed)        

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def inviteclaim(ctx, user: discord.Member, invites: str, *,price: str):
        await bot.delete_message(ctx.message)
        embed = discord.Embed(title="INVITES REDEEMED", color=0xffbf00)
        embed.add_field(name="Claimed by:", value="{}".format(user))
        embed.add_field(name="For:", value="{} Invites".format(invites))
        embed.add_field(name="Prize:", value="{}".format(price))
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="Distibuted by: {}".format(ctx.message.author))
        await bot.say(embed=embed)
        
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def membership(ctx, user: discord.Member, *,price: str):
        await bot.delete_message(ctx.message)
        embed = discord.Embed(title="ITEM PURCHASED", color=0xFFBF00)
        embed.add_field(name="Purchased by:", value="{}".format(user))
        embed.add_field(name="Item:", value="Membership")
        embed.add_field(name="Price:", value="{}".format(price))
        embed.set_thumbnail(url=ctx.message.server.icon_url) 
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="Sold by: {}".format(ctx.message.author))
        await bot.say(embed=embed)
	        
@bot.command(pass_context=True)
@commands.check(is_owner)
async def searchforgays(ctx):
	msg = await bot.say('🔍Searching for gays please wait<a:loading:587590269617176576>')
	await asyncio.sleep(2)
	await bot.edit_message(msg, 'Found An ant! #1')
	await asyncio.sleep(2)
	await bot.edit_message(msg, 'Found Glue! #2')
	await asyncio.sleep(2)
	await bot.edit_message(msg, 'Found Frigay! #3')
	await asyncio.sleep(2)
	await bot.edit_message(msg, 'Found Arigay! #4')
	await asyncio.sleep(2)
	await bot.edit_message(msg, ':gay_pride_flag:**Final Gay Match Results**:gay_pride_flag:\n4 Matches found:\nAn ant\nGlue\nFrigay\nArigay')
	
@bot.command(pass_context = True)
async def pokemon(ctx, *, pokemon: str):
	embed=discord.Embed(color=0xFFBF00)
	embed.set_image(url='https://play.pokemonshowdown.com/sprites/xyani/{}.gif'.format(pokemon))
	await bot.say(embed=embed)
	
@bot.command(pass_context = True)
async def shinypokemon(ctx, *, pokemon: str):
	embed=discord.Embed(color=0xFFBF00)
	embed.set_image(url='https://play.pokemonshowdown.com/sprites/xyani-shiny/{}.gif'.format(pokemon))
	await bot.say(embed=embed)
	  	        
@bot.command(pass_context = True)
async def flipcoin(ctx):
    choices = ['Heads', 'Tails']
    pick = random.choice(choices)
    if pick == 'Heads':
    	heads=discord.Embed(color = 0xFFBF00, description='{ctx.message.author.name} flipped Heads!')
    heads.set_image(url='https://cdn.discordapp.com/attachments/603252260792959016/603254206765334556/ELECTRO_heads.png')
    await bot.send_typing(ctx.message.channel)
    await bot.say(embed=heads)
    if pick == 'Tails':
    	tails=discord.Embed(color = 0xFFBF00, description='{ctx.message.author.name} flipped Heads!')
    tails.set_image(url='https://cdn.discordapp.com/attachments/603252260792959016/603254226101076016/ELECTRO_tails.png')
    await bot.send_typing(ctx.message.channel)
    await bot.say(embed=tails)
    
@bot.command(pass_context=True)
async def define(ctx, *, msg:str):
	await bot.send_typing(ctx.message.channel)
	if msg is None:
		await bot.say('Please say some words to define!')
		return
	else:
		word = ' '.join(msg)
		api = "http://api.urbandictionary.com/v0/define"
		response = requests.get(api, params=[("term", word)]).json()
	if len(response["list"]) == 0:
		return await bot.say("No defination found!")
	else:
		embed = discord.Embed(description = 'Defination of {word}', color = 0x429CFF)
		embed.add_field(name = "Top definition:", value = response['list'][0]['definition'])
		embed.add_field(name = "Examples:", value = response['list'][0]["example"])
		embed.set_footer(text = "Tag: " + ', '.join(response['tags']))
		await bot.say(embed=embed)
		
@bot.command(pass_context=True)
async def rps(ctx, *, message=None):
    await bot.send_typing(ctx.message.channel)
    ans = ["rock", "paper", "scissor"]
    pick=ans[random.randint(0, 2)]
    embed=discord.Embed(title = "Rock Paper Scissor", color = 0x429CFF)
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/603252260792959016/603976081199857664/ElectroRPS.png')
    if message is None:
        await bot.say('Please Pick Rock, Paper or Scissor!')
    if message.lower() != ans[0] and message.lower() != ans[1] and message.lower() != ans[2] :
        return await bot.say("Please Pick Rock Paper or Scissors")
    elif message.lower() == pick:
        embed.add_field(name = "ELECTRO vs {}".format(ctx.message.author.name), value = "**ELECTRO Picked:**{}\n**{} Picked:** {}\n\n**Result:** Tie".format(pick, ctx.message.author.name, pick))
        return await bot.say(embed=embed)
    else:
        if message.lower()  == "rock" and pick == "paper":
            embed.add_field(name = "ELECTRO vs {}".format(ctx.message.author.name), value = "**ELECTRO Picked:** <:ElectroPaper:603975293484531722>{}\n**{} Picked:** <:ElectroRock:603975251612663828>{}\n\n**Result:** ELECTRO Wins!".format(pick, ctx.message.author.name, message))
            await bot.say(embed=embed)
        elif message.lower()  == "rock" and pick == "scissors":
            embed.add_field(name = "ELECTRO vs {}".format(ctx.message.author.name), value = "**ELECTRO Picked:** <:ElectroScissor:603975202581381141>{}\n**{} Picked:** <:ElectroRock:603975251612663828>{}\n\n**Result:** {} Wins!".format(pick, ctx.message.author.name, message, ctx.message.author.name))
            await bot.say(embed=embed)
        elif message.lower()  == "paper" and pick == "rock":
            embed.add_field(name = "ELECTRO vs {}".format(ctx.message.author.name), value = "**ELECTRO Picked:** <:ElectroRock:603975251612663828>{}\n**{} Picked:** <:ElectroPaper:603975293484531722>{}\n\n**Result:** {} Wins!".format(pick, ctx.message.author.name, message, ctx.message.author.name))
            await bot.say(embed=embed)
        elif message.lower()  == "paper" and pick == "scissors":
            embed.add_field(name = "ELECTRO vs {}".format(ctx.message.author.name), value = "**ELECTRO Picked:** <:ElectroScissor:603975202581381141>{}\n**{} Picked:** <:ElectroPaper:603975293484531722>{}\n\n**Result:** ELECTRO Wins!".format(pick, ctx.message.author.name, message))
            await bot.say(embed=embed)
        elif message.lower()  == "scissors" and pick == "rock":
            embed.add_field(name = "ELECTRO vs {}".format(ctx.message.author.name), value = "**ELECTRO Picked:** <:ElectroRock:603975251612663828>{}\n**{} Picked:** <:ElectroScissor:603975202581381141>{}\n\n**Result:** ELECTRO Wins!".format(pick, ctx.message.author.name, message))
            await bot.say(embed=embed)

@bot.command(pass_context = True)
@commands.check(is_owner) 
async def update(ctx, channel: discord.Channel=None, *, msg: str):
        embed=discord.Embed(description="{}".format(msg), color=0xFFBF00)
        embed.set_author(name="{}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/656517276832366595/677146179439427585/002-brands-and-logotypes.png")
        embed.timestamp = datetime.datetime.utcnow()
        await bot.send_message(channel,"<@&660499979177164821>",embed=embed)
        await bot.delete_message(ctx.message) 

@bot.command(pass_context=True)
async def idklol(ctx):
    await bot.say("{}".format(amounts[test]))

@bot.command(pass_context=True)
async def register(ctx):
    id = ctx.message.author.id
    if id not in amounts:
        amounts[id] = 100
        await bot.say("You are now registered")
        _save()
    else:
        await bot.say("You already have an account")

@bot.command(pass_context=True)
async def transfer(ctx, amount: int, other: discord.Member):
    primary_id = ctx.message.author.id
    other_id = other.id
    if primary_id not in amounts:
        await bot.say("You do not have an account")
    elif other_id not in amounts:
        await bot.say("The other party does not have an account")
    elif amounts[primary_id] < amount:
        await bot.say("You cannot afford this transaction")
    else:
        amounts[primary_id] -= amount
        amounts[other_id] += amount
        await bot.say("Transaction complete")
    _save()

def _save():
    with open('amounts.json', 'w+') as f:
        json.dump(amounts, f)

@bot.command(pass_context = True, aliases=['boobs','pussy','ass','thigh','anal','4k','porngif','gonewild','hentai','hentaimidriff','hentaiass','hentaianal','hentaithigh','hentaineko','hentaikitsune','blowjob','girlsolo','pussygif','feet','femdom','pussyart','smallboobs','girlsologif','classic','cumsluts','randomhentaigif','bjgif','lesbian','play','stop','pause','resume','queue','np','triggered','brazzers','burn','brilliance','bravery','balance','gay','missionpassed','thanos','rip','electroav','math','coronaav','coronaav-green','coronaav-purple','coronaav-pink','corona','joinchannel','leavechannel','testwelcomer'])
async def nsfw(ctx):
        print('{ctx.message.author} used {ctx.message.content}') 
 
@bot.command(pass_context=True)
async def urban(ctx, *, msg:str):
        if msg is None:
                await bot.say('Please mention some word to define!')
        else:
                word = '%20'.join(msg)
                url = f"http://api.urbandictionary.com/v0/define?term={msg}"
                async with aiohttp.ClientSession() as cs:
                        async with cs.get(url) as r:
                                res = await r.json()
                                a = res['list'][0]['definition'] 
                                e = res['list'][0]['example'] 
                                u = ['list'][0]['thumbs_up'] 
                                d = ['list'][0]['thumbs_down'] 
                                embed = discord.Embed(title = 'Urban Dictionary',color = 0xFFBF00)
                                embed.add_field(name = 'Top definition', value=a)
                                embed.add_field(name = 'Example', value=e)
                                embed.set_footer(text = "👍{u} 👎{d}")
                                await bot.say(embed=embed)

@bot.command(pass_context=True)
async def hug(ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
                await bot.say('Go infront of a mirror and hug yourself!')
        else:
                url = f"https://nekos.life/api/v2/img/hug"
                async with aiohttp.ClientSession() as cs:
                               async with cs.get(url) as r:
                                res = await r.json()
                                embed = discord.Embed(color = 0xFFBF00)
                                embed.set_author(name="{} gives {} a big hug! ❤".format(ctx.message.author.name, user.name),url='https://discord.gg/kuWVFpR', icon_url=ctx.message.author.avatar_url)
                                embed.set_image(url=res['url'])
                                await bot.say(embed=embed)

@bot.command(pass_context=True)
async def kiss(ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
                await bot.say('Go infront of a mirror and kiss yourself!')
        else:
                url = f"https://nekos.life/api/v2/img/kiss"
                async with aiohttp.ClientSession() as cs:
                               async with cs.get(url) as r:
                                res = await r.json()
                                embed = discord.Embed(color = 0xFFBF00)
                                embed.set_author(name="{} kisses {}'s lips! ❤".format(ctx.message.author.name, user.name),url='https://discord.gg/kuWVFpR', icon_url=ctx.message.author.avatar_url)
                                embed.set_image(url=res['url'])
                                await bot.say(embed=embed)
 
@bot.command(pass_context=True)
async def slap(ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
                await bot.say('Go infront of a mirror and slap yourself!')
        else:
                url = f"https://nekos.life/api/v2/img/slap"
                async with aiohttp.ClientSession() as cs:
                               async with cs.get(url) as r:
                                res = await r.json()
                                embed = discord.Embed(color = 0xFFBF00)
                                embed.set_author(name="{} slaps {}!! Deserves it! 😡".format(ctx.message.author.name, user.name),url='https://discord.gg/kuWVFpR', icon_url=ctx.message.author.avatar_url)
                                embed.set_image(url=res['url'])
                                await bot.say(embed=embed)
 
@bot.command(pass_context=True)
async def spank(ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
                await bot.say('Go infront of a mirror and spank yourself!')
        else:
                url = f"https://nekos.life/api/v2/img/spank"
                async with aiohttp.ClientSession() as cs:
                               async with cs.get(url) as r:
                                res = await r.json()
                                embed = discord.Embed(color = 0xFFBF00)
                                embed.set_author(name="{} spanks {}! 🍑".format(ctx.message.author.name, user.name),url='https://discord.gg/kuWVFpR', icon_url=ctx.message.author.avatar_url)
                                embed.set_image(url=res['url'])
                                await bot.say(embed=embed)
 
@bot.command(pass_context=True)
async def pat(ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
                await bot.say('Go infront of a mirror and pat yourself!')
        else:
                url = f"https://nekos.life/api/v2/img/pat"
                async with aiohttp.ClientSession() as cs:
                               async with cs.get(url) as r:
                                res = await r.json()
                                embed = discord.Embed(color = 0xFFBF00)
                                embed.set_author(name="{} pats {}! 🤗".format(ctx.message.author.name, user.name),url='https://discord.gg/kuWVFpR', icon_url=ctx.message.author.avatar_url)
                                embed.set_image(url=res['url'])
                                await bot.say(embed=embed)
 
@bot.command(pass_context=True)
async def cuddle(ctx, user: discord.Member):
        if user.id == ctx.message.author.id:
                await bot.say('Go infront of a mirror and cuddle yourself!')
        else:
                url = f"https://nekos.life/api/v2/img/cuddle"
                async with aiohttp.ClientSession() as cs:
                               async with cs.get(url) as r:
                                res = await r.json()
                                embed = discord.Embed(color = 0xFFBF00)
                                embed.set_author(name="{} cuddles {}! 😏".format(ctx.message.author.name, user.name),url='https://discord.gg/kuWVFpR', icon_url=ctx.message.author.avatar_url)
                                embed.set_image(url=res['url'])
                                await bot.say(embed=embed)

@bot.command(pass_context=True, aliases = ['8ball','question'])
async def eightball(ctx, *, question:str):
        if question is None:
                await bot.say('`e!8ball <question>')
        else:
                url = f"https://nekos.life/api/v2/img/8ball"
                async with aiohttp.ClientSession() as cs:
                               async with cs.get(url) as r:
                                res = await r.json()
                                embed = discord.Embed(title = '{}?'.format(question),color = 0xFFBF00)
                                embed.set_image(url=res['url'])
                                await bot.say(embed=embed)

@bot.command(pass_context=True, aliases=['+'])
async def add(ctx, a: int, b:int):
    await bot.say(a+b)
    
@bot.command(pass_context=True, aliases=['-'] )
async def subtract(ctx, a: int, b:int):
    await bot.say(a-b)
    
@bot.command(pass_context=True, aliases=['*'] )
async def multiply(ctx, a: int, b:int):
    await bot.say(a*b)
    
@bot.command(pass_context=True, aliases=['/'])
async def divide(ctx, a: int, b:int):
    await bot.say(a/b)

@bot.command(pass_context=True)
async def pokefuse(ctx):
        num = random.randint(1, 151)
        num2 = random.randint(1, 150)
        embed = discord.Embed(title="Pokefusion", color=0xFFBF00)
        embed.set_image(url="http://images.alexonsager.net/pokemon/fused/{}/{}.{}.png".format(num, num, num2))
        await bot.send_message(ctx.message.channel, embed=embed)
       
   
@bot.command(pass_context=True)
async def whosthatpokemon(ctx):
        num = random.randint(1, 807)
        url = f"https://pokeapi.co/api/v2/pokemon-form/{num}/"
        async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                        data = await r.json()
                        pname = data['name']
                        embed = discord.Embed(title="Who's that pokemon?", color=0xFFBF00)
                        embed.set_image(url="https://play.pokemonshowdown.com/sprites/xyani/"+pname+".gif")
                        await bot.send_message(ctx.message.channel, embed=embed)
                        guess = await bot.wait_for_message(timeout= 30, author=ctx.message.author, channel=ctx.message.channel)
                        if guess.content == data['name']:
                                await bot.say(f'Correct! That pokemon is {data["name"]}')
                        else:
                                await bot.say(f'Incorrect! That pokemon is {data["name"]}') 
       
bot.run(os.getenv('Token'))
