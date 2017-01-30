import webapp2
import re
import cgi

user_regular = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_regular = re.compile(r"^.{3,20}$")
email_regular = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def build_page(error_username='', error_password='', error_verifyPassword='', error_email='', usernamePreserve='', emailPreserve = ''):
    header = """
        <html>
            <head>
                <style>
                    .errorUsername, .errorPassword, .errorVerifyPassword, .errorEmail {
                        color: red;
                    }
                </style>
            </head>
        <body>
            <h1>Signup</h1>"""

    username_label = "<label>Username:</label>"
    username_input = "<input type='text' name='username' value='"+ usernamePreserve +"'' required />"

    password_label = "<label>Password:</label>"
    password_input = "<input type='password' name='password' required />"

    verifyPassword_label = "<label>Verify Password:</label>"
    verifyPassword_input = "<input type='password' name='verifyPassword' required />"

    email_label = "<label>Email (optional):</label>"
    email_input = "<input type='text' name='email' value='" + emailPreserve + "' />"

    errorUsername = "<span class='errorUsername'>  " + error_username + "</span>"
    errorPassword = "<span class='errorPassword'>  " + error_password + "</span>"
    errorVerifyPassword = "<span class='errorVerifyPassword'>  " + error_verifyPassword + "</span>"
    errorEmail = "<span class='errorEmail'>  " + error_email + "</span>"

    submit = "<input type='submit'/>"
    form = ("<form method='post'>" +
            "<table><tr><td>" + username_label + "</td><td>" + username_input + errorUsername + "</td></tr>" +
            "<tr><td>" + password_label + "</td><td>" + password_input + errorPassword + "</td></tr>" +
            "<tr><td>" + verifyPassword_label + "</td><td>" + verifyPassword_input + errorVerifyPassword + "</td></tr>" +
            "<tr><td>" + email_label + "</td><td>" + email_input + errorEmail + "</td></tr></table><br />" +
            submit + "</form></body></html>")

    return header + form

def valid_username(username):
    return user_regular.match(username)

def valid_password(password):
    return password_regular.match(password)

def valid_email(email):
    return email_regular.match(email)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(build_page())

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verifyPassword = self.request.get("verifyPassword")
        email = self.request.get("email")

        checked_username = valid_username(username)
        checked_password = valid_password(password)
        checked_email = valid_email(email)

        username = cgi.escape(username)
        email = cgi.escape(email)

        if not checked_username:
            self.response.write(build_page("Invalid username.", '', '', '', username, email))
        elif not checked_email:
            self.response.write(build_page('', '', '', "Invalid email address.", username, email))
        elif not checked_password:
            self.response.write(build_page('', "Invalid password.", '', '', username, email))
        elif not (password == verifyPassword):
            self.response.write(build_page('', '', "Passwords do not match.", '', username, email))
        else:
            self.redirect("/success?username=" + username)

class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("<center><h1>Welcome, " + self.request.get('username') + "!</h1><img src='http://cdn.inquisitr.com/wp-content/uploads/2010/02/catgif8.gif' /></center>")

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/success', SuccessHandler)
], debug=True)
