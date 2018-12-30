import paramiko

class DHCP():
    
    def __init__(self, ip=None, port=22, username=None, password=None):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.client = None
    
    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(self.ip,
                            port=self.port,
                            username=self.username,
                            password=self.password)

    def disconnect(self):
        self.client.close()
        
    def exec_command(command):
        return self.client.exec_command(command)
