@auth.requires_membership("admin")
def index():
	grid = SQLFORM.grid(
		db.entry,
		create=True,
		editable=True,
		user_signature=False
		)

	return locals()