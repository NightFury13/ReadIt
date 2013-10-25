# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
def postpage():
	x=request.args(0)
	usertype=db(db.auth_user.id==auth.user_id).select(db.auth_user.usertype)
	usertype=usertype[0]
	post=db(db.post.title.contains(x)).select()
	if post:
		post=post[0]
	else:
	 	post=None
	 	return locals()
	x=post['id']
	check=db(db.rate.userid==auth.user_id and db.rate.postid==x).select()
	comments=db(db.comm.postid==x).select(db.comm.id,db.comm.commby,db.comm.commt,db.comm.posttime)
	form=crud.create(db.comm)
	likeform=crud.create(db.rate)
	ctr=rate()
	catnames=db().select(db.categ.id,db.categ.catname)
	return locals()

def delpost():
	pid=request.args(0)
	db(db.post.id==pid).delete()
	response.flash=T('Post Removed')
	return (dict(message=T('Post Removed')))

def delcomm():
	commid=request.args(0)
	db(db.comm.id==commid).delete()
	response.flash=T('Comment Removed')
	return (dict(message=T('Comment Removed')))


@auth.requires_login()
def rate():
	rate=db(db.rate.postid==(request.args(1))).select(db.rate.userid,db.rate.postid,db.rate.stat)
	ctr=100
	users=[]
	for i in rate:
		if i['userid'] not in users:
			users.append(i['userid'])
			last=db(db.rate.userid==i['userid']).select(db.rate.stat)
			l=len(last)
			stat=last[l-1]['stat']
			if stat=='Like':
				ctr += 5
			else:
				ctr -= 3
		else:
			continue
	db(db.post.id==(request.args(1))).update(rating=ctr)
	return ctr

@auth.requires_login()
def search():
	x=request.vars['keyword']
	usertype=db(db.auth_user.id==auth.user_id).select(db.auth_user.usertype)
	usertype=usertype[0]
	categ=db(db.post.title.contains(x)).select(orderby=~(db.post.rating))
	names=db().select(db.categ.id,db.categ.catname)
	return (locals())

def catsearch():
	usertype=db(db.auth_user.id==auth.user_id).select(db.auth_user.usertype)
	usertype=usertype[0]
	x=request.args(0)
	catnames=db().select(db.categ.id,db.categ.catname)
	names=db(db.post.category==x).select(db.post.title,db.post.postby,db.post.id,db.post.rating,orderby=~(db.post.rating))
	return locals()

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to Read!t")
    return (dict(message=T('Hello World')))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
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


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
