import boto.ses

AWS_ACCESS_KEY = 'AKIAIZJTUTIHG2VJXLRQ'
AWS_SECRET_KEY = 'AtVrjwqN7+ore898eWWzFsMaT1L2LN+KqHTjVsdO7qf9'
SES_REGION='us-west-2'

class Email(object):
	def __init__(self, to, subject):
		self.to = to
		self.subject = subject
		self._html = None
		self._text = None
		self._format = 'html'
		
	def html(self, html):
		self._html = html
		
	def text(self, text):
		self._text = text
		
	def send(self, from_addr=None):
		body = self._html
		
		if isinstance(self.to, basestring):
			self.to = [self.to]
		if not from_addr:
			from_addr = 'siming.meng@gmail.com'
		if not self._html and not self._text:
			raise Exception('You must provide a text or html body.')
		if not self._html:
			self._format = 'text'
			body = self._text
			
		connection = boto.ses.connect_to_region(
			'us-west-2',
			aws_access_key_id=AWS_ACCESS_KEY, 
			aws_secret_access_key=AWS_SECRET_KEY
		)
		return connection.send_email(
			from_addr,
			self.subject,
			None,
			self.to,
			format=self._format,
			text_body=self._text,
			html_body=self._html
		)


		
from boto.regioninfo import RegionInfo
from boto.ses.connection import SESConnection

oregon_region = RegionInfo(name='us-west-2',
                       endpoint='email-smtp.us-west-2.amazonaws.com',
                       connection_cls=SESConnection)
ses_conn = oregon_region.connect()


conn=boto.ses.connection.SESConnection(
	aws_access_key_id=AWS_ACCESS_KEY, 
	aws_secret_access_key=AWS_SECRET_KEY,
	region=oregon_region,
	debug=2)

conn.send_email(source='siming.meng@gmail.com', subject='test email', body='test body', to_addresses='smmeng@gmail.com', format='text')