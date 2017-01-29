import hashlib
import binascii

def index():
	form = SQLFORM.factory(
		Field('hash1', 'string'),
		Field('hash2', 'string'),
		Field('hash3', 'string'),
		Field('hash4', 'string'),
		Field('email', 'string'),
		Field('email_confirm', 'string'),
	)

	if form.process().accepted:
		request_key = '%s%s%s%s' % (
			request.vars.hash1,
			request.vars.hash2,
			request.vars.hash3,
			request.vars.hash4
			)

		secret_key = db(
			(db.secret_key.secret_key == request_key)
			).select().first()

		if secret_key is None:
			#this key doesn't exist
			pass

		#TODO: requests from a single IP should be rate limited.

		elif secret_key['redeemed']:
			#this key has already been validated.
			pass
		else:
			secret_key.update_record(
				redeemed=True
				)

			db.entry.insert(
				secret_key = secret_key.id,
				email = request.vars.email,
				ip_address = request.vars.client,
				browser_hash = hashlib.sha1(request.env.http_user_agent).hexdigest()
				)

			pass

	return locals()