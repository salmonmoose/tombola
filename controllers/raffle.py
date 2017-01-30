import random
import hashlib
import binascii
import struct
import os

@auth.requires_membership("admin")
def index():
	grid = SQLFORM.grid(
		db.raffle,
		create=True,
		editable=True,
		user_signature=False
		)

	return locals()

@auth.requires_membership("admin")
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

@auth.requires_membership("admin")
def make_flyers():
	flyer_keys = db(
		(db.secret_key.released == False)
		).select()

	tempfolder = os.path.join(request.folder, 'temp')

	if not os.path.exists(tempfolder):
		os.makedirs(tempfolder)

	for flyer_key in flyer_keys:
		filename = os.path.join(
			tempfolder,
			'%s.svg' % (flyer_key['secret_key'])
			)

		hashparts = [flyer_key['secret_key'][i:i+4] for i in range(0, len(flyer_key['secret_key']), 4)]

		open(filename, 'wb').write(
			response.render('raffle/flyer.svg',
				dict(
					hash1=hashparts[0],
					hash2=hashparts[1],
					hash3=hashparts[2],
					hash4=hashparts[3],
					)
				)
			)

		flyer_key.update_record(
			released=True
			)


	return response.render('raffle/flyer.svg', dict(
			hash1=hashparts[0],
			hash2=hashparts[1],
			hash3=hashparts[2],
			hash4=hashparts[3],
		))

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
				released=False,
				redeemed=False,
				)

			valid_key = True

	return id
