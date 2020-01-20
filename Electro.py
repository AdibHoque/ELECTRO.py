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
import dbl
import logging

bot = commands.Bot(command_prefix=commands.when_mentioned_or('e!','E!'),case_insensitive=True)
bot.remove_command("help")

async def status_task():
    while True:
        await bot.change_presence(game=discord.Game(name='For e!help', url='https://twitch.tv/myname', type=1))
        await asyncio.sleep(12)
        await bot.change_presence(game=discord.Game(name='With '+str(len(set(bot.get_all_members())))+' Users', url='https://twitch.tv/myname', type=1))
        await asyncio.sleep(12)
        await bot.change_presence(game=discord.Game(name='in '+str(len(bot.servers))+' Guilds', url='https://twitch.tv/myname', type=1))
        await asyncio.sleep(12)

@bot.event
async def on_ready():
    print('SUCCESS')
    print(bot.user.name)
    print(bot.user.id)
    print('ONLINE')
    bot.loop.create_task(status_task())
    
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
  await bot.say('\n'.join(server.members for server in servers))
 																
@bot.command(pass_context = True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(ctx):
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await bot.send_typing(channel)
    t2 = time.perf_counter()
    embed=discord.Embed(description="Pong! {}ms".format(round((t2-t1)*1000)), color=0xFFBF00) 
    await bot.say(embed=embed)

@bot.command(pass_context = True)
@commands.has_permissions(manage_nicknames=True)     
async def setnick(ctx, user: discord.Member, *, nickname):
    await bot.change_nickname(user, nickname)
    await bot.say("<:ElectroSucess:527118398753079317> {}'s nickname was changed to {}!".format(user, nickname))
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
      await bot.say('<a:ElectroFail:656772856184832025>**Please mention a user to kick & specify a reason for kicking out!**\nEXAMPLE:`e!kick <@user or id> <reason>`')
    if user.server_permissions.kick_members:
      await bot.say("<a:ElectroFail:656772856184832025>**He is a Mod/Admin, I can't do that!**")
      return
    else:
      await bot.send_message(user, 'You were kicked out from **{}**, {}!'.format(ctx.message.server.name, reason))
      await bot.kick(user)
      await bot.say('<a:ElectroSuccess:656772759812046851>{} was kicked, {}!'.format(user, reason))
      await bot.delete_message(ctx.message)
      for channel in user.server.channels:
        if channel.name == '📡electro-logs':
            embed=discord.Embed(title="KICK COMMAND USED", description="**User:** {0}\n**Moderator:** {1}".format(user, ctx.message.author), color=0xFFBF00)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text ='USER KICKED')
            await bot.send_message(channel, embed=embed)
    
@bot.command(pass_context=True)  
@commands.has_permissions(ban_members=True)     
async def ban(ctx, user:discord.Member, *, reason:str):
    if user is None or reason is None:
      await bot.say('<a:ElectroFail:656772856184832025>**Please mention a user to ban & specify a reason for banning!\nExample:`e!ban <@user or id> <reason>**')
    if user.server_permissions.kick_members:
      await bot.say("<a:ElectroFail:656772856184832025>**He is a Mod/Admin, I can't do that!**")
      return
    else:
      await bot.send_message(user, 'You were banned from **{ctx.message.server.name}**, {reason}!'.format(ctx.message.server.name, reason))
      await bot.kick(user)
      await bot.say('<a:ElectroSuccess:656772759812046851>{} was banned, {}!'.format(user, reason))
      await bot.delete_message(ctx.message)
      for channel in user.server.channels:
        if channel.name == '📡electro-logs':
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
        await bot.say(f'<a:ElectroSuccess:656772759812046851>**{user} was unbanned!**')
        for channel in ctx.message.server.channels:
          if channel.name == '📡electro-logs':
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

@bot.command(pass_context = True)  
async def avatarurl(ctx, user: discord.Member):
	url = user.avatar_url
	await bot.say(url)

@bot.command(pass_context = True)
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
    
@bot.command()
async def emoji(emoji: discord.Emoji):
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
    	embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
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
    await bot.say('<a:ElectroSuccess:656772759812046851>{} MESSAGES WERE DELETED!'.format(number))

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
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = 0xFFBF00) 
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.reddit.com/r/me_irl/random") as r:
            data = await r.json()
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

@bot.command(pass_context=True)
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
    url = f"https://nekobot.xyz/api/imagegen?type=tweet&username={usernamename}&text={txt}"
    async with aiohttp.ClientSession() as cs:
    	async with cs.get(url) as r:
            res = await r.json()
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = 0xFFBF00) 
            embed.set_image(url=res['message'])
            embed.title = "{} tweeted: {}".format(usernamename, txt)
            embed.set_footer(text ='You can add the bot to your server by e!invite')
            await bot.say(embed=embed)
		   	   	 
 
@bot.command(pass_context=True)
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
    counter_ = '█' * filled_progbar + '‍ ‍' * (10 - filled_progbar)
    url = f"https://nekobot.xyz/api/imagegen?type=ship&user1={useravatar1}&user2={useravatar2s}"
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            res = await r.json()
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(title=f"💛Love Meter💛", description=f"**💖{shipuser1}**\n**💖{shipuser2}**\n{score}% [{counter_}](https://discord.gg/kuWVFpR)", color = 0x429CFF) 
            embed.set_image(url=res['message'])
            await bot.say(embed=embed)   		   	   	   	 		   	  		   
 
@bot.command(pass_context = True)
async def rolldice(ctx):
    choices = ['1', '2', '3', '4', '5', '6']
    em = discord.Embed(color=0xFFBF00, title='Rolled! (1 6-sided die)', description=random.choice(choices))
    await bot.send_typing(ctx.message.channel)
    await bot.say(embed=em)
    
@bot.command(pass_context=True)
async def kiss(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    randomurl = ["https://media3.giphy.com/media/G3va31oEEnIkM/giphy.gif", "https://i.imgur.com/eisk88U.gif", "https://media1.tenor.com/images/e4fcb11bc3f6585ecc70276cc325aa1c/tenor.gif?itemid=7386341", "http://25.media.tumblr.com/6a0377e5cab1c8695f8f115b756187a8/tumblr_msbc5kC6uD1s9g6xgo1_500.gif"]
    if user.id == ctx.message.author.id:
        await bot.say("Goodluck kissing yourself {}".format(ctx.message.author.mention))
    else:
        embed = discord.Embed(title=f"{user.name} You just got a kiss from {ctx.message.author.name}", color = 0xFFBF00)
        embed.set_image(url=random.choice(randomurl))
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def hug(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    if user.id == ctx.message.author.id:
        await bot.say("{} You can't hug yourself!😒".format(user.mention))
    else:
        randomurl = ["http://gifimage.net/wp-content/uploads/2017/09/anime-hug-gif-5.gif", "https://media1.tenor.com/images/595f89fa0ea06a5e3d7ddd00e920a5bb/tenor.gif?itemid=7919037", "https://media.giphy.com/media/NvkwNVuHdLRSw/giphy.gif"]
        embed = discord.Embed(title=f"{user.name} You just got a hug from {ctx.message.author.name}", color = 0xFFBF00)
        embed.set_image(url=random.choice(randomurl))
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def gender(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    random.seed(user.id)
    genderized = ["Male", "Female", "Transgender", "Unknown", "Can't be detected", "Shemale"]
    randomizer = random.choice(genderized)
    if user == ctx.message.author:
        embed = discord.Embed(title="You should know your own gender😒", color = 0xFFBF00)
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(color=0xFFBF00)
        embed.add_field(name=f"{user.name}'s gender check results", value=f"{randomizer}")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def virgin(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    random.seed(user.id)
    results= ["Not a virgin", "Never been a virgin", "100% Virgin", "Half virgin :thinking:", "Forever Virgin"]
    randomizer = random.choice(results)
    if user == ctx.message.author:
        embed = discord.Embed(title="Go ask yourself if you are still a virgin or not!", color = discord.Color((r << 16) + (g << 8) + b))
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(color=0xFFBF00)
        embed.add_field(name=f"{user.name}'s virginity check results", value=f"{randomizer}")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def joke(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    joke = ["What do you call a frozen dog?\nA pupsicle", "What do you call a dog magician?\nA labracadabrador", "What do you call a large dog that meditates?\nAware wolf", "How did the little scottish dog feel when he saw a monster\nTerrier-fied!", "Why did the computer show up at work late?\nBecause it had a hard drive", "Autocorrect has become my worst enime", "What do you call an IPhone that isn't kidding around\nDead Siri-ous", "The guy who invented auto-correct for smartphones passed away today\nRestaurant in peace", "You know you're texting too much when you say LOL in real life, instead of laughing", "I have a question = I have 18 Questions\nI'll look into it = I've already forgotten about it", "Knock Knock!\nWho's there?\Owls say\nOwls say who?\nYes they do.", "Knock Knock!\nWho's there?\nWill\nWill who?\nWill you just open the door already?", "Knock Knock!\nWho's there?\nAlpaca\nAlpaca who?\nAlpaca the suitcase, you load up the car.","Once a guy foumd a genie lamp, He rubbed the lamp and wished that he dosen't wants to die virgin. Then the genie granted him immortality!'", "Yo momma's teeth is so yellow, when she smiled at traffic, it slowed down.", "Yo momma's so fat, she brought a spoon to the super bowl.", "Yo momma's so fat, when she went to the beach, all the whales started singing 'We are family'", "Yo momma's so stupid, she put lipstick on her forehead to make up her mind.", "Yo momma's so fat, even Dora can't explore her.", "Yo momma's so old, her breast milk is actually powder", "Yo momma's so fat, she has to wear six different watches: one for each time zone", "Yo momma's so dumb, she went to the dentist to get a bluetooth", "Yo momma's so fat, the aliens call her 'the mothership'", "Yo momma's so ugly, she made an onion cry.", "Yo momma's so fat, the only letters she knows in the alphabet are K.F.C", "Yo momma's so ugly, she threw a boomerang and it refused to come back", "Yo momma's so fat, Donald trump used her as a wall", "Sends a cringey joke\nTypes LOL\nFace in real life : Serious AF", "I just got fired from my job at the keyboard factory. They told me I wasn't putting enough shifts.", "Thanks to autocorrect, 1 in 5 children will be getting a visit from Satan this Christmas.", "Have you ever heard about the new restaurant called karma?\nThere's no menu, You get what you deserve.", "Did you hear about the claustrophobic astronaut?\nHe just needed a little space", "Why don't scientists trust atoms?\nBecase they make up everything", "How did you drown a hipster?\nThrow him in the mainstream", "How does moses make tea?\nHe brews", "A man tells his doctor\n'DOC, HELP ME. I'm addicted to twitter!'\nThe doctor replies\n'Sorry i don't follow you...'", "I told my wife she was drawing her eyebrows too high. She looked surprised.", "I threw a boomeranga a few years ago. I now live in constant fear"]
    embed = discord.Embed(color = 0xFFBF00)
    embed.add_field(name=f"Here is a random joke {ctx.message.author}!", value=random.choice(joke))
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def slap(ctx, user: discord.Member = None):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    gifs = ["http://rs20.pbsrc.com/albums/b217/strangething/flurry-of-blows.gif?w=280&h=210&fit=crop", "https://media.giphy.com/media/LB1kIoSRFTC2Q/giphy.gif", "https://i.imgur.com/4MQkDKm.gif"]
    if user == None:
        await bot.say(f"{ctx.message.author.mention} Please mention a user to slap!")
    else:
        embed = discord.Embed(title=f"{ctx.message.author.name} Just slapped the shit out of {user.name}!", color = 0xFFBF00)
        embed.set_image(url=random.choice(gifs))
        await bot.say(embed=embed)

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
	await bot.say('<a:fortnite1:527116722369593365> <a:fortnite2:527116726249193472> <a:fortnite1:527116722369593365>')
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
	
@bot.command(pass_context=True)
async def plsboi(ctx):
	await asyncio.sleep(1)
	await bot.say('<a:plsboi:527116722218467328>')
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(description='**[HELP MENU](https://discord.gg/kuWVFpR)**\nTo see a detailed page, just react with their numeral emojis or add the page number after the `e!help` command. E.G. `e!help1`, `e!help2` Etc.', color = 0xFFBF00) 
    embed.set_author(name='ELECTRO',url='https://discord.gg/kuWVFpR', icon_url='https://cdn.discordapp.com/attachments/656517276832366595/656519678499487745/ELECTRO.png')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/656760631474520074/ELECTRO_ELECTRIFY_YOUR_SERVER.gif')
    embed.add_field(name = '<:ElectroGeneral:666202936929681418> General Commands - (8)',value ='`ping`,`userinfo`,`serverinfo`,`ownerinfo`,`avatar`,`membercount`,`invite`,`upvote`',inline = False)
    embed.add_field(name = '<:ElectroModeration:666920202818027531> Moderation Commands - (13)',value ='`kick`,`ban`,`setnick`,`role`,`say`,`DM`,`english`,`rolecolor`,`lockdown`,`unlock`,`menro`,`mute`,`unmute`',inline = False)
    embed.add_field(name = '<:ElectroFun:666203658467147776> Fun Commands - (16)',value ='`meme`,`joke`,`love`,`slap`, `kiss`, `hug`, `virgin`, `gender`, `tweet`, `rolldice`, `flipcoin`, `howgay`, `whowouldwin`, `captcha`,`magik`,`deepfry`',inline = False)
    embed.add_field(name = '<:ElectroMusic:666203904186515467> Music Commands - (8)',value ='`play`,`skip`,`stop`,`NP`,`queue`,`pause`,`resume`,`volume`\n\n<:ElectroBookmark:668018207549816833> **Additional Links:**\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)',inline = False)
    msg = await bot.send_message(author ,embed=embed)
    await bot.add_reaction(msg,'1⃣')
    await bot.add_reaction(msg,'2⃣')
    await bot.add_reaction(msg,'3⃣')
    await bot.add_reaction(msg,'4⃣')
    await bot.say('📨 Check Your DMs For Bot Commands!')
    			
@bot.command(pass_context = True)
async def help1(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title = 'GENERAL COMMANDS', color = 0xFFBF00)
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
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For General Commands!')
    
@bot.command(pass_context = True)
async def help2(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title = 'MODERATION COMMANDS', color = 0xFFBF00)
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
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Moderation Commands!') 
    
@bot.command(pass_context = True)
async def help3(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title = 'FUN COMMANDS', color = 0xFFBF00)
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
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Fun Commands!')   
    
@bot.command(pass_context = True)
async def help4(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title = 'MUSIC COMMANDS', color = 0xFFBF00) 
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/656517276832366595/656760860085321748/ELECTRO_HELP4.gif')
    embed.add_field(name = 'Play',value ='Plays music from YouTube!\n**USAGE:**`e!play <music name> or <url>`',inline = False)
    embed.add_field(name = 'Skip',value ='Skips the current playing music!\n**USAGE:**`e!skip',inline = False)
    embed.add_field(name = 'Stop',value ='Stops playing music and leaves the vc!\n**USAGE:**`e!stop` ',inline = False)
    embed.add_field(name = 'NP',value ='Shows the now playing music!\n**USAGE:**`e!np`',inline = False)
    embed.add_field(name = 'Queue',value ='Shows the music queue!\n**USAGE:**`e!queue`',inline = False)
    embed.add_field(name = 'Pause',value ='Pauses the current playing song!\n**USAGE:**`e!pause`',inline = False)
    embed.add_field(name = 'Resume',value ='Resumes the current paused song!\n**USAGE:**`e!resume`',inline = False)
    embed.add_field(name = 'Volume',value ='Change volume of the song!\n**USAGE:**`e!volume <1-200>`\n[Add Bot](https://discordapp.com/api/oauth2/authorize?client_id=629323586930212884&permissions=8&scope=bot) | [Join Server](https://discord.gg/kuWVFpR ) | [Upvote](https://discordbots.org/bot/629323586930212884/vote)',inline = False)
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Music Commands!')    

@bot.command(pass_context=True)
async def howgay(ctx, user: discord.Member = None):
	if user is None:
		score = random.randint(0, 100)
		r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
		embed = discord.Embed(title=f"Gayrate machine", description=f"{ctx.message.author} is **{score}%** gay :rainbow:", color = 0xFFBF00) 
		await bot.say(embed=embed)
	else:
		score = random.randint(0, 100)
		r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
		embed = discord.Embed(title=f"Gayrate machine", description=f"{user} is **{score}%** gay :rainbow:", color = 0xFFBF00)
		await bot.say(embed=embed)
  
@bot.command(pass_context=True)
async def gayrate(ctx, user: discord.Member = None):
	if user is None:
		score = random.randint(0, 100)
		r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
		embed = discord.Embed(title=f"Gayrate machine", description=f"{ctx.message.author} is **{score}%** gay :rainbow:", color = 0xFFBF00)
		await bot.say(embed=embed)
	else:
		score = random.randint(0, 100)
		r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
		embed = discord.Embed(title=f"Gayrate machine", description=f"{user} is **{score}%** gay :rainbow:", color = 0xFFBF00)
		await bot.say(embed=embed)
		
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
@commands.has_permissions(administrator=True) 
async def announce(ctx, channel: discord.Channel=None, *, msg: str):
	embed=discord.Embed(title="ANNOUNCEMENT", description="{}".format(msg), color=0xFFBF00)
	embed.set_author(name="{}".format(ctx.message.author))
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
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(title = "MESSAGE EDITED", color = 0xFFBF00)
            embed.add_field(name = 'Message Author:',value ='{}'.format(user),inline = False)
            embed.add_field(name = 'Before:',value ='{}'.format(before.content),inline = False)
            embed.add_field(name = 'After:',value ='{}'.format(after.content),inline = False)
            embed.add_field(name = 'Channel:',value ='{0}\n[Jump To Message](https://discordapp.com/channels/{1}/{2}/{3})'.format(before.channel.mention, before.server.id, before.channel.id, before.id),inline = False)
            embed.set_thumbnail(url=user.server.icon_url) 
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text ='MESSAGE EDITED')
            await bot.send_message(channel, embed=embed)
         
@bot.event
async def on_reaction_add(reaction, user):
	if reaction.message.server is None:
		if reaction.emoji == '1⃣':
			embed = discord.Embed(title = 'GENERAL COMMANDS', color = 0xFFBF00)
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
		if reaction.emoji == '2⃣':
			embed = discord.Embed(title = 'MODERATION COMMANDS', color = 0xFFBF00)
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
			await bot.send_message(user, embed=embed)
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
					embed.set_thumbnail(url=reaction.server.icon_url)
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
        embed.set_thumbnail(url=reaction.server.icon_url) 
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text ='REACTION REMOVED')
        await bot.send_message(logchannel, embed=embed)   
        
@bot.event
async def on_message(message):
	if not message.author.bot:
		await bot.process_commands(message)
	if '<@488353416599306270>' in message.content:
		emoji = 'a:AdibReeeeee:558181398670737408'
		await bot.add_reaction(message, emoji) 
		channe = bot.get_channel('656535174548553730')
	if message.server is None and message.author != bot.user:
		electrosucess = 'a:ElectroSuccess:656772759812046851'
		await bot.add_reaction(message, electrosucess)
		embed=discord.Embed(title="{}".format(message.author), description="{}".format(message.content), color = 0xFFBF00)
		embed.set_thumbnail(url= message.author.avatar_url)
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
async def magik(ctx, user:discord.Member):
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
async def captcha(ctx, user:discord.Member):
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
async def deepfry(ctx, user:discord.Member):
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
async def whowouldwin(ctx, user1:discord.Member, *, user2:discord.Member):
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
async def iphonex(ctx, user:discord.Member):
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
async def trash(ctx, user:discord.Member):
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
async def threats(ctx, user:discord.Member):
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
async def cc(ctx, user: discord.Member, *,price: str):
        await bot.delete_message(ctx.message)
        embed = discord.Embed(title="ITEM PURCHASED", color=0x429CFF)
        embed.add_field(name="Purchased by:", value="{}".format(user))
        embed.add_field(name="Item:", value="Custom Dyno Command")
        embed.add_field(name="Price:", value="{}".format(price))
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="Sold by: {}".format(ctx.message.author))
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
	embed.set_image(url='https://raw.githubusercontent.com/110Percent/beheeyem-data/master/gifs/{}.gif'.format(pokemon))
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
	embed.timestamp = datetime.datetime.utcnow()
	await bot.send_message(channel,"<@&660499979177164821>",embed=embed)
	await bot.delete_message(ctx.message) 
            
bot.run(os.getenv('Token'))
