from SubProcessInputOutputHandler import SubProcessInputOutputHandler
from UrlController import Url
import os

def main():
    io_mgr = SubProcessInputOutputHandler()
    connector_params = io_mgr.connector_params
    connector_result = {}
    directory = os.fsencode(connector_params.source_folder_path)
    for file in os.listdir(directory):
        filename      = os.fsdecode(file)
        if not filename.endswith(".done"):
            filePath  = connector_params.source_folder_path+'\\'+filename
            dataFile  = open(filePath, 'r')
            success,err   = readFromFile(dataFile, connector_params, connector_result,filename)
            dataFile.close()
            if(success):
                base = os.path.splitext(filename)[0]
                os.rename(filePath, connector_params.source_folder_path+'//'+ base + '.done')
            else:
                connector_result[ 'ERROR' ] = err
    io_mgr.end(connector_result)

# Defining a temp dict "temp_connector_result"- we want to appeand the current file's results only if file has scanned successfully
def readFromFile(dataFile, connector_params, connector_result,filename):
    temp_connector_result = {}
    Urls    = dataFile.readlines()
    api_key = 'd04b789a9806635aa811e685fdfcae5952d982da4cf6dd920bbc5eb4a8237b5f'
    headers = {'x-apikey': api_key, 'Accept': 'application/json'}
    api_url = 'https://www.virustotal.com/api/v3/urls'
    count   = 0 
    for curURL in Urls:
        if(int(connector_params.iteration_count)<= count):
            break
        url = Url(curURL)
        success,err  = url.scanURLwithVT(api_url,headers,filename)
        if(not success):
            return 0,err
        temp_connector_result[url.url] = url
        count +=1
    connector_result.update(temp_connector_result)
    return 1,err
    
if __name__ == "__main__":
    main()