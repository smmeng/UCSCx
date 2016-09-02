'''
	AWS Python Assignment 1
	Author: Siming Meng
'''

#boto2 version
import os
import boto

#add a function to generate a random string – this will be used below

import string
import random
def random_generator(size=4, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))
	

UPLOAD_PATH = '/home/siming.meng/uploads/'
DOWNLOAD_PATH = '/home/siming.meng/Downloads/'
BUCKET_PREFIX = 'smmeng'

s3 = boto.connect_s3()
rs = s3.get_all_buckets()

print 'Listing all buckets'
for b in rs:
	print b

#######################################
# 1. create at least 2 new buckets
#######################################
newBucketsToCreate = raw_input("How many new bucket to create (less than 3):")
newBucketList = []
for num in range(0, int(newBucketsToCreate)):
	newBucketName = BUCKET_PREFIX + random_generator().lower()
	print 'newBucketName=[', newBucketName
	nb=s3.create_bucket(newBucketName)
	newBucketList.append( newBucketName)

print 'relisting all buckets again'
rs = s3.get_all_buckets()
for b in rs:
	print b
	
#######################################
# Get local filenames and upload them 
# to these new buckets
#######################################
iFileName = ''
iFileList = []

while True:
	iFileName = raw_input("Enter local file name to upload (use 'EOF' to stop):")
	if  iFileName == 'EOF' or len(iFileName)==0:
		break;
	iFileList.append(iFileName)
	
print 'iFileList=', iFileList

#Upload them to the new buckets (one copy each bucket!)
for bucketname in newBucketList:
	for filename in iFileList:
		bucket=s3.get_bucket(bucketname)
		anothernewkey=bucket.new_key(filename)
		anothernewkey.set_contents_from_filename(UPLOAD_PATH+filename)
		anothernewkey.set_acl('public-read')

#######################################
# Get  all objects in the new buckets
#######################################		
for bucketname01 in newBucketList:
	bucketlist=s3.get_bucket(bucketname01)
	bucket=s3.get_bucket(bucketname01)
	for obj in bucketlist:
		print obj

#######################################
# Get all objects in the new buckets
# to our downloads folder
#######################################	
for bucketname01 in newBucketList:
	bucketlist=s3.get_bucket(bucketname01)
	if os.path.exists(bucketname01)== False :
			print "creating folder [", bucketname01
			os.mkdir(DOWNLOAD_PATH+bucketname01)
			
	for obj in bucketlist:
		fn = bucketname01 + "/" + str(obj.key)
		print obj, " filename=", fn, fn[len(fn)-1]
		if fn[len(fn)-1] is '/' and os.path.exists(fn)== False :
			print "creating folder [", fn
			os.mkdir(DOWNLOAD_PATH+ fn)
		elif fn[len(fn)-1] is '/':
			continue
		else:
			obj.get_contents_to_filename(DOWNLOAD_PATH+fn)
			
print "SUCCESS!"