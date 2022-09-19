import os
from history import HistoryParser


def main():
    # Set up collection and analysis path
    system_info = os.path.join('./', 'os_artifact')
    web_framework = os.path.join('./', 'web_framework')

    os.makedirs(system_info, exist_ok = True)
    os.makedirs(web_framework, exist_ok = True)

    # History
    HistoryParser history_parser = HistoryParser()
    history_parser.history_analyze(system_info)




if __name__ == "__main__":
    main()