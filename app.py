#!/usr/bin/env python
#coding=utf-8

import web
import page_API
import tenhouService

from tenhouDAO import *

web.config.debug = False

def Authorization(rights=[], needLogin=False):
    def funcDec(pageFunc):
        def retFunc(*arg, **karg):
            if needLogin and not session.isLogin:
                raise web.Unauthorized()
            if any(not r in session.rights for r in rights):
                raise web.Unauthorized()
            return pageFunc(*arg, **karg)
        return retFunc
    return funcDec


class index:
    def GET(self):
        data = dict()
        data['subpage'] = render.gameList({'games': DAOgame.select()})
        navbars = [
            (u"比赛列表", "/", True),
        ]
        data['navbars'] = navbars
        return render.base(data)

class login:
    def GET(self):
        data = dict()
        data['subpage'] = render.login({'info': '', 'username': ''})
        data['navbars'] = []
        return render.base(data)

    def POST(self):
        username = web.input().username
        password = web.input().password
        user = tenhouService.checkLogin(username, password)
        if user:
            login.login(user)
            raise web.seeother('/')
        else:
            data = dict()
            data['subpage'] = render.login({'info': 'has-error', 
                                            'username': username})
            data['navbars'] = []
            return render.base(data)

    @staticmethod
    def login(user):
        session.name = user.username
        session.id_user = user.id
        session.id_role = user.id_role
        session.role_name = user.getRole().name
        session.isLogin = True
        session.rights = [ri.id for ri in user.getRights()]

class register:
    def GET(self):
        data = dict()
        data['subpage'] = render.register({'info': '', 'username': ''})
        data['navbars'] = []
        return render.base(data)

    def POST(self):
        username = web.input().username
        password = web.input().password
        passwordcfm = web.input().passwordcfm

        user = DAOuser.selectFirst(where=web.db.sqlwhere({'username': username}))
        if user:
            data = dict()
            data['subpage'] = render.register({'info': 'has-error', 
                                               'username': username,
                                               'error': u'用户名已经存在。如果是你的天凤ID被别人注册，可以与联系比赛管理员。'})
            data['navbars'] = []
            return render.base(data)

        if password != passwordcfm:
            data = dict()
            data['subpage'] = render.register({'info': 'has-error', 
                                               'username': username,
                                               'error': u'两次密码不一致'})
            data['navbars'] = []
            return render.base(data)

        user = tenhouService.register(username=username, password=password)
        login.login(user)
        raise web.seeother('/')

class logout:
    def GET(self):
        session.kill()
        raise web.seeother('/')

class user:
    def GET(self):
        id_user = web.input().get('id_user', None)
        if id_user is None:
            if session.isLogin:
                id_user = session.id_user
            else:
                raise web.notfound()
        user = DAOuser.selectFirst(where=web.db.sqlwhere({'id': id_user}))
        if not user:
            raise web.notfound()
        data = dict()
        data['subpage'] = render.userview({'user': user, 'okToUpdate': self.okToUpdate(user)})
        data['navbars'] = [
            (u"比赛列表", "/", False),
            (u"用户信息", "/user", True),
        ]
        if 1 in session.rights:
            data['navbars'].append((u"管理用户", "/manageuser", False))
            data['navbars'].append((u"管理比赛", "/managegame", False))

        return render.base(data)

    @Authorization(needLogin=True)
    def POST(self):
        id_user = web.input().get('id_user', session.id_user)
        des = web.input().des
        password = web.input().password
        passwordcfm = web.input().passwordcfm
        if password:
            if password != passwordcfm:
                return u"两次密码不一致"
        if not des is None:
            user = DAOuser.selectFirst(where=web.db.sqlwhere({'id': id_user}))
            if self.okToUpdate(user):
                user.des = des
                if password:
                    user.password = tenhouService.saltHash(password)
                user.update()
            else:
                raise Unauthorized()
        return self.GET()

    def okToUpdate(self, user):
        okToUpdate = False
        if session.id_user == user.id:   #可以管理自己的信息
            okToUpdate = True
        elif user.id_role == 2 and 0 in session.rights:  #0号权利可以管理管理员
            okToUpdate = True
        elif user.id_role == 3 and 1 in session.rights:  #1号权利可以管理会员
            okToUpdate = True
        return okToUpdate

class manageuser:
    @Authorization(rights=[1], needLogin=True)
    def GET(self):
        self.work()
        data = dict()
        data['subpage'] = render.manageuser({'users': DAOuser.select()})
        data['navbars'] = [
            (u"比赛列表", "/", False),
            (u"用户信息", "/user", False),
            (u"管理用户", "/manageuser", True),
            (u"管理比赛", "/managegame", False)
        ]
        return render.base(data) 

    def work(self):
        action = web.input().get("action", None)
        if action is None:
            return
        id_user = web.input().get("id_user", None)
        value = int(web.input().get("value", None))
        user = DAOuser.selectFirst(where=web.db.sqlwhere({"id": id_user}))
        if not user:
            raise web.notfound()
        if self.okToOperat(user):
            if action == "delete":
                user.delete()
            elif action == "setrole":
                if value == 2 or value == 3:
                    user.id_role = value
                    user.update()
                else:
                    print value
                    raise web.Unauthorized()
        else:
            raise web.Unauthorized()

    def okToOperat(self, user):
        okToUpdate = False
        if user.id_role == 2 and 0 in session.rights:  #0号权利可以管理管理员
            okToUpdate = True
        elif user.id_role == 3 and 1 in session.rights:  #1号权利可以管理会员
            okToUpdate = True
        return okToUpdate



initializer = {
    'name': u'游客',
    'id_user': 0,
    'id_role': 0,
    'role_name': u'游客',
    'isLogin': False,
    'hasUnread': 0,
    'rights': []
}
urls  = ['/', 'index',
         '/login', 'login',
         '/logout', 'logout',
         '/register', 'register',
         '/user', 'user',
         '/manageuser', 'manageuser']
pages = {'index': index,
         'login': login,
         'logout': logout,
         'register': register,
         'user': user,
         'manageuser': manageuser}

app = web.application(urls, pages)
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer=initializer)
render = web.template.render('templates', globals={'session': session})

if __name__ == '__main__':
    app.run()