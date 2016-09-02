#boto2 version
import osimport boto

UPLOAD_PATH = '/home/siming.meng/uploads/'
DOWNLOAD_PATH = '/home/siming.meng/Downloads/'
s3 = boto.connect_s3()
rs = s3.get_all_buckets()
print 'Listing all buckets'
for b in rs:
	print b

#get all objects in a bucket
#change this bucketname to the name of one of your buckets
bucketname01='sampdfs'
bucketlist=s3.get_bucket(bucketname01)
bucket=s3.get_bucket(bucketname01)
for o in bucketlist:
	print o

#get the contents of an object:
'''
bucketname01='samtemp'
bucket=s3.get_bucket(bucketname01)
key=bucket.get_key('calculation.txt')
obj=key.get_contents_as_string()
print obj
'''

#add a function to generate a random string – this will be used below
import string
import random
def random_generator(size=4, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

	
#upload a file - for this example the terminal
#used to run Python was opened in the same directory
#the install-boto2.txt file is locate in –
filename = "Class1.pdf"
anothernewkey=bucket.new_key(filename)
anothernewkey.set_contents_from_filename(UPLOAD_PATH+filename)
anothernewkey.set_acl('public-read')

#Download S3 object contents and save to a file
for o in bucketlist:
	fn = str(o.key)
	print o, " filename=", fn, fn[len(fn)-1]
	if fn[len(fn)-1] is '/' and os.path.exists(fn)== False :
		print "creating folder [", fn
		os.mkdir(DOWNLOAD_PATH+fn)
	elif fn[len(fn)-1] is '/':
		continue
	else:
		o.get_contents_to_filename(DOWNLOAD_PATH+fn)
		
