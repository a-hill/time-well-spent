import urllib, json
import requests
import os

def get_data(entry_filename, exit_filename):
    with open(entry_filename, 'rb') as f:
        img_data = f.read()

    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = '90e67f0f7ef6413aa239f0101aa7be63'

    ## Request headers.
    header = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Request parameters.
    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,emotion'
    })

    api_url = "https://northeurope.api.cognitive.microsoft.com/face/v1.0/detect?%s" % params

    r = requests.post(api_url, headers=header, data=img_data)
    data = r.json()[0]
    emotion = data['faceAttributes']['emotion']

    #get filename data
    entry_filename_split = entry_filename.split('/')
    exit_filename_split = exit_filename.split('/')
    entry_filename = entry_filename_split[len(entry_filename_split)-1]
    exit_filename = exit_filename_split[len(exit_filename_split)-1]
    entry_p = entry_filename.split('.')[0].split('-')
    exit_p = exit_filename.split('.')[0].split('-')
    print exit_p
    print entry_p
    result = {
        'age' : data['faceAttributes']['age'],
        'gender' : data['faceAttributes']['gender'],
        'emotion' : max(emotion, key=emotion.get),
        'entrance time' : entry_p[0],
        'time in room' : int(exit_p[0]) - int(entry_p[0]),
        'entry door' : entry_p[2],
        'exit door' : exit_p[2]
    }

    return result
    

def data_to_csv(data):
    l = [
        str(data['age']), data['gender'], data['emotion'], 
        data['entrance time'], str(data['time in room']), 
        data['entry door'], data['exit door']
    ]

    return ', '.join(l) + '\n'

def get_dirs(baseDir):
    people = os.listdir(baseDir)
    return people

    # TODO:
    # this is the only thing you guys need to do
    # returns a list of pairs of filenames. 
    # first element is the face on entry,
    # second element is the same persons face on exit
    return [['18573-entry-1.jpg', '19432-exit-0.jpg']]

def build_data(output_filename):
    f = open(output_filename, 'w')
    people = os.listdir(baseDir)
    for person in people:
        if person != ".DS_Store":
            first = 0
            second = 1
            filename_pair = os.listdir(baseDir + person)
            while filename_pair[first] == ".DS_Store":
                first = first + 1
            while filename_pair[second] == ".DS_Store" or first == second:
                second = second + 1
            data = get_data(baseDir+person+"/"+filename_pair[first], baseDir+person+"/"+filename_pair[second])
            csv = data_to_csv(data)
            f.write(csv)

    f.close()


baseDir = "/Users/riajha/modern-times/analysis/people/"
build_data('results.csv')
