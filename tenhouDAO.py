#!/usr/bin/env python
#coding=utf-8

import web
import tenhouDB
import tenhouService

class DAO(object):
    """docstring for DAO"""
    PROPERTYNAMES = list()
    PROPERTYS     = dict()
    TABLENAME     = ""
    DATABASE      = tenhouDB.database
    SEQCOLUMN     = 'id'
    def __init__(self):
        object.__init__(self)
        object.__setattr__(self, 'PROPERTYS', dict(type(self).PROPERTYS))

    def __str__(self):
        return "<%s %s>" % (type(self), self.PROPERTYS)

    def __getattr__(self, name):
        if name in self.PROPERTYNAMES:
            return self.PROPERTYS.get(name, None)
        else:
            raise AttributeError("'DAO' object has no attribute '%s'" % name)
    
    def __setattr__(self, name, value):
        if name in self.PROPERTYNAMES:
            self.PROPERTYS[name] = value
        else:
            raise AttributeError("'DAO' object has no attribute '%s'" % name)

    def __sqlDict__(self):
        sqlDict = dict(self.PROPERTYS)
        if self.SEQCOLUMN in sqlDict:
            del sqlDict[self.SEQCOLUMN]
        return sqlDict

    def __sqlWhere__(self):
        return web.db.sqlwhere(
            {self.SEQCOLUMN: self.PROPERTYS[self.SEQCOLUMN]}
        )

    def set(self, **karg):
        for key in karg:
            self.PROPERTYS[key] = karg[key]
        return self

    def insert(self):
        self.DATABASE.insert(self.TABLENAME, **self.__sqlDict__())
        return self

    def update(self):
        self.DATABASE.update(self.TABLENAME, 
            where = self.__sqlWhere__(),
            **self.__sqlDict__())
        return self

    def delete(self):
        self.DATABASE.delete(self.TABLENAME,
            where = self.__sqlWhere__())
        return self

    @classmethod
    def select(cls, **karg):
        sqliter = cls.DATABASE.select(cls.TABLENAME, **karg)
        return [cls().set(**row) for row in sqliter]

    @classmethod
    def selectFirst(cls, **karg):
        DAOs = cls.select(**karg)
        if DAOs:
            return DAOs[0]
        else:
            return None

class DAOuser(DAO):
    """docstring for DAOuser"""
    PROPERTYNAMES = ['id', 
                     'username', 
                     'password', 
                     'id_role', 
                     'des']
    TABLENAME     = 'user'
    def __init__(self):
        DAO.__init__(self)

    def getRole(self):
        return DAOrole.selectFirst(
            where=web.db.sqlwhere({'id': self.id_role}))

    def getRights(self):
        return tenhouService.selectByLinker(
            linkKey = 'id_role',
            linkValue = self.id_role,
            linkTarget = 'id_right',
            linkTable = DAOroleRight.TABLENAME,
            targetDAO = DAOright
        )

    def getGames(self):
        return tenhouService.selectByLinker(
            linkKey = 'id_user',
            linkValue = self.id,
            linkTarget = 'id_user',
            linkTable = DAOgameUser.TABLENAME,
            targetDAO = DAOuser
        )

    def isInGame(self, id_game):
        links = DAOgameUser.selct(where = web.db.sqlwhere({'id_game': id_game, 'id_user': self.id}))
        return len(links) > 0

    def joinGame(self, id_game):
        if not self.isInGame(id_game):
            gameUser = DAOgameUser().set(id_user=this.id, id_game=id_game).insert()



class DAOrole(DAO):
    """docstring for DAOrole"""
    PROPERTYNAMES = ['id', 
                     'name']
    TABLENAME     = 'role'
    def __init__(self):
        DAO.__init__(self)


class DAOright(DAO):
    """docstring for DAOright"""
    PROPERTYNAMES = ['id', 
                     'name']
    TABLENAME     = 'right'
    def __init__(self):
        DAO.__init__(self)

class DAOroleRight(DAO):
    """docstring for DAOroleRight"""
    PROPERTYNAMES = ['id', 
                     'id_role',
                     'id_right']
    TABLENAME     = 'roleright'
    def __init__(self):
        DAO.__init__(self)

class DAOgame(DAO):
    """docstring for DAOgame"""
    PROPERTYNAMES = ['id', 
                     'name',
                     'url',
                     'id_statue',
                     'id_user_creator',
                     'des']
    TABLENAME     = 'game'
    def __init__(self):
        DAO.__init__(self)

    def getUser(self):
        return tenhouService.selectByLinker(
            linkKey = 'id_game',
            linkValue = self.id,
            linkTable = DAOgameUser.TABLENAME,
            targetDAO = DAOuser
        )

    def getStatue(self):
        return DAOgameStatue.select(where=web.db.sqlwhere({'id': self.id_statue}))

class DAOgameStatue(DAO):
    """docstring for DAOgameStatue"""
    PROPERTYNAMES = ['id',
                     'name']
    TABLENAME     = 'gameStatue'
    def __init__(self):
        DAO.__init__(self)

class DAOgameUser(DAO):
    """docstring for DAOgameUser"""
    PROPERTYNAMES = ['id',
                     'id_game',
                     'id_user']
    TABLENAME     = 'gameUser'
    def __init__(self):
        DAO.__init__(self)

class DAOround(DAO):
    """docstring for DAOround"""
    PROPERTYNAMES = ['id',
                     'id_game']
    TABLENAME     = 'round'
    def __init__(self):
        DAO.__init__(self)

class DAOroundRef(DAO):
    """docstring for DAOroundRef"""
    PROPERTYNAMES = ['id',
                     'id_round',
                     'ref']
    TABLENAME     = 'roundRef'
    def __init__(self):
        DAO.__init__(self)

class DAOteam(DAO):
    """docstring for DAOteam"""
    PROPERTYNAMES = ['id',
                     'name',
                     'id_user_leader',
                     'id_game',
                     'des']
    TABLENAME     = 'team'
    def __init__(self):
        DAO.__init__(self)

class DAOteamUser(DAO):
    """docstring for DAOteamUser"""
    PROPERTYNAMES = ['id',
                     'id_team',
                     'id_user',
                     'id_teamrole']
    TABLENAME     = 'teamUser'
    def __init__(self):
        DAO.__init__(self)

class DAOteamRole(DAO):
    """docstring for DAOteamRole"""
    PROPERTYNAMES = ['id',
                     'name']
    TABLENAME     = 'teamRole'
    def __init__(self):
        DAO.__init__(self)

if __name__ == '__main__':
    for u in DAOuser.select():
        print u.username
        print [r.name for r in u.getRights()]