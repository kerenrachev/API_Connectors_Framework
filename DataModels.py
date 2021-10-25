class ConnectorSettings(object):
    run_interval_seconds = None  # int - iterations interval in seconds for current connector
    script_file_path = None # string - the file path to the connector script
    connector_name = None  # string - connector name
    params = None  # ConnectorParams object - see below
    output_folder_path = None # string - file path for connector output

class ConnectorParams(object):
    source_folder_path = None  # string - file path for entity list files
    iteration_count = None  # int - how many entities to process each interval (ignore the rest)

class ConnectorResult(object):
    alerts = None  # Dictionary {string, any} - connector output with data per entity. Key = Entity, value = entity data
