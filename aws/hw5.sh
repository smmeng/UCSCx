echo $RANDOM

echo Setup the bucket 
bucketname="ucscawscli"
bucketname="s3://$bucketname"$RANDOM

echo Create the s3 bucket
aws s3 mb  $bucketname

echo copy all the files in the current directory to the new s3 bucket
aws s3 cp . s3://ucscawscli15021 --recursive

echo download all the files in  the new s3 bucket 
aws s3 cp  s3://ucscawscli15021 ~/download --recursive
  
echo finally remove the s3 bucket
aws s3 rb s3://ucscawscli15021 --force
