import hashlib
import binascii

def index():
	print hashlib.sha1(request.env.http_user_agent).hexdigest()

