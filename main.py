import webapp2,logging
from backend import *
from data_processor import *
from google.appengine.ext.webapp import template


class MainHandler(webapp2.RequestHandler):
    def get(self):
        htmlTemplate = 'index.html'
        content = template.render(htmlTemplate,{})
        self.response.write(content)
        
    def post(self):
        name = self.request.get("name")
        #logging.info(name)
        self.response.write(final_call(name))
         
class test1(webapp2.RequestHandler):
    def get(self):
        self.response.write(final_call('tesla'))


app = webapp2.WSGIApplication([
    ('/', MainHandler),('/debug', test1)
], debug=True)
