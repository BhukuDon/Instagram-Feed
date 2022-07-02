from scripts.defines import getCreds,makeAPICall

"""https://graph.facebook.com/v3.2/17841405309211844?
    fields=business_discovery.username(bluebottle){followers_count,media_count,media{comments_count,like_count}}
    &access_token={access-token}"""

def getPost( params,userName):
    
    """
        Takes params : parameter and username. Returns post of passes username in dict nested in list form.
    """

    endpointParams = dict()

    feild = "business_discovery.username({userName})".format(userName = userName)

    #endpointParams['fields'] = feild +"{followers_count,media_count,media{id,caption,timestamp,username,media_product_type,media_type,permalink,media_url,children{media_url}}}"
    
    endpointParams['fields'] = feild +"{profile_picture_url,name,media{id,caption,name,timestamp,media_type,permalink,media_url,children{media_url,media_type}}}"
    endpointParams['access_token'] = params['access_token']



    url = params['endpoint_base'] + params["instagram_account_id"] + "?"

    return makeAPICall(url,endpointParams,params['debug'])

def run():


    params= getCreds()
    params['debug'] = 'yes'
    response = getPost(params,"food.nepal")

    posts = response['json_data']['business_discovery']['media']['data']

    for num in range(0,5):
        post  = posts[num]
        #print (post)
        print("\n------------------START-----------------------")
        
        #print("\nPost No. :" , post["id"], "of Username :",post["username"])
        print("\n\tTimestamp :" , post["timestamp"])
        
        
        #print("\n\tMedia Product Type :" , post["media_product_type"])
        
        print("\n\tMedia Type :" , post["media_type"])
        
        print("\n\tPost Link :" , post["permalink"])

        try:
            print("\n\tPost Caption :" , post["caption"])
        except:
            print("\n\tPost Caption :" , None)

        
        if post['media_type'] == "CAROUSEL_ALBUM":

            post_num=0

            for childrenPost in post['children']['data']:
                post_num += 1
                print(f"\n\tMedia URL (Picture No. {post_num}):" , childrenPost["media_url"])
        
        else:
            print("\n\tMedia URL :" , post["media_url"])
        

        print("\n------------------END-----------------------")
        
#run()



def getStories(params):
    #GET /{ig-user-id}/stories

    endpointParams = dict()

    endpointParams['fields'] = "business_discovery.username(sushant_pradhan_){username,stories}"
    endpointParams['access_token'] = params['access_token']



    url = params['endpoint_base'] + params["instagram_account_id"] + "/stories"

    return makeAPICall(url,endpointParams,params['debug'])

"""params= getCreds()
#params['debug'] = 'yes'
response = getStories(params)"""