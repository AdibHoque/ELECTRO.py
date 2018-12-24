import discord
from discord.ext import commands
import asyncio
import colorsys
import random
import time
import os
import json

with open("prefixes.json") as f:
    prefixes = json.load(f)
default_prefix = "e!"

def prefix(bot, message):
    id = message.server.id
    return prefixes.get(id, default_prefix)

bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")

@bot.command(name="prefix", pass_context=True)
async def _prefix(ctx, new_prefix):
    # Do any validations you want to do
    prefixes[ctx.message.server.id] = new_prefix
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)
        await bot.say('{} is the new prefix!'.format(new_prefix))

@bot.event
async def on_ready():
    print('the bot is ready')
    print(bot.user.name)
    print(bot.user.id)
    bot.loop.create_task(adib())

def is_owner(ctx):
    return ctx.message.author.id == "488353416599306270" 
 
@bot.command(pass_context=True)
@commands.check(is_owner)
async def oof():
	await bot.change_presence(game=discord.Game(name='For e!help | with '+str(len(set(bot.get_all_members())))+' Users | in ' +str(len(bot.servers))+' Servers'))
 						
@bot.command(pass_context = True)
async def ping(ctx):
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await bot.send_typing(channel)
    t2 = time.perf_counter()
    await bot.say("Pong! {}ms".format(round((t2-t1)*1000)))

@bot.command(pass_context = True)
@commands.has_permissions(manage_nicknames=True)     
async def setnick(ctx, user: discord.Member, *, nickname):
    await bot.change_nickname(user, nickname)
    await bot.say("{}'s nickname was changed to {}!".format(user, nickname))
    await bot.delete_message(ctx.message)

@bot.command()
async def invite():
	await bot.say('Add me to your server by this link - https://discordapp.com/api/oauth2/authorize?client_id=510491243155816449&permissions=8&scope=bot')
	
@bot.command()
async def authlink():
	await bot.say('https://discordapp.com/api/oauth2/authorize?client_id=510491243155816449&permissions=8&scope=bot')	

@bot.command(pass_context = True)
@commands.has_permissions(kick_members=True)     
async def userinfo(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title="{}'s info".format(user.name), description="HERE WHAT I COULD FOUND!", color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)	

@bot.command(pass_context = True)  
async def avatar(ctx, user: discord.Member):
	url = user.avatar_url
	await bot.say(url)
												
@bot.command()
async def ownerinfo():
    await bot.say("**__THIS BOT WAS CREATED BY ADIB HOQUE__**    DISCORD - `@Adib Hoque#5782`       YOUTUBE - __YouTube.com/AdibHoque__            INSTAGRAM - ~~@ADIB_HOQUE_04~~ ")	
	  		   	   	
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def dm(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    await bot.send_message(user, message)
    await bot.say('✅YOUR DM WAS SENT!')
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def say(ctx, *, message=None):
    message = message or "Please specify a message to say!"
    await bot.say(message)
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
async def purge(ctx, number):
    mgs = [] 
    number = int(number) 
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await bot.delete_messages(mgs)
    await bot.say('✅ {} MESSAGES WERE PURGED!'.format(number))

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def spam():
	await bot.say('spam')
	await bot.say('spam')
	await bot.say('spam')
	await bot.say('spam')
	await bot.say('spam')
	await bot.say('spam')
	await bot.say('spam')
	await bot.say('spam')
 
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

@bot.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	embed = discord.Embed(color = discord.Color.green())
	embed.set_author(name='HERE ARE THE BOT COMMANDS!')
	embed.add_field(name='e!ping', value='Returns pong!', inline=True)
	embed.add_field(name='e!dm @user', value='DM a user by this bot!', inline=True)
	embed.add_field(name='e!say', value='Make the bot say anything you want!', inline=True)
	embed.add_field(name='e!kick @user', value='Kick out a user from the server!', inline=True)
	embed.add_field(name='e!ban @user', value='Ban a user from the server!', inline=True)
	embed.add_field(name='e!spam', value='Bot starts spamming!', inline=True)
	embed.add_field(name='e!purge [amount 2-100]', value='Bulk deletes messages!', inline=True)
	embed.add_field(name='e!english @user', value='Soft warns a user to talk in English!', inline=True)
	embed.add_field(name='e!setnick @user [new nick name]', value='Change a users nickname by this command!', inline=True)
	embed.add_field(name='e!userinfo', value='Get info about a user!', inline=True)
	await bot.say(':envelope: Check your DMs for bot commands!')
	embed.add_field(name='e!serverinfo', value='Shows info about the server!', inline=True)
	embed.add_field(name='e!giverole @user @role', value='Give a role to a user!', inline=True)
	embed.add_field(name='e!removerole @user @role', value='Remove a role from a user!', inline=True)
	embed.add_field(name='e!avatar @user', value='Sends avatar url of mentioned user!', inline=True)
	embed.add_field(name='e!invite or e!authlink', value='Sends bot invite link!', inline=True)
	await bot.send_message(author, embed=embed)
	
@bot.command(pass_context = True) 
@commands.has_permissions(kick_members=True)
async def giverole(ctx, user: discord.Member, *, role: discord.Role = None):
        if role is None:
            return await bot.say("Please specify a role to give! ")
            if role not in user.roles:
            	await bot.add_roles(user, role)
            	return await bot.say("{} role has been added to {}.".format(role, user))

@bot.command(pass_context = True) 
@commands.has_permissions(kick_members=True)
async def removerole(ctx, user: discord.Member, *, role: discord.Role = None):
	if role is None:
		return await bot.say('Please specify a role to remove!')
		if role in user.roles:
			return await bot.remove_roles(user, role)
			return await bot.say("{} role has been removed from {}.".format(role, user))

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
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = discord.Color((r << 16) + (g << 8) + b));
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz));
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await bot.say(embed = join);
		   	   	   	  				   	   	   
@bot.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, userName: discord.User):
    await bot.kick(userName)
    await bot.say("{} was kicked!".format(userName))
    
@bot.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def ban(ctx, userName: discord.User):
    await bot.kick(userName)
    await bot.say("{} was banned!".format(userName))    

@bot.command(pass_context=True)
@commands.check(is_owner)
async def roledm(ctx, role: discord.Role, *, message):
    for member in ctx.message.server.members:
        if role in member.roles:
        	await bot.delete_message(ctx.message)
        	await bot.send_message(member, message)
		   	   	   	 		   	  		   	 
bot.run(os.getenv('Token'))		   	   	   	 		   	  		   	 
