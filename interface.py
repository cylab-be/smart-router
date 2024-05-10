from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    #app.run(debug=False, port=5000, host="192.168.1.5") # Check if i really need to put the ip of the router
    #app.run(debug=False, port=5000, host="0.0.0.0") # Check if i need to put 0.0.0.0 or the bellow one
    app.run(debug=False, port=5000, host="127.0.0.1")