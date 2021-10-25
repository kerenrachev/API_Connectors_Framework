
import requests
import base64
from Errors import errorsPrinter
class Url(object):

    url          = None
    isMalicious  = None
    RelevantData = None

    def __init__(self,url):
        self.url = url
    # Scanning the given url with the VirusTotal API
    # If some error has accured, we will try to finish this file in the next interval and will not mark it as ".done"
    def scanURLwithVT(self,api_url,headers,fileName):
        try:
            postResponse = requests.post(api_url, headers= headers, data = {'url': self.url.rstrip()})
            if postResponse.status_code != 200:
                errPrinter = errorsPrinter(postResponse.status_code, self.url, fileName)
                err = errPrinter.returnErrorMessage()
                return 0,err
            encoded_url               = base64.b64encode(self.url.encode())
            getResponse              = requests.get(api_url + '/{}'.format(encoded_url.decode().replace('=', '')),headers=headers).json()
            reputation                = getResponse['data']['attributes']['reputation']
            self.reputationChecker(reputation,getResponse)
        except Exception as e: 
            err = 'An exception has accured while trying to make a get/post request.' +str(e)
            return 0,err
        return 1,None
            
    # Adding searialized data to the malicious urls
    def reputationChecker(self,reputation,JSONresponse):
        if( reputation < 0 ):
            self.isMalicious = True
            self.RelevantData = {
                'Analysis': {
                    'harmless'      : JSONresponse['data']['attributes']['last_analysis_stats']['harmless'  ],
                    'malicious'     : JSONresponse['data']['attributes']['last_analysis_stats']['malicious' ],
                    'suspicious'    : JSONresponse['data']['attributes']['last_analysis_stats']['suspicious'],
                    'timeout'       : JSONresponse['data']['attributes']['last_analysis_stats']['timeout'   ],
                    'undetected'    : JSONresponse['data']['attributes']['last_analysis_stats']['undetected'],
                },
                'Reputation': { reputation, } 
            }
        else:
            self.isMalicious = False
