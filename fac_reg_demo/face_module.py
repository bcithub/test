import os
import face_recognition

UPLOAD_FOLDER = r'D:\SourceCodes\Python\FaceRecognitionDemo\fac_reg_demo\uploads'
TRAIN_FOLDER = r'D:\SourceCodes\Python\FaceRecognitionDemo\fac_reg_demo\known_persons'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

def rec_user(filename, group_id, person_id):
    pathOfKnonwFaces = os.path.join(TRAIN_FOLDER, group_id)
    if not os.path.isdir(pathOfKnonwFaces):
        raise Exception('Invalid Group id.')

    unknown_image = face_recognition.load_image_file(os.path.join(UPLOAD_FOLDER, filename))
    face_locations = face_recognition.face_locations(unknown_image)
    #face_locations = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=0, model="cnn")
    if len(face_locations)==0:
        raise Exception('No face detected.')
    elif len(face_locations)>1:
        raise Exception('Multiple face detected: ' + str(len(face_locations)))
    
    # Load a sample picture and learn how to recognize it.
    # ravi_image = face_recognition.load_image_file("known_persons/Ravindra.jpeg")
    # ravi_face_encoding = face_recognition.face_encodings(ravi_image)[0]
    # nitin_image = face_recognition.load_image_file("known_persons/NitinPaliwal.jpeg")
    # nitin_face_encoding = face_recognition.face_encodings(nitin_image)[0]
    # rajesh_image = face_recognition.load_image_file("known_persons/rajesh.jpeg")
    # rajesh_face_encoding = face_recognition.face_encodings(rajesh_image)[0]

    # Create arrays of known face encodings and their names
    # known_face_encodings = [
    #     ravi_face_encoding,
    #     nitin_face_encoding,
    #     rajesh_face_encoding
    # ]
    # known_face_names = [
    #     "Ravindra Vishwakarma",
    #     "Nitin Paliwal",
    #     "Rajesh Kumar"
    # ]

    #iterate all persons
    known_face_encodings = []
    known_face_names = []
    parent_loop_exit=False
    for entry in os.scandir(pathOfKnonwFaces):
        if parent_loop_exit==True:
            break

        if not isBlank(person_id):
            if person_id != entry.name:
                continue

        for entry1 in os.scandir(entry.path):
            if entry1.is_file():
                #print(entry1.path)
                temp_image = face_recognition.load_image_file(entry1.path)
                temp_face_encoding = face_recognition.face_encodings(temp_image)[0]
                known_face_encodings.append(temp_face_encoding)
                known_face_names.append(entry.name)

    if len(known_face_encodings)==0:
        raise Exception('Please Train Face first.')

    name = "We are unable to recognize your face."
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding, tolerance=0.50)
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    return name
