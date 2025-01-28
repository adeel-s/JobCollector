from flask import Flask, redirect, url_for, request

app = Flask(__name__)

@app.route('/initialize/<text>')
def initialize(text):
    return 'Initialized: %s' % text
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('initialize', text=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('initialize', text=user))

if __name__ == '__main__':
    app.run(debug=True)

