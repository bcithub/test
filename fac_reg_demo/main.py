import os
import face_recognition
import face_module as fm
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = fm.UPLOAD_FOLDER
app.config['TRAIN_FOLDER'] = fm.TRAIN_FOLDER

@app.route('/')
def test():
    Req_response={
        'status': 200,
        'message': "Welcome to MIND-AI"
    }
    return jsonify(Req_response)

@app.route('/create_group')
def create_group():
    try:
        if 'group_id' in request.headers:
            group_id = request.headers['group_id']
            
            if fm.isBlank(group_id):
                raise Exception("Group id cannot be blank.")

            pathOfGroup = os.path.join(app.config['TRAIN_FOLDER'], group_id)

            if not os.path.isdir(pathOfGroup):
                os.mkdir(pathOfGroup)
            else:
                raise Exception("Group id already created.")

            Req_response={
                'status': 200,
                'message': 'Group id '+ str(group_id) +' created.'
            }
            return jsonify(Req_response)
        else:
            raise Exception("Group id missing")
    except Exception as e:
        Req_response={
            'status': 500,
            'message': str(e)
        }
        return jsonify(Req_response)

@app.route('/create_person')
def create_person():
    try:
        if 'group_id' in request.headers and 'person_id' in request.headers:
            group_id = request.headers['group_id']
            person_id = request.headers['person_id']
            
            if fm.isBlank(group_id):
                raise Exception("Group id cannot be blank.")
            
            if fm.isBlank(person_id):
                raise Exception("Person id cannot be blank.")

            pathOfGroup = os.path.join(app.config['TRAIN_FOLDER'], group_id)

            if os.path.isdir(pathOfGroup):
                pathOfPerson = os.path.join(pathOfGroup, person_id)
                if not os.path.isdir(pathOfPerson):
                    os.mkdir(pathOfPerson)
                else:
                    raise Exception("Person id already exist.")
            else:
                raise Exception("Group id not exist.")

            Req_response={
                'status': 200,
                'message': 'Person id '+ str(person_id) +' created.'
            }
            return jsonify(Req_response)
        else:
            raise Exception("Group id or person id missing")
    except Exception as e:
        Req_response={
            'status': 500,
            'message': str(e)
        }
        return jsonify(Req_response)

@app.route('/rec_image', methods=['POST'])
def rec_image():
    try:
        if request.method == 'POST':
            group_id = ''
            person_id = ''
            if 'group_id' in request.headers:
                group_id = request.headers['group_id']
                if fm.isBlank(group_id):
                    raise Exception("Group id cannot be blank.")
            else:
                raise Exception("Group id missing.")

            if 'person_id' in request.headers:
                person_id = request.headers['person_id']
                if fm.isBlank(person_id):
                    raise Exception("Person id cannot be blank.")

            # check if the post request has the file part
            if 'file' not in request.files:
                raise Exception("No file found.")
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':                
                raise Exception("File name missing.")
            if file and fm.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                Req_response={
                    'status': 200,
                    'message': fm.rec_user(filename,group_id,person_id)
                }
                return jsonify(Req_response)
            raise Exception("Invalid request")
    except Exception as e:
        Req_response={
            'status': 500,
            'message': str(e)
        }
        return jsonify(Req_response)

@app.route('/train_image', methods=['POST'])
def train_image():
    try:
        if request.method == 'POST':
            if 'group_id' in request.headers and 'person_id' in request.headers:
                group_id = request.headers['group_id']
                person_id = request.headers['person_id']
                
                if fm.isBlank(group_id):
                    raise Exception("Group id cannot be blank.")
                
                if fm.isBlank(person_id):
                    raise Exception("Person id cannot be blank.")

                # check if the post request has the file part
                if 'file' not in request.files:
                    raise Exception("No file found.")
                file = request.files['file']
                # if user does not select file, browser also
                # submit an empty part without filename
                if file.filename == '':                
                    raise Exception("File name missing.")
                if file and fm.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    extension = os.path.splitext(filename)[1]
                    new_filename=str(uuid.uuid4()) + extension

                    pathOfPerson = os.path.join(app.config['TRAIN_FOLDER'], group_id, person_id)

                    if not os.path.isdir(pathOfPerson):
                        raise Exception("Person id not exist.")
                    
                    file.save(os.path.join(pathOfPerson, new_filename))
                    Req_response={
                        'status': 200,
                        'message': 'Trained successfully.'
                    }
                    return jsonify(Req_response)
                raise Exception("Invalid request")
            else:
                raise Exception("Group id or person id missing")
    except Exception as e:
        Req_response={
            'status': 500,
            'message': str(e)
        }
        return jsonify(Req_response)


if __name__=="__main__":
    #app.run(port=80, debug=True)
    app.run(debug=True)
