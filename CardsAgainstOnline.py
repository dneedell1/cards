import pymongo
from tornado import options
from CardsAgainstHumanity import GameHandler
from Server import Room
import json
import uuid
import os
import bcrypt
import hashlib
import urllib
import base64
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import tornado.httpserver
from tornado.web import url
import tornado.websocket
import tornado.util
import tornado.template

from handlers.handlers import *

define("port", default=8888, type=int)
# define("config_file", default="app_config.yml", help="app_config file")

MONGO_SERVER = 'localhost'

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
        url(r'/', HelloHandler, name='index'),
        url(r'/hello', HelloHandler, name='hello'),
        url(r'/email', EmailMeHandler, name='email'),
        url(r'/message', MessageHandler, name='message'),
        url(r'/thread', ThreadHandler, name='thread_handler'),
        url(r'/login_no_block', NoneBlockingLogin, name='login_no_block'),
        url(r'/login', LoginHandler, name='login'),
        url(r'/register', RegisterHandler, name='register'),
        url(r'/logout', LogoutHandler, name='logout'),
        # url(r'/chat', WebSocketChatHandler, name='wbchat'),
        # url(r'/play', GameScreenHandler, name='game')
        ]

        self.clients = {}
        self.rooms = []
        settings = {
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            "cookie_secret": base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            'xsrf_cookies': False,
            'debug': True,
            'log_file_prefix': "tornado.log",
        }
        tornado.web.Application.__init__(self, handlers, **settings)
        self.syncconnection = pymongo.Connection(MONGO_SERVER, 27017)
        self.syncdb = self.syncconnection["cah-test"]

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()