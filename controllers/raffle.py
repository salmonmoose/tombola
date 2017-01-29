import random
import hashlib
import binascii
import struct

def index():
	grid = SQLFORM.grid(
		db.raffle,
		create=True,
		editable=True,
		user_signature=False
		)

	return locals()

def make_keys():
	form = SQLFORM.factory(
		Field('raffle', 'reference raffle',
			requires=IS_IN_DB(db, db.raffle.id, '%(name)s')
			),
		Field('tag', 'string'),
		Field('quantity', 'integer'),
		)

	if form.process().accepted:
		key_ids = []
		for i in range (0, int(request.vars.quantity)):
			key_ids.append(__generate_key(
				request.vars.raffle,
				request.vars.tag,
				))

		#show new keys, and force download of file

	return dict(grid=form)

def __generate_key(raffle, tag):
	valid_key = False

	while not valid_key:
		temp_key = hashlib.sha1(
			struct.pack(
				"f",
				random.random()
				)
			).hexdigest()[0:16]

		test_key = db(
			(db.secret_key.secret_key == temp_key)
			).select().first()

		if test_key is None:
			id = db.secret_key.insert(
				secret_key=temp_key,
				raffle=raffle,
				tag=tag,
				redeemed=False
				)

			valid_key = True

	return id
