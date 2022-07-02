import urllib.request
import os
import discord
import json
import discord.utils
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
from matplotlib.pyplot import get
from scripts.access_token import getLongLivedAccessToken,debugAccessToken
from scripts.defines import getCreds
from getMedia import getPost
import random
import datetime
import time
from scripts.dbManager import dbHandeler
from scripts.default import checkBanWords,checkModRole
from scripts.bitly import shortURL
# fetching config
with open ("config.json","r") as read_config:
    Config = json.load(read_config)
read_config.close()

prefix= '.'
Token = Config['Discord-Token']

Client = commands.Bot(command_prefix=prefix,help_command=None)

##### Events #####


# on event when the bot is ready
@Client.event
async def on_ready():
    print(("I {username} am ready and online on following Servers:").format(username = Client.user))
    
    
    #for every server 
    async for guild in Client.fetch_guilds(limit=150):
        print(guild.name)

    changePresence.start()
    return
    
# on event when message send on guild
@Client.event
async def on_message(message):
    # checking if we made that message
    if message.author == Client.user:
        return
    await Client.process_commands(message)

    # checking if message contains any ban words
    if checkBanWords(message.content,message.guild.id) == True:
        await message.delete()
        await message.channel.send("Bad Boy / Girl!!")
        return
    return

# on event when command error occurs
@Client.event
async def on_command_error(ctx,error):

    if isinstance(error,commands.MissingPermissions):
        await ctx.send("Permission Missing.")
        await ctx.message.delete()
    
    #if isinstance(error,commands.CommandInvokeError):
    #    await ctx.send("{member} Bot Permission Missing".format(member = ctx.author.mention))
    #    await ctx.message.delete()
    else:
        raise error

@Client.event
async def on_guild_join(guild):
    print("Joined:")

    print(guild.name)
    print(guild.id)

    dbHandeler().insertGuildDetails(guildName=guild.name,guildID=guild.id)

@Client.event
async def on_guild_remove(guild):

    print("Left :")
    print(guild.name)
    print(guild.id)

    dbHandeler().deleteGuildDetails(guild.id)
    dbHandeler().deleteBanWords(guild.id)

@Client.event
async def on_member_join(member):
    pass

@Client.event
async def on_member_remove(member):
    pass

##### Commands #####

@Client.command(aliases =[ "Ping","PING"])
async def ping(ctx):
        """
        Ping command. Returns Latency
        """
        await ctx.channel.send("Pong🏓 -> {ping}ms".format(ping=round(Client.latency,1)))
    
@Client.command(aliases=["HELP","Help"])
async def help(ctx,*,arg=None):
    """
        Help command.
    """
    if arg == None:
        #list out all the help commands.
        return
    if arg == "command" or arg == "commands":
        # list available commands
        command = """
            1. {prefix}help - Help command.
            2. {prefix}help command - List of available command.
            3. {prefix}ping - Shows Bot latency.
        """.format(prefix = prefix)
        await ctx.send("{member} \n {command}".format(member=ctx.author.mention,command=command))
        return

# Needs Optimization    
@tasks.loop(minutes=3)
async def changePresence():
    """
        Changes discord presence form random list of presence every 2 mins.
    """

    # get access token info
    params= getCreds()
    
    response = debugAccessToken(params)
    dataAccessExpiresTimestamp=(datetime.datetime.fromtimestamp(response["json_data"]["data"]["data_access_expires_at"]))
    accessTokenExpiresTimestamp=(datetime.datetime.fromtimestamp(response["json_data"]["data"]["expires_at"]))

    

    now = datetime.datetime.now()

    time_diff = str(dataAccessExpiresTimestamp-now)
    
    dataAccessExpiresTime=dict()

    dataAccessExpiresTime["days"] = str(int(((time_diff.split(","))[0]).split()[0]))
    dataAccessExpiresTime["hour"] = str(int((((time_diff.split(","))[1]).split(":"))[0]))
    dataAccessExpiresTime["min"] = str(int((((time_diff.split(","))[1]).split(":"))[1]))

    time_diff = str(accessTokenExpiresTimestamp-now)
    
    accessTokenExpiresTime=dict()
    accessTokenExpiresTime["days"] = str(int(((time_diff.split(","))[0]).split()[0]))
    accessTokenExpiresTime["hour"] = str(int((((time_diff.split(","))[1]).split(":"))[0]))
    accessTokenExpiresTime["min"] = str(int((((time_diff.split(","))[1]).split(":"))[1]))


    accessTokenExpires = accessTokenExpiresTime['days'] + " days"
    if accessTokenExpiresTime['days'] == 0:
        if accessTokenExpiresTime['hour'] == 0:
            accessTokenExpires = accessTokenExpiresTime['min'] + " minutes"

        accessTokenExpires = accessTokenExpiresTime['hour'] + "hours"

    dataAccessExpires = dataAccessExpiresTime['days'] + " days"
    if dataAccessExpiresTime['days'] == 0:
        if dataAccessExpiresTime['hour'] == 0:
            dataAccessExpires = dataAccessExpiresTime['min'] + " minutes"

        dataAccessExpires = dataAccessExpiresTime['hour'] + "hours"


    listOfPresence = {
        "1":" Bhuku_Don#4268",
        "2":"Playing with Graph API",
        "3":"{} left for Access Token to expire".format(accessTokenExpires),
        "4":"{} left for Data Access".format(dataAccessExpires),
        "5":".help Default Prefix (.)"
    }
    num = random.randrange(1,5)

    await Client.change_presence(status=discord.Status.online, activity=discord.Game(name=listOfPresence[str(num)]))

    return

@tasks.loop(minutes=30)
async def autoRefresh(ctx):
    # check time refresh time 
    print("Refreshing")
    await instafeed(ctx,'refresh')
    return
    
@Client.command(aliases=["ClearChat","CLEARCHAT"])
async def clearchat(ctx,*,arg=None):
    
    #check if author has mod role or not
    response = checkModRole(ctx)
    
    # if mod role has not been setuped
    if response == None:
        await ctx.send("The bot has not been setuped to use Mod Commands.")
        await ctx.send("The owner has to use ({prefix}setup mod).".format(prefix=prefix))
        return


    # if author doesnot have mod role
    if response == False:
        
        roleID = dbHandeler().fetchGuildDetails(ctx.guild.id)
        roleID = roleID["modRoleID"]
        role = discord.utils.get(ctx.guild.roles , id = roleID)

        await ctx.send("{mention} You do not have Bot Mod Role. You need {role} role to use any Mod commands.".format(mention = ctx.author.mention,role = role.name))
        return

    # if limit number not pass delete all message
    if arg == None:

        await ctx.channel.purge()
        await ctx.channel.send("{mention} The chat has been cleared.".format(mention = ctx.author.mention))
        return
    
    # if limit number has passed only delete passed number of messages
    try:
        delNum = int(arg)

    except:
        await ctx.send("{mention} Syntax error! \n {prefix}clearchat (number)".format(mention = ctx.author.mention,prefix = prefix))
        return

    else:
        await ctx.channel.purge(limit=delNum)
        await ctx.channel.send("{mention} {number} message has been deleted from the chat.".format(mention = ctx.author.mention,number = delNum))


    return

@Client.command(aliases = ["Setup","SETUP"])
async def setup(ctx,*,arg=None):
    if arg == None:
        await ctx.send("Invalid Syntax TEST!!")
    """
    Setup your discord bot.
    """

    if arg.lower() == "mod":

        roleName = "Zen Z Mod"
        guild=ctx.guild

        # if message sender is not the owner.
        if guild.owner_id != ctx.author.id:
            
            await ctx.send("{mention} You are not the owner. I can only be setuped by the owner.".format(mention=ctx.author.mention))
            return

        # check if role with same name has already been created and delete
        # Cannot delete unless the user shifts bot above role to be deleted ( Needs to be fixed )
        """for role in ctx.guild.roles:
            if role.name == roleName:
                await role.delete()"""


        role = await guild.create_role(name=roleName)
        
        await ctx.send("Created A new role named {name}".format(name=roleName))

        await ctx.send("This role is essential for members in order for them to use Bot Mod Commands.")


        dbHandeler().updateGuildDetails(guildID=guild.id,modRoleID=role.id)    

        return
    
    if arg.lower() == "welcome":
        
        
        pass

    if arg.lower() == "ban":
        pass
    
    if arg.lower() == "instafeed":
        await ctx.send("Choose a channel to post insta feed.")

        def check(m):
            # to check if the response is of author or not
            return m.author.id == ctx.author.id

        try:
            channel = await Client.wait_for("message",timeout=30,check=check)
            channel = (channel.content)

        except:
            await ctx.send("{mention} You didn't reply on time.".format(mention = ctx.author.mention))
            return

        channelID = int(channel[:-1][2:])
        for channels in Client.get_all_channels():
            if (channelID) == (channels.id):
                checkChannel = True
                break
            checkChannel = False 
            
        if checkChannel == False:
            await ctx.send("{mention} Channel not found ".format(mention = ctx.author.mention))
            return
            
        channelOBJ = Client.get_channel(channelID)
        dbHandeler().updateGuildDetails(guildID=ctx.guild.id,instaFeedChannel=channelID)
        await ctx.send("{mention} Sucessfully added {channel} channel.".format(mention = ctx.author.mention,channel = channelOBJ.mention))

        return
    return

@Client.command(aliases = ["BANWORD","BanWord"])
async def banword(ctx,keyword,*,arg=None):
    
    if keyword.lower() == "list":
        #list all the ban words
        data = dbHandeler().fetchBanWords(ctx.guild.id)
        
        # if emply send emply message:
        if len(data) == 0:
            await ctx.send("{mention} No ban words found.".format(mention = ctx.author.mention ))

            return
        
        banWords = str()

        for words in data:
            banWords += words+"\n"

        await ctx.send("{mention} Following are the ban words: \n {words}".format(mention = ctx.author.mention , words = banWords))

        return
    
    if keyword.lower() == "add":
        # check has mod role
        response = checkModRole(ctx)
    
            # if mod role has not been setuped
        if response == None:
            await ctx.send("The bot has not been setuped to use Mod Commands.")
            await ctx.send("The owner has to use ({prefix}setup mod).".format(prefix=prefix))
            return

            # if author doesnot have mod role
        if response == False:
            
            roleID = dbHandeler().fetchGuildDetails(ctx.guild.id)
            roleID = roleID["modRoleID"]
            role = discord.utils.get(ctx.guild.roles , id = roleID)

            await ctx.send("{mention} You do not have Bot Mod Role. You need {role} role to use any Mod commands.".format(mention = ctx.author.mention,role = role.name))
            return

        
        # check if syntax corret

        if arg == None:

            await ctx.send("{mention} Syntax Error:\n {prefix}banword add (word)".format(mention = ctx.author.mention,prefix= prefix ))
            return
        
        try :
            arg  = str(arg)
        except:
            await ctx.send("{mention} Syntax Error:\n {prefix}banword add (word)".format(mention = ctx.author.mention,prefix= prefix ))
            return
        # check if already exist

        data = dbHandeler().fetchBanWords(ctx.guild.id)
        for word in data:
            if word == arg:

                await ctx.send("{mention} Ban word '{word}' already exists.".format(mention = ctx.author.mention,word=arg ))
                return
        # add keyword

        dbHandeler().insertBanWords(ctx.guild.id,arg)
        await ctx.send("{mention} Ban word '{word}' added.".format(mention = ctx.author.mention,word=arg ))
        return
    
    if keyword.lower() == "del" or keyword.lower() == "delete":
        # check has mod role
        response = checkModRole(ctx)
    
            # if mod role has not been setuped
        if response == None:
            await ctx.send("The bot has not been setuped to use Mod Commands.")
            await ctx.send("The owner has to use ({prefix}setup mod).".format(prefix=prefix))
            return

            # if author doesnot have mod role
        if response == False:
            
            roleID = dbHandeler().fetchGuildDetails(ctx.guild.id)
            roleID = roleID["modRoleID"]
            role = discord.utils.get(ctx.guild.roles , id = roleID)

            await ctx.send("{mention} You do not have Bot Mod Role. You need {role} role to use any Mod commands.".format(mention = ctx.author.mention,role = role.name))
            return

        
        # check if syntax corret

        if arg == None:

            await ctx.send("{mention} Syntax Error:\n {prefix}banword del (word) or (all)".format(mention = ctx.author.mention,prefix= prefix ))
            return
        
        try :
            arg  = str(arg)
        except:
            await ctx.send("{mention} Syntax Error:\n {prefix}banword del (word) or (all)".format(mention = ctx.author.mention,prefix= prefix ))
            return
        
        # delete all if arg is all    
        if arg == "ALL" or arg == "All" or arg == "all":
            
            dbHandeler().deleteBanWords(ctx.guild.id)
            await ctx.send("{mention} All the ban words has been deleted".format(mention = ctx.author.mention ))
            return
        
        # check if word exist or not

        data = dbHandeler().fetchBanWords(ctx.guild.id)

        for word in data:
            if word == arg:
                dbHandeler().deleteBanWords(ctx.guild.id,arg)
                await ctx.send("{mention} Ban word '{word}' deleted. ".format(mention = ctx.author.mention,word = arg ))
                return

        await ctx.send("{mention} Ban word '{word}' does not exist. ".format(mention = ctx.author.mention,word = arg ))

        return



    return

@Client.command(aliases = ["INSTAFEED","Instafeed"])
async def instafeed(ctx,keyword,*,arg=None):
    
    if keyword.lower() == "list":
        #list all the ban words
        data = dbHandeler().fetchInstaUserName(ctx.guild.id)

        listOfUserNames = data['usernames']

        # if emply send emply message:
        if len(listOfUserNames) == 0:
            await ctx.send("{mention} No username found.".format(mention = ctx.author.mention ))

            return
        
        userName = str()

        for names in listOfUserNames:
            userName += names+"\n"

        await ctx.send("{mention} Following are the username: \n {words}".format(mention = ctx.author.mention , words = userName))

        return
    
    if keyword.lower() == "add":
        # check has mod role
        response = checkModRole(ctx)
    
            # if mod role has not been setuped
        if response == None:
            await ctx.send("The bot has not been setuped to use Mod Commands.")
            await ctx.send("The owner has to use ({prefix}setup mod).".format(prefix=prefix))
            return

            # if author doesnot have mod role
        if response == False:
            
            roleID = dbHandeler().fetchGuildDetails(ctx.guild.id)
            roleID = roleID["modRoleID"]
            role = discord.utils.get(ctx.guild.roles , id = roleID)

            await ctx.send("{mention} You do not have Bot Mod Role. You need {role} role to use any Mod commands.".format(mention = ctx.author.mention,role = role.name))
            return

            # if instaFeed Channel has not been setuped, return

        instaFeedChannel = dbHandeler().fetchGuildDetails(ctx.guild.id)
        instaFeedChannel = instaFeedChannel['instaFeedChannel']
        if instaFeedChannel == None:
            await ctx.send("{mention} instafeed has not been setuped. Use ({prefix}setup instafeed) cmd first.".format(mention = ctx.author.mention,prefix = prefix))
            return

        # check if syntax is corret

        if arg == None:

            await ctx.send("{mention} Syntax Error:\n {prefix}instafeed add (username)".format(mention = ctx.author.mention,prefix= prefix ))
            return
        
        try :
            arg  = str(arg)
        except:
            await ctx.send("{mention} Syntax Error:\n {prefix}instafeed add (username)".format(mention = ctx.author.mention,prefix= prefix ))
            return
        # check if already username exist in DB

        data = dbHandeler().fetchInstaUserName(ctx.guild.id)
        for names in data:
            if names == arg:

                await ctx.send("{mention} Username '{word}' already exists.".format(mention = ctx.author.mention,word=arg ))
                return
        
        # add username to DB

        dbHandeler().insertInstaUserName(ctx.guild.id,arg)
        await ctx.send("{mention} Username '{word}' added.".format(mention = ctx.author.mention,word=arg ))

        
        # if this is the first time for insta feed manually fetch post
        lastInstaRefresh = dbHandeler().fetchGuildDetails(ctx.guild.id)
        lastInstaRefresh = lastInstaRefresh["lastInstaRefresh"]
        if lastInstaRefresh == None:
            await instafeed(ctx,"refresh")
            return
        
        return
    
    if keyword.lower() in ["del","delete"] :
        # check has mod role
        response = checkModRole(ctx)
    
            # if mod role has not been setuped
        if response == None:
            await ctx.send("The bot has not been setuped to use Mod Commands.")
            await ctx.send("The owner has to use ({prefix}setup mod).".format(prefix=prefix))
            return

            # if author doesnot have mod role
        if response == False:
            
            roleID = dbHandeler().fetchGuildDetails(ctx.guild.id)
            roleID = roleID["modRoleID"]
            role = discord.utils.get(ctx.guild.roles , id = roleID)

            await ctx.send("{mention} You do not have Bot Mod Role. You need {role} role to use any Mod commands.".format(mention = ctx.author.mention,role = role.name))
            return

        
        # check if syntax corret

        if arg == None:

            await ctx.send("{mention} Syntax Error:\n {prefix}instafeed del (username) or (all)".format(mention = ctx.author.mention,prefix= prefix ))
            return
        
        try :
            arg  = str(arg)
        except:
            await ctx.send("{mention} Syntax Error:\n {prefix}instafeed del (username) or (all)".format(mention = ctx.author.mention,prefix= prefix ))
            return
        
        # delete all if arg is all    
        if arg == "ALL" or arg == "All" or arg == "all":
            
            dbHandeler().deleteInstaUserName(ctx.guild.id)
            await ctx.send("{mention} All the usernames has been deleted".format(mention = ctx.author.mention ))
            return
        
        # check if word exist or not

        data = dbHandeler().fetchInstaUserName(ctx.guild.id)
        listOfUserNames = data['usernames']
        for word in listOfUserNames:
            if word == arg:
                dbHandeler().deleteInstaUserName(ctx.guild.id,arg)
                await ctx.send("{mention} Username '{word}' deleted. ".format(mention = ctx.author.mention,word = arg ))
                return

        await ctx.send("{mention} Username '{word}' does not exist. ".format(mention = ctx.author.mention,word = arg ))

        return

    if keyword.lower() in ['refresh',"ref"] :
        # fetch list of usernames
        fetchInstaUsername = dbHandeler().fetchInstaUserName(ctx.guild.id)
        listOfUserNames = fetchInstaUsername['usernames']

        # if list of usernames is empty
        if len(listOfUserNames) == 0:
            await ctx.send("{mention} No username found.".format(mention = ctx.author.mention ))

            return

        
        # Check if instafeed channel has been setuped or not channel 
        fetch = dbHandeler().fetchGuildDetails(ctx.guild.id)
        channel = fetch['instaFeedChannel']
        
        
        if channel == None:
            await ctx.send("{member}! InstaFeed channel has not been setuped. Use cmd ({prefix}setup instafeed)").format(
                member = ctx.author.mention,
                prefix = prefix
            )
            return

        # if this is the first time for posting only post latest 5 posts.
        
        for username in listOfUserNames:
            lastFetchedPostID = fetchInstaUsername[username]
            await getInstaFeedMedia(ctx.guild.id,lastFetchedPostID,username)
       
    if keyword.lower() in ["autorefresh"]:
         
        # Check if instafeed channel / refresh time and usernames added

        data = dbHandeler().fetchGuildDetails(ctx.guild.id)
        instaFeedChannel = data['instaFeedChannel']
        if instaFeedChannel == None:
            await ctx.send("{mention} Insta Feed channel hasn't been setuped.".format(mention = ctx.author.mention))
            return
        usernames = dbHandeler().fetchInstaUserName(ctx.guild.id)
        if len(usernames['usernames']) == 0:
            await ctx.send("{mention} Username not added".format(mention = ctx.author.mention))
            return

        if arg in ["true",'start']:
            autoRefresh.start(ctx)
            await ctx.send("{mention} Insta will be fetched every 30 mins.".format(mention = ctx.author.mention)) 
        if arg in ["false","stop"]:
            autoRefresh.stop()
            await ctx.send("{mention} Insta auto fetch stopped.".format(mention = ctx.author.mention)) 

    return

async def getInstaFeedMedia(guildID,lastFetchedPost,userName):

    param = getCreds()
    data = getPost(param,userName)

    # posts basic data
    postData= dict()
    posts = data['json_data']['business_discovery']['media']['data']
    postData["profilePictureURL"] = data['json_data']['business_discovery']['profile_picture_url']
    postData["profileName"] = data['json_data']['business_discovery']['name']

    postData['fileType'] = {
        "IMAGE" : ".jpg",
        "CAROUSEL_ALBUM" : ".jpg",
        "VIDEO" : ".mp4"
    }

    # if this is the first time for posting
    if lastFetchedPost == None:
        numToFetch = 5
        listOfPostID = list()
        for num in range(numToFetch):
            post = posts[numToFetch-num-1]
            postData["postID"] = post['id']
            postData["postTimestamp"] = post['timestamp']
            postData["postType"] = post['media_type']
            postData["postLink"] = post['permalink']
            postData["mediaLink"] = post['media_url']
            
            
            try: 
                postData['postCaption'] = post['caption']
            except:
                postData['postCaption'] = None
            if postData['postType'] == "CAROUSEL_ALBUM":

                postData['children'] = post['children']


            # Post to Discord 
            if postData['postType'] == 'IMAGE':
               await postInstaImage(guildID,postData)
            if postData['postType'] == 'VIDEO':
               await postInstaVideo(guildID,postData)
            if postData['postType'] == 'CAROUSEL_ALBUM':
                await postInstaCarousel(guildID,postData)

            # Collect post id
            listOfPostID.append(postData["postID"])


        # Update Post ID
        dbHandeler().updatePostID(guildID,userName,listOfPostID)
            
        #Update TimeStamp
        dbHandeler().updateGuildDetails(guildID=guildID,lastInstaRefresh=datetime.datetime.timestamp(datetime.datetime.now()))
        
        return



    # if already fetched 
    # list of insta posts to post (only posts that hasn't been fetched)
        
    # Creating new list for latest post and reverse it
    # Doing it so that it posts latests post at last
    latestPosts = list()
    listOfPostID = list()
    for post in posts:
        if int(post['id']) in lastFetchedPost:
            break
        latestPosts.append(post)
    latestPosts.reverse()

    for post in latestPosts:
        #if postid matches with the list of already fetched posts
        if int(post['id']) in lastFetchedPost:
            break

        postData["postID"] = post['id']
        postData["postTimestamp"] = post['timestamp']
        postData["postType"] = post['media_type']
        postData["postLink"] = post['permalink']
        postData["mediaLink"] = post['media_url']
        
        
        try: 
            postData['postCaption'] = post['caption']
        except:
            postData['postCaption'] = None
        if postData['postType'] == "CAROUSEL_ALBUM":
            postData['children'] = post['children']
        
        listOfPostID.append(postData["postID"])
        # Post to Discord 
        if postData['postType'] == 'IMAGE':
            await postInstaImage(guildID,postData)
        if postData['postType'] == 'VIDEO':
            await postInstaVideo(guildID,postData)
        if postData['postType'] == 'CAROUSEL_ALBUM':
            await postInstaCarousel(guildID,postData)

    # Update Post ID

    dbHandeler().updatePostID(guildID,userName,listOfPostID)
        
    #Update TimeStamp
    dbHandeler().updateGuildDetails(guildID=guildID,lastInstaRefresh=datetime.datetime.timestamp(datetime.datetime.now()))
    return

async def postInstaImage(guildID,data):
    # channels
    channel = dbHandeler().fetchGuildDetails(guildID)
    channel = Client.get_channel((channel["instaFeedChannel"]))
    
    # download image and save 
    
    # create folder
    try:
        os.mkdir("./lib/postFiles/{postID}/".format(postID = data['postID']))
    except:
        pass
    urllib.request.urlretrieve(url=data['mediaLink'], filename="./lib/postFiles/{postID}/1.jpg".format(postID = data['postID']))
    pathToImg = './lib/postFiles/{postID}/1{filetype}'.format(postID=data['postID'],filetype = data['fileType']['IMAGE'])

    em = discord.Embed(title = "Post Link",
        description = data['postCaption'],
        url = data["postLink"],
        colour = 0xDB162F) 
    em.set_author(name = data['profileName'],icon_url=data['profilePictureURL'])

    file = discord.File(pathToImg, filename="image.png")
    em.set_image(url="attachment://image.png")
    em.timestamp=(datetime.datetime.strptime(data['postTimestamp'], '%Y-%m-%dT%H:%M:%S+0000'))
    #em.set_footer(text="1 out of 1")
    await channel.send(file=file,embed=em)
    return
    
async def postInstaVideo(guildID,data):
    # channels
    channel = dbHandeler().fetchGuildDetails(guildID)
    channel = Client.get_channel((channel["instaFeedChannel"]))
    
    # download image and save 
    # create folder
    try:
        os.mkdir("./lib/postFiles/{postID}/".format(postID = data['postID']))
    except:
        pass    
    urllib.request.urlretrieve(data['mediaLink'], "./lib/postFiles/{postID}/1.mp4".format(postID = data['postID']))
    pathToVid = './lib/{postID}/1{filetype}'.format(postID=data['postID'],filetype = data['fileType']['VIDEO'])

    em = discord.Embed(title = "Post Link",
        description = data['postCaption'],
        url = data["postLink"],
        colour = 0xDB162F) 
    em.set_author(name = data['profileName'],icon_url=data['profilePictureURL'])
    em.timestamp=(datetime.datetime.strptime(data['postTimestamp'], '%Y-%m-%dT%H:%M:%S+0000'))
    url = shortURL(data['mediaLink'])
    em.add_field(name="Video Link",value=url,inline=False)
    #em.set_footer(text="1 out of 1")
    await channel.send(embed=em)
    await channel.send(url)
    return

async def postInstaCarousel(guildID,data):
    """    
    
    
    # download image and save 
    urllib.request.urlretrieve(data['mediaLink'], "./lib/{postID}/1.jpg".format(postID = data['postID']))
    pathToImg = './lib/{postID}/1{filetype}'.format(postID=data['postID'],filetype = data['fileType']['CAROUSEL_ALBUM'])


    """
    
    if data['postType'] != "CAROUSEL_ALBUM":
        return
    # channels
    channel = dbHandeler().fetchGuildDetails(guildID)
    channel = Client.get_channel((channel["instaFeedChannel"]))

    #download all media type
    carousel = data['children']['data']

    pathLib = list()

    # Store all media of carousel into a dict
    for media in carousel:
        x = dict()
        if media['media_type'] == "IMAGE":
            x['type'] = "IMAGE"
        if media['media_type'] == "VIDEO":
            x['type'] = "VIDEO"

        x['url'] = media["media_url"]
        x['path'] = None
        pathLib.append(x)

    """
    [
    {
        "type": "IMAGE",
        "url" : "1.com",
        "path": "1/1"
    },
    {
        "type": "VIDEO",
        "url" : "2.com",
        "path": "2/2"
    }
    ]
    """


    # Download and store media files
    # create folder
    try:
        os.mkdir("./lib/postFiles/{postID}/".format(postID = data['postID']))
    except:
        pass
    num = 0
    for dicts in pathLib:
        num += 1
        # For image file
        if dicts['type'] == 'IMAGE':
            path = "./lib/postFiles/{postID}/{num}{filetype}".format(postID = data['postID'],filetype = data['fileType']['IMAGE'],num=num)
        
        if dicts['type'] == 'VIDEO':
            path = shortURL(dicts['url'])
        dicts['path'] = path
        urllib.request.urlretrieve(dicts['url'], path)

        


    em = discord.Embed(title = "Post Link",
        description = data['postCaption'],
        url = data["postLink"],
        colour = 0xDB162F) 
    em.set_author(name = data['profileName'],icon_url=data['profilePictureURL'])
    for media in pathLib:
        if media['type'] == "IMAGE":
            toSkip = media['url']
            file = discord.File(media['path'],'img.png')
            break
    em.set_image(url="attachment://img.png")
    em.timestamp=(datetime.datetime.strptime(data['postTimestamp'], '%Y-%m-%dT%H:%M:%S+0000'))
    em.set_footer(text="1 out of {length}".format(length=len(pathLib)))
    await channel.send(file=file,embed=em)
    num = 2
    for media in pathLib:
        if media['url'] == toSkip:
            continue
        if media['type'] == "VIDEO":
            await channel.send("{url}\n {num} out of {length}.".format(url = media['path'],num=num,length=len(pathLib)))
        
        if media['type'] == "IMAGE":
            file  = discord.File(media['path'])

            await channel.send(file=file,content="\n {num} out of {length}.".format(num=num,length=len(pathLib)))
        
        num += 1
    return

@Client.command()
async def test(ctx,*,arg=None):
    path = "lib/postFiles/17948340982959247/1.jpg"
    file = discord.File(path)
    
    await ctx.send(file=file,content="hello")
    return



Client.run(Token) 