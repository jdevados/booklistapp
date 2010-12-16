import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from models import Book

from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            template_values = {
               'user' : user.nickname(),  
               'logoutUrl' : users.create_login_url("/")              
            }
            path = os.path.join(os.path.dirname(__file__)+"/templates", 'index.html')
            self.response.out.write(template.render(path, template_values))
            
        else:
            self.redirect(users.create_login_url(self.request.uri))

class NewBookPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__)+"/templates", 'new.html')
        self.response.out.write(template.render(path, {}))
        
class ListBooksPage(webapp.RequestHandler):
    def get(self):
        books = Book.all();
        template_values = {
            'books' : books,                
        }

        path = os.path.join(os.path.dirname(__file__)+"/templates", 'list.html')
        self.response.out.write(template.render(path, template_values))

class SaveBookPage(webapp.RequestHandler):
    def post(self):
        book = Book();
        book.title = self.request.get('title')
        book.author = self.request.get('author')
        book.put()
        self.redirect("/list")

class RemoveBookPage(webapp.RequestHandler):
    def get(self):
        book = Book.get(self.request.get('key'))
        book.delete()
        self.redirect("/list")

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/list', ListBooksPage),
                                      ('/save', SaveBookPage),
                                      ('/remove', RemoveBookPage),
                                      ('/new', NewBookPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()