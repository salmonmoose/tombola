@auth.requires_membership("admin")
def index():
    grid = SQLFORM.grid(
        db.secret_key,
        create=True,
        editable=True,
        user_signature=False
        )

    return locals()
