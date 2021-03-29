from app import app
from flask import render_template, request, redirect, jsonify, make_response
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask import send_file, send_from_directory, safe_join, abort, session, url_for
from flask import flash
                   
@app.template_filter("clean_date")
def clean_date(dt):
        return dt.strftime("%d %b %Y %H:%M:%S %A") 

@app.route("/")
def index():
  #      print(app.config)
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
                return redirect (request.url)
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


'''

@app.route("/json", method=["POST"])
def json_example():
        
        # Validate the request body contains JSON
        if request.get_json:

                # Parse the JSON into a Python dictionary
                req = request.get_json()

                # Print the dictionary
                print(req)

                # Return a string along with an HTTP status code
                return "JSON received!", 200

        else:

                # The request body wasn't JSON so return a 400 HTTP status code
                return "Request was not JSON", 400     return 'Thanks!', 200

'''
@app.route("/guestbook")
def guestbook():
        return render_template("public/guestbook.html")

@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():
        

        req = request.get_json()

        print(req)

#        res = make_response(jsonify({"message": "OK"}), 200)
        res = make_response(jsonify(req), 200)

        return res


@app.route("/query")
def query():

        if request.args:

                # We have our query string nicely serialized as a Python dictionary
                args = request.args

                # We'll create a string to display the parameters & values
                serialized = ", ".join(f"{k}: {v}" for k, v in request.args.items())

                # Display the query string to the client in a different format
                return f"(Query) {serialized}", 200

        else:

                return "No query string received", 200 
'''
@app.route("/query")
def query():

        args = request.args

        print(args)
        for k, v in args.items():
                    print(f"{k}: {v}")

        return "No query string received", 200
'''

#app.config["IMAGE_UPLOADS"] = "/home/tech-3/Рабочий стол/test/app/static/img/uploads"
app.config["IMAGE_UPLOADS"] = "/home/lem/PROJECTS/test/app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 4 * 1024 * 1024



def allowed_image(filename):

        if not "." in filename:
                return False

        ext = filename.rsplit(".", 1)[1]

        if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
                return True
        else:
                return False

def allowed_image_filesize(filesize):
        
        if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
                return True
        else:
                return False
                

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

        if request.method == "POST":

                if request.files:

                        if "filesize" in request.cookies:

                                if not allowed_image_filesize(request.cookies["filesize"]):
                                        print("Filesize exceeded maximum limit")
                                        return redirect(request.url)

                        image = request.files["image"]

                        if image.filename == "":
                                print("No filename")
                                return redirect(request.url)

                        if allowed_image(image.filename):
                                filename = secure_filename(image.filename)

                                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                                print("Image saved")

                                return redirect(request.url)

                        else:
                                print("That file extension is not allowed")
                                return redirect(request.url)

        return render_template("public/upload_image.html")


#Learning Flask Ep. 14
# The absolute path of the directory containing images for users to download
app.config["CLIENT_IMAGES"] = "/home/lem/PROJECTS/test/app/static/client/img"

# The absolute path of the directory containing CSV files for users to download
app.config["CLIENT_CSV"] = "/home/lem/PROJECTS/test/app/static/client/csv"

# The absolute path of the directory containing PDF files for users to download
app.config["CLIENT_PDF"] = "/home/lem/PROJECTS/test/app/static/client/pdf"



@app.route("/get-image/<image_name>")
def get_image(image_name):
        try:
                return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True)
        except FileNotFoundError:
                abort(404)

#============================================================
#Flask cookies | Learning Flask Ep. 15
@app.route("/cookies")
def coolies():

        resp = make_response("Cookies")
        cookies = request.cookies
        print(request.cookies)
        
        resp.set_cookie("flavor", "chocolate_chip")
        resp.set_cookie("sex", value="money", max_age=10, path=request.path)
        
        return resp
        

#============================================================                
#The Flask session object | Learning Flask Ep. 16

app.config["SECRET_KEY"] = "OB3Ux3QBsUxCdK0ROCQd_w"


nusers = {
    "julian": {
        "username": "julian",
        "email": "julian@gmail.com",
        "password": "example",
        "bio": "Some guy from the internet"
    },
    "clarissa": {
        "username": "clarissa",
        "email": "clarissa@icloud.com",
        "password": "sweetpotato22",
        "bio": "Sweet potato is life"
    }
}

@app.route("/sign_in", methods=['POST', 'GET'])
def sign_in():
        if request.method == 'POST':
                req = request.form
                print (req)
                username = req.get('username')
                password = req.get('password')

                if not username in nusers:
                        print ("Username not found")
                        return redirect(request.url)
                else:
                        user = nusers[username]

                if not password == user['password']:
                        print ('Incorrect password')
                        return redirect(request.url)
                else:
                        session['USERNAME'] = user['username'] 
                        session['PASSWORD'] = user['password']      
                        print('Session username set')
                        print(session)
                        # return redirect(request.url)
                        return redirect(url_for("user_profile"))

        return render_template('public/sign_in.html')


@app.route("/user_profile")
def user_profile():

        if not session.get("USERNAME") is None:
                # 
                username = session.get("USERNAME")
                user = nusers[username]
                return render_template("public/user_profile.html", user=user)
        else:
                print("No username found is session")
                return redirect(url_for("sign_in"))
        # return render_template("public/user_profile.html", user=user)

@app.route("/sign_out")
def sign_out():

        session.pop("USERNAME", None)
        return redirect(url_for("sign_in"))
        # return '<h2>end</h2>'

#============================================================================
#Flask message flashing | Learning Flask Ep. 17
#============================================================================
        
