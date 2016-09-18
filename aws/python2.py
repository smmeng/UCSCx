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

VPC_GROUP_NAME = 'python2'
VPC_GROUP_DESCRIPTION = 'Security group for python homework2'

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
newKeyname = 'mynewkey1'
newKey = ec2.create_key_pair(newKeyname)
newKey.save("./")

#
# Create two new instances
#getAMI-ID from AWS Ec2 console in region, then we programmatically create the new EC2 instance with reservation# as a return
#
instance1 = ec2.run_instances('ami-31490d51', instance_type='t2.micro',security_group_ids=[group.id],subnet_id=sn1.id, key_name=newKeyname)
pprint(vars(instance1))
id1 = str(instance1.instances[0].id)
time.sleep(1)
print 'int1 [', id1 , '] created.'

# wait for initialization to complete
while True:
	status1 = ec2.get_all_instance_status(instance_ids=id1)
	print 'status1=', status1
	if len(status1)==0:
		print "Wait for another 6 sec until the EC2 instance up......"
		time.sleep(6)
		continue
	break

print 'Shutting down int1 [', id , '] in 30 sec.'
time.sleep(30)
term1= ec2.terminate_instances(instance_ids=[str(id1)])



#########