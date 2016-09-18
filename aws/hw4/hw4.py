'''
	AWS Python Assignment 4
	Author: Siming Meng
'''
#boto2 version
import os
import time
#import Xme
import boto
import boto.vpc
import boto.vpc.vpc
#import boto.manage.cmdshell
from pprint import pprint


#add a function to generate a random string – this will be used below

import string
import random
def random_generator(size=4, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))
	
REGION = 'us-west-1'
KEY_NAME = 'key-west1'

VPC_GROUP_NAME = 'python2'
VPC_GROUP_DESCRIPTION = 'Security group for python homework2'

'''
ec2 = boto.connect_ec2()
ec2=boto.ec2.connect_to_region(REGION)
#create a new security group
app = ec2.create_security_group(VPC_GROUP_NAME, VPC_GROUP_DESCRIPTION )
sg = ec2.get_all_security_groups(filters={'group-name': [VPC_GROUP_NAME]})
app.authorize('tcp','22', '22', "0.0.0.0/0")

pprint (vars(sg[0]))
sgGroupId =  str(sg[0].id)
sgVPCId = str(sg[0].vpc_id)

vpccon = boto.vpc.connect_to_region(REGION)

#get vpc-id from VPC Dashboard
vpc = vpccon.get_all_vpcs(vpc_ids=[sgVPCId])[0];

#get security group id, from "Security Groups" section of EC2 management console, create a key pair
group = ec2.get_all_security_groups(group_ids=[sgGroupId])[0]
sn=vpccon.get_all_subnets(filters={'vpcId':[sgVPCId]})
sn1=sn[0]
key = ec2.get_all_key_pairs(keynames=[KEY_NAME])[0]
newKey = ec2.create_key_pair('mynewkey1')
newKey.save("./")
'''
#
######## Step1

def launch_instance(ami="ami-31490d51",
					region = 'us-west-1',
                    instance_type="t2.micro",
                    key_name="key-west1",
                    key_extension=".pem",
                    key_dir="~/.ssh",
					group_name="python2",
                    ssh_port="22",
                    cidr="0.0.0.0/0",
                    tag="homework4",
                    user_data=None,
                    login_user="ec2-user",
                    ssh_passwd=None):
	ec2 = boto.connect_ec2() # Crededentials are stored in /etc/boto.cfg
	ec2 = boto.connect_ec2(debug=2)
	ec2 =boto.ec2.connect_to_region(region)
	try:
		key = ec2.get_all_key_pairs(keynames=[key_name])[0]
		print "Key name=", key
	except ec2.ResponseError, e:
		print "ERROR!\n"
		if e.code == 'InvalidKeyPair.NotFound':
			print 'Creating keypair %s' % key_name
			key = ec2.create_key_pair(key_name)
			key.save(key_dir)
		else:
			raise
	try:
		group = ec2.get_all_security_groups(groupnames=[group_name])[0]
		print "Group name=", group
	except ec2.ResponseError, e:
		if e.code == 'InvalidGroup.NotFound':
			print'Creating security group %s' % group_name
			group = ec2.create_security_group(group_name, 'A group that allows SSH access')
		else:
			raise
	try:
		group.authorize('tcp',ssh_port,ssh_port,cidr)
	except ec2.ResponseError, e:
		if e.code == 'InvalidPermission.Duplicate':
			print ('Security group %s already authorized') % group_name
		else:
			raise
	reservation = ec2.run_instances(ami,
								key_name=key_name,
								security_groups=[group_name],
								instance_type=instance_type,
								user_data=user_data)
	instance = reservation.instances[0]
	print 'waiting for instance...'
	while instance.state != 'running':
		print '.'
		time.sleep(6)
		instance.update()
		
	print 'Instance is now running'
	print 'Instance IP is %s' % instance.ip_address
	
	instance.add_tag(tag)
	return (instance, reservation)

#Create & laucnh ec2 instance
l=launch_instance()
inst=l[0]
res=l[1]

#
ec2=inst.connection
azone=inst.placement
azone

#Create EBS volume
vol=ec2.create_volume(2,azone)
vol
vol.attach(inst.id,'/dev/sdf')

######################### Step 2
#ssh -i ~/.ssh/"keyPair0.pem" ec2-user@ec2-54-67-106-44.us-west-1.compute.amazonaws.com
#cat /proc/partitions
#sudo mke2fs -F -j /dev/sdf
#sudo mkdir /mnt/data-store
#sudo mount /dev/sdf /mnt/data-store
#df -T

######################### Step 3
snapshotName = 'ucsc-aws-class'
vol.create_snapshot(snapshotName)

ec2=boto.connect_ec2()
ec2=boto.ec2.connect_to_region('us-west-1')

instlist=ec2.get_all_instances()
instlist

#res=instlist[0] #Should we use res value from the previous launch_instance() instead??
inst=res.instances[0]
inst.id

inst.stop()
inst.terminate()

######################### Step 4
l=launch_instance(key_name="keyPair0")

inst=l[0]
res=l[1]

######################### Step 5
ec2=inst.connection
azone=inst.placement
azone

#Create EBS volume
ec2=boto.connect_ec2()
ec2=boto.ec2.connect_to_region('us-west-1')

insts=ec2.get_all_instances()
insts[0].connection

filters = {
	'description': snapshotName
}
snapshots = ec2.get_all_snapshots(filters=filters)
snapShotId =  snapshots[0].id
snapShotId

vol=ec2.create_volume(2,inst.placement, snapShotId)
#vol=ec2.create_volume(2,inst.placement,'snap-0084de3c5a56e404f')
vol
vol.attach(inst.id,'/dev/sdf')

######################### Verify step 5 
#ssh -i "keyPair0.pem" ec2-user@ec2-52-53-165-252.us-west-1.compute.amazonaws.com
#cat /proc/partitions
#sudo mkdir /mnt/dz
#sudo mount -t ext3 /dev/sdf /mnt/dz
#df -T