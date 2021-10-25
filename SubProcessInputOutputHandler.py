from DataModels import ConnectorParams
import json
import sys
class SubProcessInputOutputHandler(object):
    @property
    def connector_params(self):

        result = ConnectorParams()
        params                    = json.loads(input())
        result.source_folder_path = params["source_folder_path"]
        result.iteration_count    = params["iteration_entities_count"]
        return result

    # Printing the results to the STDOUT
    # If an 'Error' key appears in the dictionary, first print the error to the STDOUT and then the results (if any)
    def end(self, connector_result):
        if('ERROR' in connector_result):
            print(0,connector_result['ERROR'])
            del connector_result['ERROR']
        for key in connector_result:
            currentUrRL = connector_result[ key ]
            print(key)
            if(currentUrRL.isMalicious):
                print('MALICIOUS - '+ str(currentUrRL.RelevantData['Analysis'])+ str(currentUrRL.RelevantData['Reputation'])+'\n\n')
            else:
                print('NOT MALICIOUS'+'\n')
        sys.exit()