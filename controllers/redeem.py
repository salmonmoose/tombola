import hashlib
import binascii

def index():
	form = SQLFORM.factory(
		Field('hash1', 'string',
			length=4,
			),
		Field('hash2', 'string',
			length=4
			),
		Field('hash3', 'string',
			length=4
			),
		Field('hash4', 'string',
			length=4
			),
		Field('email', 'string',
			requires=IS_EMAIL()
			),
		Field('email_confirm', 'string',
			requires=IS_EXPR(
				'value==%s' % repr(request.vars.get('email', None)),
				error_message="emails do not match",
				)
			),
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
			response.flash = T("unknown key")

		#TODO: requests from a single IP should be rate limited.

		elif secret_key['redeemed']:
			response.flash =T("key has already been redeemed")
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

	return locals()
