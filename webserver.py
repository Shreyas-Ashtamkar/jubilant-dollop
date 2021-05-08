# Web Server Requirements
from flask import Flask, request, render_template
from requests import post

negotiator_url = "https://rpi-url-negotiator.herokuapp.com"

v_url = None
app = Flask(__name__)

# Yolo Requirements
from yolov3.utils import Load_Yolo_model, detect_custom
from yolov3.configs import YOLO_INPUT_SIZE

yolo = Load_Yolo_model()

# Multiprocessing Requirements
from multiprocessing import Process, Queue
from json import dumps as toJSON, load as fromJSON

detected_objects = []

@app.route('/', methods=['GET', 'POST'])
def index():
    # if v_url:
    #     print(v_url)
    #     return render_template('index.html', vurl = v_url)
    # else:
    return render_template('index.html', vurl = v_url)

@app.route('/setvurl', methods=['POST'])
def seturl():
    global v_url
    print(request.form.get('vurl'))
    v_url = request.form.get('vurl')
    return ""

@app.route('/unsetvurl', methods=['POST'])
def unseturl():
    global v_url
    v_url = None
    print("url unset")
    return "True"

@app.route('/getvurl', methods=['GET', 'POST'])
def getvurl():
    return v_url

@app.route('/isready', methods=['GET', 'POST'])
def ready():
    return "True"

@app.route('/setobjects', methods=['POST'])
def setObjects():
    global detected_objects
    detected_objects = fromJSON(detected_objects)

@app.route('/getobjects', methods=['GET', 'POST'])
def getObjects():
    detected_objects = ["demo1", "demo2", "demo3"]

    if v_url:
        detected_objects = []
	    for _ in range(2):
	        many_boxes = detect_custom(
	            video_path          = v_url        ,
	            Yolo                = yolo         ,
	            output_path         = ''           , 
	            show                = False        ,
	            score_threshold     = 0.4          ,
	            rectangle_colors    = (255,0,0)
	        )

	        for single_box in many_boxes:
	            if single_box not in detected_objects:
	                detected_objects.append(single_box)

    if request.method=='GET':
        detected_objects = render_template('output.html', vurl = str(v_url), data= detected_objects)
    else:
        detected_objects = toJSON(detected_objects)

    return detected_objects


if __name__=='__main__':
    from pyngrok import ngrok
    myurl = ngrok.connect(8000)
    
    post(negotiator_url+"/seturl", data={"url":myurl.public_url})
    
    app.run(port=8000)

    
