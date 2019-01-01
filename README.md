# coredyndns

CoreDynDNS will likely be renamed, but is a Python script to coordinate dynamic DNS information between Ubiuiti EdgeMax routers and `etcd` based backends for a CoreDNS based DNS environment.

## Router Support

coredyndns currently only supports EdgeOS based routers. I'm happy to add additional routers but would need assistance with the DHCP lease output and testing. Pull requests are welcome.

## Configuration

Instructions assume DHCP server, etcd configuration, and CoreDNS are configured properly.

1. Rename the `config.template` file to `config`.
2. Install dependencies using `pip install -r requirements.txt`. venv is supported.
3. Fill out the variables in the `config` file.
4. Login to your EdgeOS router via SSH and execute `sudo su`.
5. Write the following script to `/config/scripts/getdhcpleases`

```
#!/bin/vbash
/opt/vyatta/bin/vyatta-op-cmd-wrapper show dhcp leases
exit 0
```

6. Execute `main.py`