import sqlite3
import shutil
class dbHandeler():
    
    def __init__(self):

        self.connection = sqlite3.connect("./data/heathens.db")
        self.cursor = self.connection.cursor()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS guildDetails(
                    guildName TEXT,
                    guildID TEXT,
                    prefix TEXT,
                    modRoleID TEXT,
                    welcomeByeChannelID TEXT,
                    kickBanChannelID TEXT,
                    instaFeedChannel TEXT,
                    lastInstaRefresh REAL,
                    autoRefreshTime INTEGER

            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS banWords(
                    banWord TEXT,
                    guildID TEXT                 

            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS instaUserNames(
                    userName TEXT,
                    guildID TEXT,
                    listFetchedPostID  TEXT

            )
        """)

        self.connection.commit()

    def closeDB(self):
        
        """Simply closes database connection"""
        self.connection.commit()
        self.connection.close()
        return

    def insertGuildDetails(self,guildName=None,guildID=None,prefix = ".",modRoleID=None,welcomeByeChannelID=None,kickBanChannelID=None,instaFeedChannel = None,lastInstaRefresh = None,autoRefreshTime=None):
        """
            Insert values to guildDetails Table. If some values are not passes stores None.
        """
        self.cursor.execute(""" INSERT INTO guildDetails Values(?,?,?,?,?,?,?,?,?) """,(guildName,guildID,prefix,modRoleID,welcomeByeChannelID,kickBanChannelID,instaFeedChannel,lastInstaRefresh,autoRefreshTime))
        self.connection.commit()

        return

    def fetchGuildDetails(self,guildID):
        """
            Fetches all the data from guildDetails Table where value of guildID matches. Return in form of dict.
        """
        self.cursor.execute("SELECT * FROM guildDetails WHERE guildID = :guildID",{"guildID":guildID})

        data = self.cursor.fetchall()

        dataReturn = dict()
        dataReturn["guildName"] = data[0][0]
        dataReturn["prefix"] = data[0][2]


        try:        
            dataReturn["guildID"] = int(data[0][1])
        except:
            dataReturn["guildID"] = (data[0][1])
        try:
            dataReturn["modRoleID"] = int(data[0][3])
        except:
            dataReturn["modRoleID"] = (data[0][3])
        try:
            dataReturn["welcomeByeChannelID"] = int(data[0][4])
        except:
            dataReturn["welcomeByeChannelID"] = (data[0][4])
        try:
            dataReturn["kickBanChannelID"] = int(data[0][5])
        except:
            dataReturn["kickBanChannelID"] = (data[0][5])
        try:
            dataReturn["instaFeedChannel"] = int(data[0][6])
        except:
            dataReturn["instaFeedChannel"] = (data[0][6])
        try:
            dataReturn["lastInstaRefresh"] = float(data[0][7])
        except:
            dataReturn["lastInstaRefresh"] = (data[0][7])
        try:
            dataReturn["autoRefreshTime"] = int(data[0][8])
        except:
            dataReturn["autoRefreshTime"] = (data[0][8])


        return dataReturn

    def updateGuildDetails(self,guildName=None,guildID=None,modRoleID=None,welcomeByeChannelID=None,kickBanChannelID=None,instaFeedChannel = None,lastInstaRefresh = None,autoRefreshTime = None):
        """
            Updated only the value that has been passes where value of guildID matches to guildDetails Table.
        """
        
        if guildName != None:

            self.cursor.execute("""UPDATE guildDetails SET
                guildName = :guildName

                WHERE guildID = :guildID

            """,{
                "guildName":guildName,
                "guildID":guildID,
            })
        
        if modRoleID != None:

            self.cursor.execute("""UPDATE guildDetails SET
                modRoleID = :modRoleID

                WHERE guildID = :guildID

            """,{
                "modRoleID":modRoleID,
                "guildID":guildID,
            })
        
        if welcomeByeChannelID != None:

            self.cursor.execute("""UPDATE guildDetails SET
                welcomeByeChannelID = :welcomeByeChannelID
                WHERE guildID = :guildID

            """,{
                "welcomeByeChannelID": welcomeByeChannelID,
                "guildID":guildID,
            })
        
        if kickBanChannelID != None:

            self.cursor.execute("""UPDATE guildDetails SET
                kickBanChannelID = :kickBanChannelID

                WHERE guildID = :guildID

            """,{
                "kickBanChannelID":kickBanChannelID,
                "guildID":guildID,
            })
        
        if instaFeedChannel != None:

            self.cursor.execute("""UPDATE guildDetails SET
                instaFeedChannel = :instaFeedChannel

                WHERE guildID = :guildID

            """,{
                "instaFeedChannel":instaFeedChannel,
                "guildID":guildID,
            })
        
        if lastInstaRefresh != None:

            self.cursor.execute("""UPDATE guildDetails SET
                lastInstaRefresh = :lastInstaRefresh

                WHERE guildID = :guildID

            """,{
                "lastInstaRefresh":lastInstaRefresh,
                "guildID":guildID,
            })
        if autoRefreshTime != None:

            self.cursor.execute("""UPDATE guildDetails SET
                autoRefreshTime = :autoRefreshTime

                WHERE guildID = :guildID

            """,{
                "autoRefreshTime":autoRefreshTime,
                "guildID":guildID,
            })

        self.connection.commit()

        return

    def deleteGuildDetails(self,guildID):
        """
            Deletes data from guildDetails Table where value of guildID matches.
        """
        self.cursor.execute("DELETE FROM guildDetails WHERE guildID= :guildID ",{
            "guildID":guildID
        })
        self.connection.commit()

        return

    def insertBanWords(self,guildID,banWord):
        """
            Inserts banWord into banWords Table along with its corresponding guildID.
        """
        
        self.cursor.execute("INSERT INTO banWords VALUES(?,?) ",(banWord,guildID))
        self.connection.commit()
        
        return

    def fetchBanWords(self,guildID):
        """
            Fetches all the badWord form banWords Table where corresponding guildID matches. Returns list of banWord.
        """

        self.cursor.execute("SELECT * FROM banWords WHERE guildID = :guildID",{"guildID":guildID})

        data = self.cursor.fetchall()
        
        banWords = list()
        for word in data:
            banWords.append(word[0])

        return banWords

    def deleteBanWords(self,guildID,banWord=None):
        """
            Deletes All or one banWord form banWords Table. \nIf banWord is not passes it deletes all the banWord from the table.
            Whereas if banWord is passes it only deletes that specific banWord from the table where the corresponding guildID matches.
        """
        if banWord == None:
            self.cursor.execute("DELETE FROM banWords WHERE guildID= :guildID ",{
                "guildID":guildID
            })
        else:
            self.cursor.execute("DELETE FROM banWords WHERE guildID= :guildID AND banWord= :banWord",{
                "guildID" :guildID,
                "banWord":banWord
            })
        self.connection.commit()

        return
    
    def insertInstaUserName(self,guildID,userName,listFetchedPostID=None):
        """
            Inserts userName into instaUserNames Table along with its corresponding guildID.
        """
        
        self.cursor.execute("INSERT INTO instaUserNames VALUES(?,?,?) ",(userName,guildID,listFetchedPostID))
        self.connection.commit()
        
        return

    def fetchInstaUserName(self,guildID):
        """
            Fetches all the userName form instaUserNames Table where corresponding guildID matches.
            Returns: 
            'usernames' : list of username,
            'usernames 1' : lastFetchedPostID 1,
            'usernames 2' : lastFetchedPostID 2,
            'usernames 3' : lastFetchedPostID 3,
            'usernames 4' : lastFetchedPostID 4

            so on.
        """

        self.cursor.execute("SELECT * FROM instaUserNames WHERE guildID = :guildID",{"guildID":guildID})

        data = self.cursor.fetchall()

        userNames = list()
        returnData = dict()

        returnData['usernames'] = userNames

        
        for tupl in data:
            #(username,guildid,listFetchedPostID)
            
            userName = tupl[0]
            postID = tupl[2]
            #Update list of username
            userNames.append(userName)

            returnData[userName] = None
            if postID != None:
                #'str(postID)?str(postID2)?str(postID3)?str(postID4)'
                postIDs=postID.split("?")
                listOfPostID = list()                
                for postID in postIDs:
                    try:
                        listOfPostID.append(int(postID))
                    except ValueError:
                        pass
                pass
                
                returnData[userName] = listOfPostID


        return returnData

    def updatePostID(self,guildID,userName,listFetchedPostID):
        """
            Funtions updates list of last fetched post id to database with its corresponding guildID and userName.
            If listFetchedPostID passed with something else then type list , returns False.
            Else converts list to string and updates DB.
        """

        # checking if list of fetched post is list class or not
        if type(listFetchedPostID) is not list:
            return False

        #fetch already stored list of fetched post
        storedList = self.fetchInstaUserName(guildID)
        storedList = storedList[userName]
        
        # checking if list not empty
        if storedList != None:
            # merge both list
            for post in storedList:
                listFetchedPostID.append(post)
            pass



        # check if len is higher then 10 if it its make it 10(remove from last)

        for post in listFetchedPostID:
            if len(listFetchedPostID) > 10:
                shutil.rmtree(f"./lib/postFiles/{listFetchedPostID[len(listFetchedPostID)-1]}")
                listFetchedPostID.remove(listFetchedPostID[len(listFetchedPostID)-1])
        
        # change list back to str form ie. "123?123?123?123"
        strList = str()
        for post in listFetchedPostID:
            strList += str(post) + "?"



        self.cursor.execute("""
                UPDATE instaUserNames SET
                listFetchedPostID = :listFetchedPostID
                
                WHERE userName = :userName AND guildID = :guildID


            """,{
                "userName": userName,
                "guildID":guildID,
                "listFetchedPostID" : strList
                #"listFetchedPostID" : None
            })

        self.connection.commit()
        return True

    def deleteInstaUserName(self,guildID,userName=None):
        """
            Deletes All or one userName form instaUserNames Table. \nIf userName is not passes it deletes all the userName from the table.
            Whereas if userName is passes it only deletes that specific userName from the table where the corresponding guildID matches.
        """
        # fetch stored list of post id and usernames
        data = self.fetchInstaUserName(guildID)
        usernames = data['usernames']

        if userName == None:
            # For deleting all the usernames and files


            for username in usernames:
                listPostID = data[username]
                for postID in listPostID:
                    try:
                        shutil.rmtree(f"./lib/postFiles/{(postID)}")
                    except Exception as e:
                        print(e, "Does not exist")

            self.cursor.execute("DELETE FROM instaUserNames WHERE guildID= :guildID ",{
                "guildID":guildID
            })

        else:

            # For deleting passed the usernames and files]
            listPostID = data[userName]
            for postID in listPostID:
                try:
                    shutil.rmtree(f"./lib/postFiles/{(postID)}")
                except Exception as e:
                    print(e,"Does not exist")
            self.cursor.execute("DELETE FROM instaUserNames WHERE guildID= :guildID AND userName= :userName",{
                "guildID" :guildID,
                "userName":userName
            })
        self.connection.commit()

        return
    
    def updatePostIDRAW(self,guildID,userName,listFetchedPostID):
        self.cursor.execute("""
            UPDATE instaUserNames SET
            listFetchedPostID = :listFetchedPostID
            
            WHERE userName = :userName AND guildID = :guildID


        """,{
            "userName": userName,
            "guildID":guildID,
            "listFetchedPostID" : listFetchedPostID
            #"listFetchedPostID" : None
        })

        self.connection.commit()
        return
    pass



"""guildID = 968415871276040192
userName= "thatnepseguy"
listFetchedPostID= None
#listFetchedPostID= 12312132132151

print(dbHandeler().deleteInstaUserName(guildID,userName))
"""