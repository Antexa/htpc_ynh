"""
Root for webserver. Specifies frontpage, errorpage (default),
and pages for restarting and shutting down server.
"""
import os
import sys
import cherrypy
import htpc
import logging
from threading import Thread


def do_restart():
    arguments = sys.argv[:]
    arguments.insert(0, sys.executable)
    if sys.platform == 'win32':
        arguments = ['"%s"' % arg for arg in arguments]
    os.chdir(os.getcwd())
    cherrypy.engine.exit()
    os.execv(sys.executable, arguments)

class Root:
    """ Root class """
    def __init__(self):
        """ Do nothing on load """
        self.logger = logging.getLogger('htpc.root')
        pass

    @cherrypy.expose()
    def index(self):
        """ Load template for frontpage """
        return htpc.LOOKUP.get_template('dash.html').render(scriptname='dash')

    @cherrypy.expose()
    def default(self, *args, **kwargs):
        """ Show error if no matching page can be found """
        return "An error occured"

    @cherrypy.expose()
    def shutdown(self):
        """ Shutdown CherryPy and exit script """
        self.logger.info("Shutting down htpc-manager.")
        cherrypy.engine.exit()
        return "HTPC Manager has shut down"

    @cherrypy.tools.json_out()
    @cherrypy.expose()
    def restart(self):
        """ Shutdown script and rerun with the same variables """
        self.logger.info("Restarting htpc-manager.")
        Thread(target=do_restart).start()
        return "Restart in progress."
