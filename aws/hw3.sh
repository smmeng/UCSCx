
# create security group
aws ec2 create-security-group --group-name homework3 --description "Security group for homework3"

# Search for InstanceId
aws ec2 describe-instances --region us-west-1 --output json | grep InstanceId


sleep 3