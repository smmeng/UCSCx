##############################################################################
# AWS homework3. Author: Siming Meng
##############################################################################

##############################################################################
# 01) Programmatically create a security group that allows ssh access
##############################################################################
aws ec2 create-security-group --group-name homework3 --description "Security group for homework3"
aws ec2 authorize-security-group-ingress --group-name homework3 --protocol tcp --port 22 --cidr 0.0.0.0/0

##############################################################################
# 02) Create a key-pair that is used for ssh access (we will not actually use this key pair in this assignment) – and download it to hw3.pem
##############################################################################
aws ec2 create-key-pair --key-name mynewkey3 > hw3.pem

##############################################################################
# 03) Create two Amazon Linux Micro instances in the us-west-1 region
##############################################################################
aws ec2 run-instances --image-id ami-31490d51 --count 2 --instance-type t2.micro  --security-groups homework3

###############################################################################
# 04) Programmatically after both instances are launched – print out information about these two running instances
###############################################################################
aws ec2 describe-instances --filter Name="instance.group-name",Values="homework3" --output json 

###############################################################################
# 05) Next, Programmatically terminate both instances
###############################################################################
#first parse and save the instance id to a text file
aws ec2 describe-instances --filter Name="instance.group-name",Values="homework3" --output text | awk -F"\t" '$1=="INSTANCES" {print $8}' > termination.sh

#then add the terminate command before each instance id
sed -i -- 's/i-/aws ec2 terminate-instances --instance-ids i-/g' termination.sh

#chmod 755 prior to executing
chmod 755 termination.sh
 
./termination.sh
#aws ec2 terminate-instances --instance-ids i-44a44ac3
#aws ec2 terminate-instances  --filter Name="instance.group-name",Values="homework3" 

sleep 3

rm -f ./termination.sh
### Search for InstanceId
#aws ec2 describe-instances --region us-west-1 --output json | grep InstanceId