from flask import Flask, request, render_template

v_url = None

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if v_url:
        print(v_url)
        return render_template('base.html', vurl = v_url)
    else:
        return "url unset"

@app.route('/setvurl', methods=['POST'])
def seturl():
    global v_url
    print(request.form.get('vurl'))
    v_url = request.form.get('vurl')

    return ""

@app.route('/getvurl', methods=['POST'])
def getvurl():
    return v_url

@app.route('/isready', methods=['POST'])
def ready():
    return "True"

if __name__=='__main__':
    app.run(port=8000)
