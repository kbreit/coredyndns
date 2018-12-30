import dhcp

config = {}

def get_config():
    with open('./config') as conf:
        lines = conf.readlines()
    for line in lines:
        conf_line = line.rstrip("\n").split("=")
        config[conf_line[0]] = conf_line[1]

def main():
    # Read configuration
    get_config()
    # Create connection via paramiko
    server = dhcp.DHCP()
    server.connect()
    # Query DHCP leases
    stdin, stdout, stderr = server.exec_command("show dhcp leases")
    print(stdin)
    print(stdout)
    print(stderr)
    # Set etcd entries
    

if __name__ == '__main__':
    main()
    print("Quitting...")
    quit()
