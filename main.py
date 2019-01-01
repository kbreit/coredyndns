#!/usr/bin/env python
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
                       password=config['dhcp_password'])
    server.connect()

    # Query DHCP leases
    stdin, stdout, stderr = server.exec_command("/config/scripts/getdhcpleases")
    server.parse_leases(stdout.read().decode('utf-8'), config['etcd_domain'])

    # Set etcd entries
    client = db.DB(config['etcd_hostname'], port=2379)
    client.connect()

    for hostname, lease in server.leases.items():
        path = client.format_dir(config['etcd_prefix'],
                                 config['etcd_domain'],
                                 hostname)
        entry = {'host': lease.ip,
                 'ttl': 900,
                 }
        if client.get_key(path) is -1:
	        client.set_key(path,
    	                   entry,
        	               ttl=60)
			print("DHCP entry added for {0} at {1}".format(hostname, lease.ip)

if __name__ == '__main__':
    main()
