import webapp2
import jinja2
import os
from google.appengine.api import urlfetch
import json
from urllib import urlencode

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class SearchFormHandler(webapp2.RequestHandler):
    def get(self):
        form_template = the_jinja_env.get_template('templates/form.html')
        self.response.write(form_template.render())
    def post(self):
        favorite = self.request.get("favorite")
        form_template = the_jinja_env.get_template('templates/form.html')
        self.response.write(form_template.render())
        self.response.write(favorite)


class RecipeDisplayHandler(webapp2.RequestHandler):
    def post(self):
        query = self.request.get("query")
        ingredients = self.request.get("ingredients")
        base_url = "http://www.recipepuppy.com/api/?"
        params = { "q":query, "i":ingredients }
        response = urlfetch.fetch(base_url + urlencode(params)).content
        results = json.loads(response)
        recipe_template = the_jinja_env.get_template('templates/recipe.html')
        self.response.write(recipe_template.render({
            "results": results
        }))

app = webapp2.WSGIApplication([
    ('/', SearchFormHandler),
    ("/recipe", RecipeDisplayHandler)
], debug=True)
