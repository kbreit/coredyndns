import paramiko

class Lease():

    def __init__(self, ip, mac, expiration, host, domain):
        self.ip = ip
        self.mac = mac
        self.expiration = expiration
        self.host = host
        self.domain = domain
        self.dns_record = None
        
    def get_dns_record(self):
        self.dns_record = {'ip': self.ip}
        return self.domain, self.dns_record

class DHCP():
    
    def __init__(self, host, port=22, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.leases = dict()
    
    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # self.client.load_system_host_keys()
        self.client.connect(self.host,
                            port=self.port,
                            username=self.username,
                            password=self.password)

    def disconnect(self):
        self.client.close()
        
    def exec_command(self, command):
        return self.client.exec_command(command)
        
    def add_lease(self, host, lease):
        self.leases[host] = lease
        
    def del_lease(self, name):
        del self.leases[host]
        
    def parse_leases(self, data, domain):
        lines = data.replace("  ", " ").split("\n")
        iterlines = iter(lines)
        next(iterlines)
        next(iterlines)
        for line in iterlines:
            row = line.split(" ")
            try:
                if row[5] != "":
                    lease = Lease(row[0],
                                  row[1],
                                  row[2].join(row[3]),
                                  row[5],
                                  domain)
                    self.add_lease(lease.host, lease)
            except IndexError:
                pass

