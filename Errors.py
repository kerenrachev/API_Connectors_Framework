
class errorsPrinter(object):

    status_code  = None
    url          = None
    fileName     = None
    errorMessage = None

    def __init__(self,status_code, url, fileName):
        self.status_code = status_code
        self.url         = url
        self.fileName    = fileName

    # Returns an error message depending on the "status_code" of the get/post request 
    # Can add more error messages, depending on the "status_code"
    def returnErrorMessage(self):
        message = 'ERROR - status code ' + str(self.status_code) + ' in file - "'+self.fileName+'" '
        if( self.status_code == 400):
            message += 'url -"'+self.url.strip()+'" is not valid.'
        if( self.status_code == 429):
            message += ' TO MANY REQUESTS to the VirusTotal service. Try again later.'
        return message
