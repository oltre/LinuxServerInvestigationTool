
class SetupPath(object):
    def __init__(self):
        self.system_info = os.path.join('./', 'os_artifact')
        self.web_framework = os.path.join('./', 'web_framework')

        os.makedirs(self.system_info, exist_ok = True)
        os.makedirs(self.web_framework, exist_ok = True)

    def get_system_info():
        return self.system_info

    def get_web_framework():
        return self.web_framework








