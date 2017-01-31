# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import hashlib
import binascii

def index():
    request.empty_page = True

    form = SQLFORM.factory(
        Field('hash1', 'string',
            length=4,
            requires=IS_LENGTH(minsize=4, maxsize=4),
            ),
        Field('hash2', 'string',
            length=4,
            requires=IS_LENGTH(minsize=4, maxsize=4),
            ),
        Field('hash3', 'string',
            length=4,
            requires=IS_LENGTH(minsize=4, maxsize=4),
            ),
        Field('hash4', 'string',
            length=4,
            requires=IS_LENGTH(minsize=4, maxsize=4),
            ),
        Field('email', 'string',
            requires=IS_EMAIL()
            ),
        Field('confirm', 'string',
            rname='confirm_email',
            requires=IS_EXPR(
                'value==%s' % repr(request.vars.get('email', None)),
                error_message="Emails do not match",
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

            response.flash = T("good luck")
    else:
        pass

    return dict(form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


