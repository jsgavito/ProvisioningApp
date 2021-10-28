import re
from ncclient import manager
#pretty xml
import xmltodict
import xml.dom.minidom


# Create config template for a new classifier
createClassifier= """<config><classifiers>
 <classifier>
	<name>VLAN{vid}</name>
	<filter-entry>
    <filter-parameter xmlns:classifier="urn:ciena:params:xml:ns:yang:ciena-pn::ciena-mef-classifier">classifier:vtag-stack</filter-parameter>
		<vtags><tag>1</tag>
		<vlan-id>{vid}</vlan-id>
		</vtags>
	</filter-entry></classifier></classifiers>
 </config>"""

#Classifier Details
classifier ={ "vid": "91" }

# Create config template for a new forwarding domain
createFD= """<config><fds xmlns="urn:ciena:params:xml:ns:yang:ciena-pn:ciena-mef-fd">
<fd><name>{FDname}</name>
    <mode>vpls</mode>
	<vlan-id>{vid}</vlan-id>
	</fd></fds>
</config>"""

#FD Details
FD ={ "FDname": "FDVLAN91", "vid": "91" }

# Create config template for a new flow-point
createFP= """<config><fps xmlns="urn:ciena:params:xml:ns:yang:ciena-pn:ciena-mef-fp">
	<fp><name>{FPname}</name>
	<fd-name>{FDname}</fd-name>
	<logical-port>{PortNumber}</logical-port>
	<classifier-list>{classifier}</classifier-list>
	</fp></fps>
</config>"""

#FP Details
FP ={ "FPname": "FP_VLAN91", "classifier": "VLAN91", "FDname": "FDVLAN91", "PortNumber": "7" }


# Create config template for a key-chain
createKC= """<config>
  <macsec xmlns="http://www.ciena.com/ns/yang/ciena-macsec">
    <key-chains>
      <key-chain>
        <name>{KC}</name>
        <mka-keys><mka-key>
           <name>01</name><key>{newkey}</key>
           <cryptographic-algorithm>AES_256_CMAC</cryptographic-algorithm>
        </mka-key></mka-keys>
      </key-chain>
    </key-chains>
   </macsec>
</config>"""

# KC Details
keychain = { "KC": "K91", "newkey": "012345678901234567890123456789ab" }

# Create config template for a macsec-profile

createMSprofile= """<config>
  <macsec xmlns="http://www.ciena.com/ns/yang/ciena-macsec">
      <macsec-profiles>
         <profile><name>{pfname}</name>
         <replay-window-size>2</replay-window-size>
         <macsec-cipher-suite>GCM_AES_256</macsec-cipher-suite>
         <encryption-on>true</encryption-on>
         <sak-rekey-interval>{key-interval}</sak-rekey-interval>
         </profile>
      </macsec-profiles>
   </macsec>
</config>"""

# MACSec profile Details
profile = { "pfname": "pf33", "key-interval": "30" }

#Enable MACSec config on interface 7 (only for first service)

configIntMACSec= """<config>
    <macsec xmlns="http://www.ciena.com/ns/yang/ciena-macsec"><config>
        <interfaces><interface>
            <name>{PortNumber}</name>
            <strict-mode-on>false</strict-mode-on>
            <exclude-protocols>lldp</exclude-protocols>
    </interface></interfaces>
    </config>
   </macsec>
</config>"""
#Only port 7 & 8 are valid
pnumber = {"PortNumber": "7"}




# Create config template for a CA deletion
createCA= """<config>
<macsec xmlns="http://www.ciena.com/ns/yang/ciena-macsec">
   <config>
     <connection-association><name>{CA}</name>
       <macsec-profile>{pfname}</macsec-profile>
          <key-chain>{KC}</key-chain>
          <flow-point>{FPname}</flow-point>
          <destination-address>{DMAC}</destination-address>
          <mka-ethertype>36865</mka-ethertype> 
     </connection-association>
   </config>
</macsec>
</config>"""

# CA Details
conn_assoc = { "CA": "CA91", "KC": "K91", "pfname": "pf33", "DMAC": "91:91:4d:c6:81:80", "FPname": "FP_VLAN91"}



# Open NETCONF connection to device
with manager.connect(
    host='10.181.37.180',     # IP address of the SAOS device in your pod
    port=830,              # Port to connect to
    username='user',      # SSH Username
    password='ciena123',  # SSH Password
    hostkey_verify=False   # Allow unknown hostkeys not in local store
    )as m:

    config = createClassifier.format (**classifier)
    print(config)
    r= m.edit_config (target = "running", config=config)
    
    print('\n')

    config = createFD.format (**FD)
    print(config)
    r= m.edit_config (target = "running", config=config)
    
    print('\n')

    config = createFP.format (**FP)
    print(config)
    r= m.edit_config (target = "running", config=config)
    
    print('\n')


    config = createKC.format (**keychain)
    print(config)
    r= m.edit_config (target = "running", config=config)
    
    print('\n')
    


    print('\n')
    config = createMSprofile.format (**profile)
    print(config)
    r= m.edit_config (target = "running", config=config)
    print('\n')
    
    print('\n')
    config = configIntMACSec.format (**pnumber)
    print(config)
    r= m.edit_config (target = "running", config=config)
    print('\n')
    
    #netconf_get_reply = m.get_config('running', filter=('subtree', xml_filter))
    print('\n')
    config = createCA.format (**conn_assoc)
    print(config)
    r= m.edit_config (target = "running", config=config)
    #print(netconf_get_reply)
    print('\n')
    print('try')
    print('\n')
# Print OK status

#print(("NETCONF RPC OK: {}". r.ok))


