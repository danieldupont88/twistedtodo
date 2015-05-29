__author__ = 'dn3'
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor

resource = File('C:\Users\dn3\Desktop\MESTRADO\Sistemas Distribuidos\Projeto Final\static')
factory = Site(resource)
reactor.listenTCP(8888, factory)
reactor.run()