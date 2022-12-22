from flask import Flask, render_template

app = Flask(__name__)


# Default page.
@app.route("/")
def home():
    return render_template('home.html.j2')


# Adding more pages.
@app.route("/contactUs")
def contact_us():
    return render_template('contactUs.html.j2')


# Main function.
if (__name__ == '__main__'):
    print("started")

    # Run the server
    app.run(host="localhost", port=3000)
