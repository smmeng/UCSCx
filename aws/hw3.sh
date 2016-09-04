
# 01) Programmatically create a security group that allows ssh access
aws ec2 create-security-group --group-name homework3 --description "Security group for homework3"

aws ec2 authorize-security-group-ingress --group-name homework3 --protocol tcp --port 22 --cidr 0.0.0.0/0

### Search for InstanceId
aws ec2 describe-instances --region us-west-1 --output json | grep InstanceId

# 02) Create a key-pair that is used for ssh access (we will not actually use this key pair in this assignment) – and download it

# 03) Create two Amazon Linux Micro instances in the us-west-1 region
aws ec2 run-instances --image-id ami-31490d51 --count 1 --instance-type t1.micro --key-name stage-key --security-groups homework3

# 04) Programmatically after both instances are launched – print out information about these two running instances

# 05) Next, Programmatically terminate both instances



sleep 3