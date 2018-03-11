'''
Created on 8 mar. 2018

@author: miglesias
'''

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"   
    
if __name__ == "__main__":
  
    app.run(use_reloader=False)    
    