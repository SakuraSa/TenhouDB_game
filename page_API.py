#!/usr/bin/env python
#coding=utf-8


import web
import json

class page_API(object):
    APIs = set()
    def __init__(self):
        object.__init__(self)
        self.APIs = [api() for api in page_API.APIs]

    @classmethod
    def register(cls, api):
        if issubclass(api, APIbase):
            cls.APIs.add(api)
        else:
            raise Exception('NonAPI class register to apge_API')
        return api

    def select(self):
        method = web.input().get('method', None)
        if method is None:
            raise web.notfound()
        for api in self.APIs:
            if api.NAME == method:
                return api
        raise web.notfound()

    def checkInput(self, api):
        inputs = web.input()
        for key in api.PARAM:
            if not key in inputs:
                return False
        return True

    def GET(self):
        api = self.select()
        ok  = self.checkInput(api)
        if ok:
            return api.GET(**web.input())
        else:
            return errorJS(u"非法的参数输入")

    def POST(self):
        api = self.select()
        ok  = self.checkInput(api)
        if ok:
            return api.POST(**web.input())
        else:
            return errorJS(u"非法的参数输入")

def errorJS(msg, e=None):
    return json.dumps({
        'ok': False,
        'error': str(type(e)) + str(e),
        'message': msg
        })


class APIbase(object):
    NAME   = 'base'
    PARAM  = list()
    OPTION = dict()
    def __init__(self):
        object.__init__(self)

    def GET(self, **karg):
        raise web.notfound()

    def POST(self, **karg):
        raise web.notfound()