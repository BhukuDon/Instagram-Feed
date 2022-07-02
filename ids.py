from scripts.defines import getCreds,makeAPICall

def getUserPagesInfo(params):
    endpointParams = dict()
    endpointParams['access_token'] = params['access_token']

    url = params['endpoint_base']+ "me/accounts?"

    return makeAPICall(url,endpointParams,params['debug'])

"""params = getCreds()
params['debug'] = 'yes'
response = getUserPagesInfo(params)

print("\n Page Name : "+ response['json_data']['data'][0]['name'])
print("\n Page ID : "+ response['json_data']['data'][0]['id'])"""

def getInstagramAccountInfo(params):

    endpointParams = dict()
    endpointParams['access_token'] = params['access_token']
    endpointParams['fields'] = "instagram_business_account"


    url = params['endpoint_base'] + params["page_id"] + "?"

    return makeAPICall(url,endpointParams,params["debug"])


params = getCreds()
#params['debug'] = 'yes'
response = getInstagramAccountInfo(params)


print("\n Instagram Account ID : "+ response['json_data']['instagram_business_account']['id'])