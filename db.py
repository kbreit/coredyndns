import etcd

class DB():
    
    def __init__(self, hostname, username=None, password=None, port=2379):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.connection = None
        self.prefix = None
        
    def connect(self):
        self.connection = etcd.Client(host=self.hostname,
                                      port=self.port)
        #print(self.connection.machines)
        return self.connection

    def get_key(self, key, recursive=False):
        if recursive is True:
            return self.connection.read(key, recursive=True)
        else:
            return self.connection.read(key).value
       
    def set_key(self, key, value, ttl=None):
        self.connection.write(key, value, ttl=ttl)
        
    def delete_key(self, key):
        self.connection.delete(key)
    
    def delete_dir(self, dir):
        return self.connection.delete(dir, recursive=True)
    
    @staticmethod
    def format_dir(prefix, domain):
        path_prefix = prefix
        for i in reversed(domain.split('.')):
            path_prefix = "{0}/{1}".format(path_prefix, i)
        return path_prefix
