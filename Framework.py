import json
import subprocess
import time
import threading
import DataModels
import datetime

class frameWorkSingelton():

    __instance = None
    def __init__(self):
        if frameWorkSingelton.__instance != None:
            print("Cannot define another instance of a singelton class.")
        else:
            frameWorkSingelton.__instance = self
    
    @staticmethod 
    def getInstance():
        if frameWorkSingelton.__instance == None:
            frameWorkSingelton()
        return frameWorkSingelton.__instance

    # Starting a thread for each instance of the VT connector, each thread runs the "runConnector" function using the instance's name.
    def runFrameWork(self):
        VTConnectorfirstInstance          = threading.Thread(target=self.runConnector, args=('VirusTotal1',))
        VTConnectorSecondInstance         = threading.Thread(target=self.runConnector, args=('VirusTotal2',))
        VTConnectorfirstInstance.start()
        VTConnectorSecondInstance.start()


    # This function calls the "defineConnectorsManually()" which reads the connector's instance settings from the "config.json" file.
    # Each thread that calls this function, is starting a new process depending on the script's file path.
    # The subproccess output is printed in the "out" var using PIPES.
    def runConnector(self,name):
        count = 0
        while(1):
            configSettings,params         = self.defineConnectorsManually(name)
            proc                          = subprocess.Popen(["python",configSettings.script_file_path],stdout = subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf8')
            JSONparams                    = json.dumps(params)
            out, err                      = proc.communicate(JSONparams)
            self.printResultToOutputFile(out,configSettings)
            time.sleep(int(configSettings.run_interval_seconds))
            count+=1

    # Printing the result to the connector's output file
    # If there is an error ( the output starts with zero ) - print the error to the console (not to the output file), 
    # and do not open a new file if there are no new results.
    def printResultToOutputFile(self,out, settings):
        if(out):
            if(str(out).startswith('0')):
                errorLine, *others = out.splitlines()
                print(settings.connector_name,' Connector has not finished successfuly - ',errorLine[1:])
            else: 
                print(settings.connector_name,' Connector has finished successfuly')
                others = out.splitlines()
            if(len(others)!=0):
                outputFolderPath = settings.output_folder_path+'\\'+ datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
                file = open(outputFolderPath, 'w')
                for line in others:
                    file.write(line+'\n')
                file.close()

    # name- the name of the VT connector instance in config file
    # Accessing the config JSON file to load the VirusTotal configuration settings
    def defineConnectorsManually(self,name):
        configFile                                     = open('config.json', )
        settings                                       = json.load(configFile)
        VTconnector_settings                           = DataModels.ConnectorSettings()
        VTconnector_settings.run_interval_seconds      = settings['VT'][name]['run_interval_seconds']
        VTconnector_settings.script_file_path          = settings['VT'][name]['script_file_path']
        VTconnector_settings.connector_name            = settings['VT'][name]['connector_name']
        VTconnector_settings.output_folder_path        = settings['VT'][name]['output_folder_path']
        VTconnector_settings.params                    = DataModels.ConnectorParams()
        VTconnector_settings.params.iteration_count    = settings['VT'][name]['iteration_entities_count']
        VTconnector_settings.params.source_folder_path = settings['VT'][name]['source_folder_path']
        JSONparams = {
            "source_folder_path"                       : settings['VT'][name]['source_folder_path'],
            "iteration_entities_count"                 : settings['VT'][name]['iteration_entities_count'],
        }
        return VTconnector_settings,JSONparams
def main():
    frameWork = frameWorkSingelton()
    frameWork.runFrameWork()

if __name__ == "__main__":
    main()


