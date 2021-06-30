import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

# Web Server Requirements
from flask import Flask, request, render_template
from requests import post

# Yolo Requirements
from yolov3.utils import Load_Yolo_model, detect_custom
from yolov3.configs import YOLO_INPUT_SIZE

# Multiprocessing Requirements
from json import dumps as toJSON, load as fromJSON

negotiator_url = "https://rpi-url-negotiator.herokuapp.com"

yolo = Load_Yolo_model()

v_url = None
app = Flask(__name__)

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
	v_url = ""
	print("url unset")
	return "True"

@app.route('/getvurl', methods=['GET', 'POST'])
def getvurl():
	return v_url if v_url else ""

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
		detected_objects = detect_custom(
			video_path          = v_url        ,
			Yolo                = yolo         ,
			output_path         = ''           , 
			show                = False        ,
			score_threshold     = 0.4          ,
			rectangle_colors    = (255,0,0)
		)	

	if request.method=='GET':
		detected_objects = render_template('output.html', vurl = str(v_url), data= detected_objects)
	else:
		detected_objects = toJSON(detected_objects)

	return detected_objects


if __name__=='__main__':
	myurl = None
	from pyngrok import ngrok
	try : 
		myurl = ngrok.connect(8000)

		print(myurl.public_url)
		
		post(negotiator_url+"/seturl", data={"url":myurl.public_url})
		
		app.run(port=8000)
	except Exception as e:
		print(e)

	finally:
		if myurl:
			post(negotiator_url+"/unseturl")

	
