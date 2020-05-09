# cisco-pnp-server
Cisco Network PnP server written in Flask to bootstrap Cisco enterprise network devices

## pnp server discovery
There are 3 main way for the device to discover the ztp server:

1. DHCP Option 43: Seems to be the easiest way
2. DNS: The device will look for **pnpserver**.*localdomain*
3. Cloud redirect: requires a cisco license

### How to Configure the DHCP pool (including DHCP Option 43)
```
Device> enable
Device# configure terminal
Device(config)# ip dhcp pool pnp_device_pool
Device(config-dhcp)# network 10.1.1.0 255.255.255.0
Device(config-dhcp)# default-router 10.1.1.1
Device(config-dhcp)# option 67 ascii http://**HOST**/http.py
Device(config-dhcp)# dns-server 10.1.1.254
Device(config-dhcp)# domain-name domain.local
Device(config-dhcp)# end
```

### DNS discovery configuration
This is the DHCP configuration needed, note the DNS server and the **local domain**.
```
ip dhcp pool Vlan1
 network 10.102.1.0 255.255.255.0
 default-router 10.102.1.1
 dns-server 10.102.2.20
 domain-name secmob.local
```
(and remember to create an entry on the DNS server!!)

## Gotchas
#### 1- The out of band management interface in cat3650 and cat3850 doensn't work properly:
  * Before everest - 16.5.1a - no discovery at all is done using that interface
  * in 16.5.1a the interface will be down after the pnp operation  
  
   ```
   interface GigabitEthernet0/0
    vrf forwarding Mgmt-vrf
    ip address 10.102.1.48 255.255.255.0
    negotiation auto
    shutdown
   ```
   I have tried to force the `no shutdown` on the configuration, but this in turn made the pnp process fail AND shutted down the port anyway - **_investigations in process_**
   
#### 2- In 16.5.1a weird behaviours are observed if the configuration for the port used for pnp is not in switchport
  In my case this is the intended configuration:
```
interface GigabitEthernet1/0/37
 no switchport
 ip address 10.102.1.11 255.255.255.0
```
  And this is the outcome:
```
interface GigabitEthernet1/0/37
 no switchport
 no ip address
```
Workaround: use switchport and move the ip to the vlan.
