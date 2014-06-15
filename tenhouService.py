#!/usr/bin/env python
#coding=utf-8

import web
import hashlib
import tenhouDB
from tenhouDAO import *

DATABASE = tenhouDB.database

def selectByLinker(linkKey, linkValue, linkTarget, linkTable, targetDAO):
    #Warning: may not be compatible with other database formats
    #         compatible with: SQLite
    query = r"""
    select * from %s
    where %s in (
        select %s from %s
        where %s = $%s)
    """ % (targetDAO.TABLENAME, targetDAO.SEQCOLUMN, linkTarget, linkTable, linkKey, linkKey)
    sqliter = DATABASE.query(query, vars={linkKey: linkValue})
    return [targetDAO().set(**row) for row in sqliter]

def checkLogin(username, password):
    password = saltHash(password)
    user = DAOuser.selectFirst(
        where=web.db.sqlwhere({
            'username': username,
            'password': password
            }))
    return user

def register(username, password):
    password = saltHash(password)
    return DAOuser().set(
        username=username,
        password=password,
        id_role=3,
        des=u"新注册的会员"
    ).insert()

def saltHash(text, salt='rnd495'):
    return hashlib.sha256(text + salt).hexdigest()

if __name__ == '__main__':
    print saltHash('admin')