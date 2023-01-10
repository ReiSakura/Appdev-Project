from flask import Flask, render_template
from routes import app
from data.database import Database
from data.table import Table
import secrets
import string
from uuid import uuid4, UUID

# Main function.
if (__name__ == '__main__'):
    print("started")

    # Run the server
    app.run(debug=True)
