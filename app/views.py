from app import app
from flask import render_template
from datetime import datetime
from flask import request, redirect


@app.template_filter("clean_date")
def clean_date(dt):
        return dt.strftime("%d %b %Y %H:%M:%S %A") 

@app.route("/")
def index():
	return render_template("public/index.html")


@app.route("/about")
def about():
	return """
        <h1 style='color: red;'>I'm a red H1 heading!</h1>
        <p>This is a lovely little paragraph</p>
        <code>Flask is <em>awesome</em></code>
        """


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
        if request.method == "POST":
                req = request.form
                print (req)
                missing = list()
                for k, v in req.items():
                        if v =="":
                                missing.append(k)
                if missing:
                        feedback = f"Missing fields for {', '.join(missing)}"
                        return render_template("public/sign_up.html", feedback=feedback)
                return redirect (request,url)
        return render_template("public/sign_up.html")        
               

    

@app.route("/jinja")
def jinja():
        # Strings
        my_name = "Djonny"

        # Integers
        my_age = 45

        # Lists
        langs = ["Python", "JavaScript", "Bash", "Ruby", "C", "Rust"]

        # Dictionaries
        friends = {
            "Tony": 43,
            "Cody": 28,
            "Amy": 26,
            "Clarissa": 23,
            "Wendell": 39
        }

        # Tuples
        colors = ("Red", "Blue")

        # Booleans
        cool = True

        # Classes
        class GitRemote:
            def __init__(self, name, description, domain):
                self.name = name
                self.description = description 
                self.domain = domain
			
            def pull(self):
                    return  f'Pullen repo {self.name}'
			
            def clone(self):
                    return f"Cloning into {self.domain}"

            def fff(self):
                    return self.description
                			


        my_remote = GitRemote(
            name="Learning Flask",
            description="Learn the Flask web framework for Python",
            domain="https://github.com/Julian-Nash/learning-flask.git"
        )

        # Functions
        def repeat(x, qty=1):
            return x * qty


        date = datetime.utcnow()

        my_html = "<h1>This is some HTML</h1>"
        suspicious = "<script>alert('NEVER TRUST USER INPUT!')</script>"

        return render_template(
                "public/jinja.html", my_name=my_name, my_age=my_age, langs=langs,
                friends=friends, colors=colors, cool=cool, GitRemote=GitRemote, 
                my_remote=my_remote, repeat=repeat, date=date, my_html=my_html,
                suspicious=suspicious
                )

users = {
        "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creatof of the Flask framework",
        "twitter_handle": "@mitsuhiko"
        },
        "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
         },
        "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor, and engineer",
        "twitter_handle": "@elonmusk"
        }
}

@app.route("/profile/<username>")
def profile(username):
        
        user = None
        
        if username in users:
                user = users[username]
                
        return render_template("public/profile.html", username=username, user=user)

        
@app.route("/multiple/<foo>/<bar>/<baz>")
def multiple(foo, bar, baz):

    print(f"foo is {foo}")
    print(f"bar is {bar}")
    print(f"baz is {baz}")


    return f"foo is {foo}, bar is {bar}, baz is {baz}"
