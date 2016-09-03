'''
	AWS Python Assignment 2
	Author: Siming Meng
'''

#boto2 version
import os
import time
import boto
import boto.vpc
import boto.vpc.vpc
from pprint import pprint

#add a function to generate a random string – this will be used below

import string
import random
def random_generator(size=4, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))
	
REGION = 'us-west-1'
KEY_NAME = 'key-west1'
UPLOAD_PATH = '/home/siming.meng/uploads/'
DOWNLOAD_PATH = '/home/siming.meng/Downloads/'
BUCKET_PREFIX = 'smmeng'

VPC_GROUP_NAME = 'appserver'
ec2 = boto.connect_ec2()
ec2=boto.ec2.connect_to_region(REGION)
#create a new security group
app = ec2.create_security_group(VPC_GROUP_NAME, 'The application tier')
sg = ec2.get_all_security_groups(filters={'group-name': [VPC_GROUP_NAME]})


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
newKey = ec2.create_key_pair('mynewkey')
newKey.save("./")

#
# Create two new instances
#getAMI-ID from AWS Ec2 console in region, then we programmatically create the new EC2 instance with reservation# as a return
#
instance1 = ec2.run_instances('ami-31490d51', instance_type='t2.micro',security_group_ids=[group.id],subnet_id=sn1.id, key_name=KEY_NAME)
pprint(vars(instance1))
id1 = str(instance1.instances[0].id)

print 'int1 [', id , '] created.'

instances= ec2.get_only_instances()

for instance in instances:
	print instance.tags , " is ", instance.state, " id=", instance.id, ' id1=', id1
	if id1 == str(instance.id):
		print "Found id1", id1
		ec2Instance1 = instance
		break

print 'Found instance1 ', ec2Instance1, ' Waiting to run'
while ec2Instance1.state != "running":
	time.sleep(6)
	print "Wait for another 6 sec ......"
		

 
print 'Shutting down int1 [', id , '] in 30 sec.'
#time.sleep(30)
term1= ec2.terminate_instances(instance_ids=[str(id1)])

#########
instance2 = ec2.run_instances('ami-31490d51', instance_type='t2.micro',security_group_ids=[group.id],subnet_id=sn1.id, key_name=KEY_NAME)
