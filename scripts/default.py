from scripts.dbManager import dbHandeler
def checkBanWords(message,guildID):
    """
        Simple funtion that check if the message contains any ban words.
    """

    banWords = dbHandeler().fetchBanWords(guildID)

    for word in banWords:
        word = word.lower()
        if word in message:
            
            return True
    return False

def checkModRole(ctx):
    
    guildID = ctx.guild.id

    data=dbHandeler().fetchGuildDetails(guildID)

    modRoleID = data["modRoleID"]
    if modRoleID == None:
        return None
    

    for role in ctx.author.roles:
        if role.id == modRoleID:
            return True
    
    return False