#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Emman
#
# Created:     17/09/2018
# Copyright:   (c) Emman 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
 return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True)