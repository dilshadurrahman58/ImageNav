import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import json

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

file_names = []
running_first_time = True
counter = 0

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'files[]' not in request.files:
		flash('No file part')
		return redirect(request.url)
	files = request.files.getlist('files[]')
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_names.append(filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return render_template('onclickUpload.html', filenames=file_names)



@app.route('/onclickUpload', methods=['POST', 'GET'])
def onClickUpload():
	return render_template('show.html')

@app.route('/show_image', methods=['POST', 'GET'])
def show_image():
	global running_first_time
	global counter
	print("DEBUG: I am inside show_image")
	print("DEBUG: request.method: ", request.method)
	# if (running_first_time == False):
	# 	request.method = 'POST'
	if request.method == 'POST':
		print("I am inside the POST method")
		data_received = request.get_json()
		print(data_received)

		#saving the data to a json file
		with open('data.json', 'a') as f:
			print("DEBUG: I am inside the json data dumping function")
			test = json.dump(data_received.replace("\"", " "), f, indent=3)
			f.write('\n')

		#getting the counter value from the json string
		# data_len = len(data_received)
		# start = (data_len - 3)
		# end = (data_len - 1)
		start = 1
		end = 4
		counter = data_received[start: end]
		if (counter[1] == ','):
			counter = counter[0]
		if (counter[2] == ','):
			counter = counter[0:2]
		counter = int(counter)
		print("Counter: ", counter)
		return render_template('show.html', list_of_images=json.dumps(file_names), counter=counter)
	
	#this is executed only for the first image
	if(running_first_time):
		print("I am not inside the post method")
		running_first_time = False
		return render_template('show.html', list_of_images=json.dumps(file_names), counter=0)
	if(request.method == 'GET'):
		return render_template('show.html', list_of_images=json.dumps(file_names), counter=counter)

	




#For debugging
def utility_functions():
    def print_in_console(message):
        print(str(message))
    return dict(mdebug=print_in_console)

if __name__ == "__main__":
    app.run()