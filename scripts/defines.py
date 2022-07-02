
import requests
import json
def getCreds():
    creds = dict()
    creds['access_token'] = "EAAE3byLKTw0BADRecshWD5TZAlmhgwaLzWt2z0vi5U4gAvdh2rfCBoeJvfABfUarGespQN8HFRgYtQHviqlqEORTHI8nVgCCpIvKmfFiZACWz4mQXJapVGUnMOcZCtJ3laAsNIahAQpZCRSkfFsZBWSrXrkceZCOZAL6g2UOV4V0JvtI2kg7qu4"
    creds['app_id'] = "342425441292045"
    creds['app_secret'] = "6c7a37487f8e21ef1042d4ba0e149c92"
    creds['graph_domain'] = 'https://graph.facebook.com'
    creds['graph_version'] = 'v13.0'
    creds['endpoint_base'] = creds['graph_domain'] + "/" + creds['graph_version'] + "/"
    creds["debug"] = 'no'
    creds['page_id'] = "111370054908848"
    creds['instagram_account_id'] = "17841452966044299"
    return creds


def makeAPICall( url,endpointParams,debug = 'no'):
    data = requests.get(url,endpointParams)

    response = dict()
    
    response['url'] = url
    
    response["endpoint_params"] = endpointParams
    response["endpoint_params_pretty"] = json.dumps(endpointParams,indent=4)

    response['json_data'] = json.loads(data.content)
    response['json_data_pretty'] = json.dumps(response["json_data"],indent=4)

    if (debug == "yes"):
        displayAPICallData(response)

    return response

def displayAPICallData(response):

    print (" \nURL :" + response['url'])
    print ("\n Endpoint Params :" + response['endpoint_params_pretty'])
    print ("\n Response :" + response['json_data_pretty'])

    return
