from scripts.defines import getCreds,makeAPICall
import datetime
def getLongLivedAccessToken( params ):
    endpointParams = dict()

    endpointParams['grant_type'] = 'fb_exchange_token'
    endpointParams['client_id'] = params['app_id']
    endpointParams['client_secret'] = params['app_secret']
    endpointParams['fb_exchange_token'] = params['access_token']


    url = params['endpoint_base']+'oauth/access_token'

    return makeAPICall(url,endpointParams,params['debug'])

"""params= getCreds()
params['debug'] = 'yes'
response = getLongLivedAccessToken(params)

print("\n -------- Access Token -----------")
print("\n")
print(response['json_data']['access_token'])"""


def debugAccessToken( params ):

    endpointParams = dict()
    endpointParams['input_token'] = params['access_token']

    endpointParams['access_token'] = params['access_token']

    url = params['graph_domain'] + '/debug_token?'

    return makeAPICall(url ,endpointParams,params['debug'])

"""params= getCreds()
params['debug'] = 'yes'
response = debugAccessToken(params)
print("Data Access Expires At : ",(datetime.datetime.fromtimestamp(response["json_data"]["data"]["data_access_expires_at"])))
print("Access Token Expires At : ",(datetime.datetime.fromtimestamp(response["json_data"]["data"]["expires_at"])))"""