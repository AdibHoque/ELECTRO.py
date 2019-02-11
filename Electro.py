import discord
from discord.ext import commands
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

class DiscordBotsOrgAPI:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjUxMDQ5MTI0MzE1NTgxNjQ0OSIsImJvdCI6dHJ1ZSwiaWF0IjoxNTQ2NDExNzYxfQ.V_7sJcSceSDB93OR5ZaTkoGHQqQN2ic2uO7U8cSeQlM'  #  set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
            logger.info('attempting to post server count')
            try:
                await self.dblpy.post_server_count()
                logger.info('posted server count ({})'.format(len(self.bot.guilds)))
            except Exception as e:
                logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)

def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))

bot = commands.Bot(command_prefix=commands.when_mentioned_or('e!'))
bot.remove_command("help")

async def status_task():
    while True:
        await bot.change_presence(game=discord.Game(name='for e!help', url='https://twitch.tv/myname', type=1))
        await asyncio.sleep(5)
        await bot.change_presence(game=discord.Game(name='with '+str(len(set(bot.get_all_members())))+' users', url='https://twitch.tv/myname', type=1))
        await asyncio.sleep(5)
        await bot.change_presence(game=discord.Game(name='in '+str(len(bot.servers))+' servers', url='https://twitch.tv/myname', type=1))
        await asyncio.sleep(5)

@bot.event
async def on_ready():
    print('the bot is ready')
    print(bot.user.name)
    print(bot.user.id)
    print('working properly')
    bot.loop.create_task(status_task())
    
@bot.command(pass_context = True)
async def prefix(ctx):
	await bot.say('The prefix for the bot is **e!**') 

def is_owner(ctx):
    return ctx.message.author.id == "488353416599306270"
    
def is_masstyper(ctx):
    return ctx.message.author.id == "488353416599306270, 517729298355060736"      
   
@bot.command(pass_context = True)
@commands.check(is_owner)
async def servers(ctx):
  servers = list(bot.servers)
  await bot.say(f"Connected on {str(len(servers))} servers:")
  await bot.say(join(server.name for server in servers))						
 																
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
    await bot.say("<:ElectroSucess:527118398753079317> {}'s nickname was changed to {}!".format(user, nickname))
    await bot.delete_message(ctx.message)

@bot.command()
async def invite():
	await bot.say('Add me to your server by this link - https://discordapp.com/api/oauth2/authorize?client_id=510491243155816449&permissions=8&scope=bot')
	
@bot.command()
async def upvote():
	await bot.say('**CLICK THE LINK BELOW AND UPVOTE** https://discordbots.org/bot/510491243155816449')
	
@bot.command()
async def server():
	await bot.say('**PLEASE JOIN ELECTRO SUPPORT SERVER FROM THE LINK BELOW-** \nhttps://discord.gg/eGkATHU ** ')
	
@bot.command()
async def support():
	await bot.say('**PLEASE JOIN ELECTRO SUPPORT SERVER FROM THE LINK BELOW-** https://discord.gg/eGkATHU')			

@bot.command(pass_context = True)  
async def userinfo(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title="{}'s info".format(user.name), description="HERE WHAT I FOUND!", color = discord.Color((r << 16) + (g << 8) + b))
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
    await bot.say("__**THIS BOT WAS CREATED BY ADIB HOQUE**__\n**DISCORD** - `@ADIB HOQUE#6969`\n**YOUTUBE** - YouTube.com/AdibHoque")
    
@bot.command()
async def emoji(emoji: discord.Emoji):
    await bot.say(emoji.url)    		
	  		   	   	
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def dm(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    await bot.send_message(user, message)
    await bot.say('<:ElectroSucess:527118398753079317>YOUR DM WAS SENT!')
    await bot.delete_message(ctx.message)
    
@bot.command(pass_context = True)
async def embed(ctx, msg:str, *, msg2:str):
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
async def purge(ctx, number):
    mgs = [] 
    number = int(number) 
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await bot.delete_messages(mgs)
    await bot.say('<:ElectroSucess:527118398753079317> {} MESSAGES WERE DELETED!'.format(number))

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def english(ctx, *, msg = None):
	channel = ctx.message.channel
	await bot.say(msg + ', Please do not use any other languages than **English.**')
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True)
@commands.check(is_masstyper)
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
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, user: discord.Member, *, role: discord.Role = None):
	if role is None:
		return await bot.say("Please specify a role to give! ")
		if role not in user.roles:
			await bot.add_roles(user, role)
			return await bot.say("<:ElectroSucess:527118398753079317> **{}** role has been added to **{}**.".format(role, user))

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
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = discord.Color((r << 16) + (g << 8) + b));
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz));
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await bot.say(embed = join);
		   	   	     
@bot.command(pass_context=True)
async def tweet(ctx, usernamename:str, *, txt:str):
    url = f"https://nekobot.xyz/api/imagegen?type=tweet&username={usernamename}&text={txt}"
    async with aiohttp.ClientSession() as cs:
    	async with cs.get(url) as r:
            res = await r.json()
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
            embed.set_image(url=res['message'])
            embed.title = "{} tweeted: {}".format(usernamename, txt)
            embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
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
            embed = discord.Embed(title=f"{shipuser1} ❤ {shipuser2} Love each others", description=f"Love\n`{counter_}` Score:**{score}% **\nLoveName:**{finalName}**", color = discord.Color((r << 16) + (g << 8) + b))
            embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
            embed.set_image(url=res['message'])
            await bot.say(embed=embed)   		   	   	   	 		   	  		   
 
@bot.command(pass_context = True)
async def rolldice(ctx):
    choices = ['1', '2', '3', '4', '5', '6']
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Rolled! (1 6-sided die)', description=random.choice(choices))
    await bot.send_typing(ctx.message.channel)
    await bot.say(embed=em)
    
@bot.command(pass_context = True)
async def flipcoin(ctx):
    choices = ['Heads', 'Tails']
    color = discord.Color(value=0x00ff00)
    em=discord.Embed(color=color, title='Flipped a coin!')
    em.description = random.choice(choices)
    await bot.send_typing(ctx.message.channel)
    await bot.say(embed=em)
    
@bot.command(pass_context=True)
async def kiss(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    randomurl = ["https://media3.giphy.com/media/G3va31oEEnIkM/giphy.gif", "https://i.imgur.com/eisk88U.gif", "https://media1.tenor.com/images/e4fcb11bc3f6585ecc70276cc325aa1c/tenor.gif?itemid=7386341", "http://25.media.tumblr.com/6a0377e5cab1c8695f8f115b756187a8/tumblr_msbc5kC6uD1s9g6xgo1_500.gif"]
    if user.id == ctx.message.author.id:
        await bot.say("Goodluck kissing yourself {}".format(ctx.message.author.mention))
    else:
        embed = discord.Embed(title=f"{user.name} You just got a kiss from {ctx.message.author.name}", color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_image(url=random.choice(randomurl))
        embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def hug(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    if user.id == ctx.message.author.id:
        await bot.say("{} You can't hug yourself!😒".format(user.mention))
    else:
        randomurl = ["http://gifimage.net/wp-content/uploads/2017/09/anime-hug-gif-5.gif", "https://media1.tenor.com/images/595f89fa0ea06a5e3d7ddd00e920a5bb/tenor.gif?itemid=7919037", "https://media.giphy.com/media/NvkwNVuHdLRSw/giphy.gif"]
        embed = discord.Embed(title=f"{user.name} You just got a hug from {ctx.message.author.name}", color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_image(url=random.choice(randomurl))
        embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def gender(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    random.seed(user.id)
    genderized = ["Male", "Female", "Transgender", "Unknown", "Can't be detected", "Shemale"]
    randomizer = random.choice(genderized)
    if user == ctx.message.author:
        embed = discord.Embed(title="You should know your own gender😒", color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(color=0xfff47d)
        embed.add_field(name=f"{user.name}'s gender check results", value=f"{randomizer}")
        embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def virgin(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    random.seed(user.id)
    results= ["Not a virgin", "Never been a virgin", "100% Virgin", "Half virgin :thinking:", "We cannot seem to find out if this guy is still a virgin due to it's different blood type"]
    randomizer = random.choice(results)
    if user == ctx.message.author:
        embed = discord.Embed(title="Go ask yourself if you are still a virgin or not!", color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(color=0x7dfff2)
        embed.add_field(name=f"{user.name}'s virginity check results", value=f"{randomizer}")
        embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def joke(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    joke = ["What do you call a frozen dog?\nA pupsicle", "What do you call a dog magician?\nA labracadabrador", "What do you call a large dog that meditates?\nAware wolf", "How did the little scottish dog feel when he saw a monster\nTerrier-fied!", "Why did the computer show up at work late?\nBecause it had a hard drive", "Autocorrect has become my worst enime", "What do you call an IPhone that isn't kidding around\nDead Siri-ous", "The guy who invented auto-correct for smartphones passed away today\nRestaurant in peace", "You know you're texting too much when you say LOL in real life, instead of laughing", "I have a question = I have 18 Questions\nI'll look into it = I've already forgotten about it", "Knock Knock!\nWho's there?\Owls say\nOwls say who?\nYes they do.", "Knock Knock!\nWho's there?\nWill\nWill who?\nWill you just open the door already?", "Knock Knock!\nWho's there?\nAlpaca\nAlpaca who?\nAlpaca the suitcase, you load up the car.", "Yo momma's teeth is so yellow, when she smiled at traffic, it slowed down.", "Yo momma's so fat, she brought a spoon to the super bowl.", "Yo momma's so fat, when she went to the beach, all the whales started singing 'We are family'", "Yo momma's so stupid, she put lipstick on her forehead to make up her mind.", "Yo momma's so fat, even Dora can't explore her.", "Yo momma's so old, her breast milk is actually powder", "Yo momma's so fat, she has to wear six different watches: one for each time zone", "Yo momma's so dumb, she went to the dentist to get a bluetooth", "Yo momma's so fat, the aliens call her 'the mothership'", "Yo momma's so ugly, she made an onion cry.", "Yo momma's so fat, the only letters she knows in the alphabet are K.F.C", "Yo momma's so ugly, she threw a boomerang and it refused to come back", "Yo momma's so fat, Donald trump used her as a wall", "Sends a cringey joke\nTypes LOL\nFace in real life : Serious AF", "I just got fired from my job at the keyboard factory. They told me I wasn't putting enough shifts.", "Thanks to autocorrect, 1 in 5 children will be getting a visit from Satan this Christmas.", "Have you ever heard about the new restaurant called karma?\nThere's no menu, You get what you deserve.", "Did you hear about the claustrophobic astronaut?\nHe just needed a little space", "Why don't scientists trust atoms?\nBecase they make up everything", "How did you drown a hipster?\nThrow him in the mainstream", "How does moses make tea?\nHe brews", "A man tells his doctor\n'DOC, HELP ME. I'm addicted to twitter!'\nThe doctor replies\n'Sorry i don't follow you...'", "I told my wife she was drawing her eyebrows too high. She looked surprised.", "I threw a boomeranga a few years ago. I now live in constant fear"]
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name=f"Here is a random joke that {ctx.message.author.name} requested", value=random.choice(joke))
    embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def slap(ctx, user: discord.Member = None):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    gifs = ["http://rs20.pbsrc.com/albums/b217/strangething/flurry-of-blows.gif?w=280&h=210&fit=crop", "https://media.giphy.com/media/LB1kIoSRFTC2Q/giphy.gif", "https://i.imgur.com/4MQkDKm.gif"]
    if user == None:
        await bot.say(f"{ctx.message.author.mention} Please mention a user to slap!")
    else:
        embed = discord.Embed(title=f"{ctx.message.author.name} Just slapped the shit out of {user.name}!", color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_image(url=random.choice(gifs))
        embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
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
    
    em = Embed(title="Membercount")
    em.description =    "```\n" \
                        "Total Members:%s (%s)\n" \
                        "User Count:   %s (%s)\n" \
                        "Bot Count:    %s (%s)\n" \
                        "Created at:   %s\n" \
                        "```" % (membs, membs_on, users, users_on, bots, bots_on, created)

    await bot.send_message(ctx.message.channel, embed=em)
    await bot.delete_message(ctx.message)
    
@bot.group(pass_context=True, invoke_without_command=True)
@commands.has_permissions(manage_roles=True)  
async def role(ctx, user:discord.Member=None,*, role:discord.Role=None):
    if user is None or role is None:
        await bot.say('There was a error executing this command!**PROPER USAGE:**`e!role @user @role`')
        return
    if role in user.roles:
        await bot.remove_roles(user, role)
        await bot.say("<:ElectroSucess:527118398753079317> Changed roles for {}, -{}".format(user, role))
        return
    if role not in ctx.message.server.roles:
        await bot.say(f"There isn't any role named {role}.Please specify a valid role!")
        return
    else:
        await bot.add_roles(user, role)
        await bot.say("<:ElectroSucess:527118398753079317> Changed roles for {}, +{}".format(user, role))
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
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='ELECTRO COMMANDS')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/526757013745696769/527492677558599696/electro.png')
    embed.add_field(name = '``USAGE:`` ',value ='To see a page, just add the page number after the `e!help` command.Like this `e!help1`, `e!help2` Etc.',inline = False)
    embed.add_field(name = 'PAGE 1 | General Commands ',value ='General commands which everyone can use!.',inline = False)
    embed.add_field(name = 'PAGE 2 | Moderation Commands',value ='Commands that are used for moderation and can only be used by server moderators.',inline = False)
    embed.add_field(name = 'PAGE 3 | Fun Commands ',value ='Fun commands are used for fun and can be used by everyone.',inline = False)
    embed.add_field(name = 'PAGE 4 | Emoji Commands ',value ='Commands that makes ELECTRO send gif emotes.',inline = False)
    embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Bot Commands!')
    			
@bot.command(pass_context = True)
async def help1(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='GENERAL COMMANDS')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/526757013745696769/527492677558599696/electro.png')
    embed.add_field(name = 'Ping',value ='Returns ping lantency!\n**USAGE:**``e!ping``',inline = False)
    embed.add_field(name = 'Userinfo',value ='Shows info about mentioned user!\n**USAGE:**``e!userinfo @user``',inline = False)
    embed.add_field(name = 'Serverinfo',value ='Shows info about the server!\n**USAGE:**``e!serverinfo``',inline = False)
    embed.add_field(name = 'Ownerinfo',value ='Shows info about the bot owner!\n**USAGE:**``e!ownerinfo``',inline = False)
    embed.add_field(name = 'Avatar',value ='Shows avatar of the mentioned user!\n**USAGE:**``e!avatar @user``',inline = False)
    embed.add_field(name = 'Membercount',value ='Shows member count of the server!\n**USAGE:**``e!membercount``',inline = False)
    embed.add_field(name = 'Invite',value ='Sends bot invite link!\n**USAGE:**``e!invite``',inline = False)
    embed.add_field(name = 'Upvote',value ='Sends bot upvote link!\n**USAGE:**``e!upvote``',inline = False)
    embed.afd_field(name = 'Emoji',value ='Sends url of the emoji!\n**USAGE:**``e!emoji :emoji: ``',inline = False)
    embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For General Commands!')
    
@bot.command(pass_context = True)
async def help2(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='MODERATION COMMANDS')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/526757013745696769/527492677558599696/electro.png')
    embed.add_field(name = 'Kick',value ='Kicks out mentioned user from the server!\n**USAGE:**``e!kick @user``',inline = False)
    embed.add_field(name = 'Ban',value ='Bans mentioned user from the server!\n**USAGE:**``e!ban @user``',inline = False) 
    embed.add_field(name = 'Setnick',value ='Changes nickname of mentioned user!\n**USAGE:**``e!setnick @user [new nickname]``',inline = False)
    embed.add_field(name = 'Role',value ='Gives or removes role from mentioned user!\n**USAGE:**``e!role @user @role``',inline = False)
    embed.add_field(name = 'Say',value ='Make ELECTRO say anything you want!\n**USAGE:**``e!say [your text]``',inline = False)
    embed.add_field(name = 'DM',value ='Make ELECTRO DM mentioned user anything you want!\n**USAGE:**``e!dm @user [your text]``',inline = False) 
    embed.add_field(name = 'English',value ='Softwarns mentioned user to talk in English!\n**USAGE:**``e!english @user``',inline = False) 
    embed.add_field(name = 'Purge',value ='Bulk deletes messages!\n**USAGE:**``e!purge [amount]``',inline = False)
    embed.add_field(name = 'RoleColor',value ='Give custom color to mentioned role!\n**USAGE:**``e!rolecolor @role hexcode``',inline = False)
    embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Moderation Commands!') 
    
@bot.command(pass_context = True)
async def help3(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='FUN COMMANDS')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/526757013745696769/527492677558599696/electro.png')
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
    embed.add_field(name = 'Howgay',value ='Checks gayrate of mentioned user!\n**USAGE:**``e!howgay @user``',inline = False)
    embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Fun Commands!')   
    
@bot.command(pass_context = True)
async def help4(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='EMOJI COMMANDS')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/526757013745696769/527492677558599696/electro.png')
    embed.add_field(name = 'Fortnite',value ='<a:fortnite1:527116722369593365> <a:fortnite2:527116726249193472> <a:fortnite1:527116722369593365>',inline = False)
    embed.add_field(name = 'Hundred',value ='<a:100:527116694506700819>',inline = False)
    embed.add_field(name = 'Party',value ='<a:PartyGlasses:527116697791102977>',inline = False)
    embed.add_field(name = 'Dogdance',value ='<a:dogdance:527116702580867092>',inline = False)
    embed.add_field(name = 'Hype',value ='<a:DiscordHype:527116695253286933>',inline = False)
    embed.add_field(name = 'Plsboi',value ='<a:plsboi:527116722218467328>',inline = False)
    embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Emoji Commands!')    

@bot.command(pass_context=True)
async def howgay(ctx, user: discord.Member = None):
    score = random.randint(0, 100)
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title=f"Gayrate machine", description=f"{user} is **{score}%** gay :rainbow:", color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
    await bot.say(embed=embed)
    
@bot.command(pass_context=True)
async def gayrate(ctx, user: discord.Member = None):
    score = random.randint(0, 100)
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title=f"Gayrate machine", description=f"{user} is **{score}%** gay :rainbow:", color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
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
        user = ctx.message.author
        await bot.edit_role(ctx.message.server, role, color = discord.Color(int(colour, base=16)))
        await bot.say("<:ElectroSucess:527118398753079317> {} role color has been changed!".format(role)) 
        
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
        colour = '0x' + new_val
        user = ctx.message.author
        await bot.edit_role(ctx.message.server, role, color = discord.Color(int(colour, base=16)))
        await bot.say("<:ElectroSucess:527118398753079317> {} role colour has been changed!".format(role)) 
        
@bot.command(pass_context=True) 
@commands.has_permissions(kick_members=True)     
async def kick(ctx, user:discord.Member):
    if user is None:
      await bot.say('Please mention a user to kick!')
    if user.server_permissions.kick_members:
      await bot.say("**{} is Mod/Admin, I can't do that!**".format(user))
      return
    else:
    	await bot.delete_message(ctx.message)
    	await bot.send_message(user, 'You have been kicked from {}'.format(ctx.message.server.name))
    	await bot.kick(user)
    	await bot.say('<:ElectroSucess:527118398753079317>'+user.name+' was kicked!')
    	for channel in user.server.channels:
    		if channel.name == '📡electro-logs':
    			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    			embed.set_author(name='Kick COMMAND USED')
    			embed.add_field(name = 'Kicked User:',value ='{}'.format(user.name),inline = False)
    			embed.add_field(name = 'Kicked by:',value ='{}'.format(ctx.message.author),inline = False)
    			embed.add_field(name = 'Channel:',value ='{}'.format(ctx.message.channel.name),inline = False)
    			embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
    			await bot.send_message(channel, embed=embed)      
    	
@commands.has_permissions(kick_members=True)     
async def ban(ctx, user:discord.Member):
    if user is None:
      await bot.say('Please mention a user to ban!')
    if user.server_permissions.ban_members:
      await bot.say("**{} is Mod/Admin, I can't do that!**".format(user))
      return
    else:
    	await bot.delete_message(ctx.message)
    	await bot.send_message(user, 'You have been banned from {}'.format(ctx.message.server.name))
    	await bot.ban(user)
    	await bot.say('<:ElectroSucess:527118398753079317>'+user.name+' was banned!')
    	for channel in user.server.channels:
    		if channel.name == '📡electro-logs':
    			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    			embed.set_author(name='BAN COMMAND USED')
    			embed.add_field(name = 'Banned User:',value ='{}'.format(user.name),inline = False)
    			embed.add_field(name = 'Banned by:',value ='{}'.format(ctx.message.author),inline = False)
    			embed.add_field(name = 'Channel:',value ='{}'.format(ctx.message.channel.name),inline = False)
    			embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
    			await bot.send_message(channel, embed=embed)   
    	
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
        if channel.name == '📡electro-logs':
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
            embed.set_author(name='MESSAGE EDITED')
            embed.add_field(name = 'Message Author:',value ='{}'.format(user.name),inline = False)
            embed.add_field(name = 'Before:',value ='{}'.format(before.content),inline = False)
            embed.add_field(name = 'After:',value ='{}'.format(after.content),inline = False)
            embed.add_field(name = 'Channel:',value ='{}'.format(before.channel.name),inline = False)
            embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
            await bot.send_message(channel, embed=embed)
         
@bot.event
async def on_reaction_add(reaction, user):
  for channel in user.server.channels:
    if channel.name == '📡electro-logs':
        logchannel = channel
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_author(name='REACTION ADDED')
        embed.add_field(name = 'Reaction by:',value ='{}'.format(user.name),inline = False)
        embed.add_field(name = 'Message:',value ='{}'.format(reaction.message.content),inline = False)
        embed.add_field(name = 'Channel:',value ='{}'.format(reaction.message.channel.name),inline = False)
        embed.add_field(name = 'Emoji:',value ='{}'.format(reaction.emoji),inline = False)
        embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
        await bot.send_message(logchannel,  embed=embed)
        
@bot.event
async def on_reaction_remove(reaction, user):
  for channel in user.server.channels:
    if channel.name == '📡electro-logs':
        logchannel = channel
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_author(name='REACTION REMOVED')
        embed.add_field(name = 'Reaction by:',value ='{}'.format(user.name),inline = False)
        embed.add_field(name = 'Message:',value ='{}'.format(reaction.message.content),inline = False)
        embed.add_field(name = 'Channel:',value ='{}'.format(reaction.message.channel.name),inline = False)
        embed.add_field(name = 'Emoji:',value ='{}'.format(reaction.emoji),inline = False)
        embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
        await bot.send_message(logchannel,  embed=embed)   
        
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    channel = bot.get_channel('543425282195980294')
    if message.server is None and message.author != bot.user:
    	 check = '✅'
    	 await bot.add_reaction(message, check)
    	 r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    	 embed=discord.Embed(title=f"{message.author.name}", description=f"{message.content}", color = discord.Color((r << 16) + (g << 8) + b))
    	 embed.set_thumbnail(url= message.author.avatar_url)
    	 await bot.send_message(channel, '{} ID: {}'.format(message.author, message.author.id))
    	 embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
    	 await bot.send_message(channel, embed=embed)  
    	 
@bot.event
async def on_member_unban(guild, user):
	for channel in user.server.channels:
		if channel.name == '📡electro-logs':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
			embed.set_author(name='USER UNBANNED')
			embed.add_field(name = 'User Name:',value ='{}'.format(user.name),inline = False)
			embed.add_field(name = 'User ID:',value ='{}'.format(user.id),inline = False)
			embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
			await bot.send_message(logchannel,  embed=embed)
			
@bot.event
async def on_member_ban(guild, user):
	for channel in user.server.channels:
		if channel.name == '📡electro-logs':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
			embed.set_author(name='USER BANNED')
			embed.add_field(name = 'User Name:',value ='{}'.format(user.name),inline = False)
			embed.add_field(name = 'User ID:',value ='{}'.format(user.id),inline = False)
			embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
			await bot.send_message(logchannel,  embed=embed)	
			
@bot.event
async def on_message_delete(message):
	for channel in user.server.channels:
		if channel.name == '📡electro-logs':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
			embed.set_author(name='MESSAGE DELETED')
			embed.add_field(name = 'Message Author:',value ='{}'.format(message.author),inline = False)
			embed.add_field(name = 'Message:',value ='{}'.format(message.content),inline = False)
			embed.add_field(name = 'Channel:',value ='{}'.format(message.channel.name),inline = False)
			embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
			await bot.send_message(logchannel,  embed=embed)
			
@bot.event
async def on_guild_join(guild):
		if channel.name == '📡electro-server-joins':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
			embed.set_author(name='IM IN A NEW SERVER')
			embed.add_field(name = 'Server Name:',value ='{}'.format(guild.name),inline = False)
			embed.add_field(name = 'Membercount',value ='str(len(guild.members))',inline = False)
			embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
			await bot.send_message(logchannel,  embed=embed)		
			
@bot.event
async def on_guild_remove(guild):
		if channel.name == '📡electro-server-joins':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
			embed.set_author(name='I WAS REMOVED FROM A SERVER')
			embed.add_field(name = 'Server Name:',value ='{}'.format(guild.name),inline = False)
			embed.add_field(name = 'Membercount',value ='str(len(guild.members))',inline = False)
			embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
			await bot.send_message(logchannel,  embed=embed)
			
@bot.event
async def on_guild_role_create(role):
	for channel in user.server.channels:
		if channel.name == '📡electro-logs':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
			embed.set_author(name='ROLE CREATED')
			embed.add_field(name = 'Role Name:',value ='{}'.format(role.name),inline = False)
			embed.add_field(name = 'Role ID:',value ='{}'.format(role.id),inline = False)
			embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
			await bot.send_message(logchannel,  embed=embed)
			
@bot.event
async def on_guild_role_delete(role):
	for channel in user.server.channels:
		if channel.name == '📡electro-logs':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
			embed.set_author(name='ROLE CREATED')
			embed.add_field(name = 'Role Name:',value ='{}'.format(role.name),inline = False)
			embed.add_field(name = 'Role ID:',value ='{}'.format(role.id),inline = False)
			embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
			await bot.send_message(logchannel,  embed=embed)	
			
@bot.event
async def on_guild_channel_create(channel):
	for channel in user.server.channels:
		if channel.name == '📡electro-logs':
			logchannel = channel
			r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
			embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
			embed.set_author(name='CHANNEL CREATED')
			embed.add_field(name = 'Channel Name:',value ='{}'.format(channel.name),inline = False)
			embed.add_field(name = 'Channel ID:',value ='{}'.format(channel.id),inline = False)
			embed.set_footer(text ='Made with ❤ by @ADIB HOQUE#6969')
			await bot.send_message(logchannel,  embed=embed)								
								 
bot.run(os.getenv('Token'))
