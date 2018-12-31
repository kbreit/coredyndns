import dhcp
import db

config = {}

def get_config():
    with open('./config') as conf:
        lines = conf.readlines()
    for line in lines:
        conf_line = line.rstrip("\n").split("=")
        try:
            if conf_line[0][0] != "#":
                config[conf_line[0]] = conf_line[1]
        except IndexError:
            pass

def main():
    # Read configuration
    get_config()

    # Create connection via paramiko
    server = dhcp.DHCP(config['dhcp_hostname'],
                       port=config['dhcp_port'],
                       username=config['dhcp_username'],
                       password=['dhcp_password'])
    # server.connect()

    # Query DHCP leases
    # stdin, stdout, stderr = server.exec_command("show dhcp leases")
    #print(stdin)
    #print(stdout)
    #print(stderr)
    # server.parse_leases(stdout)

    # Set etcd entries
    client = db.DB('192.168.15.200', port=2379)

    client.connect()
    path = client.format_dir(config['etcd_prefix'],
                             'testdns.home.kevinbreit.net')
    entry = {'host': '192.168.15.201',
             'ttl': 900,
             }
    client.set_key(path,
                   entry,
                   ttl=60)
    print(client.get_key(path, recursive=True))


if __name__ == '__main__':
    main()
