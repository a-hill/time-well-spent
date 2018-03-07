import numpy as np
import cv2
import binascii
import os


class FaceRecognitionJob:
    NET_MODEL = './../openface/models/openface/nn4.small2.v1.t7'
    IMG_DIM = 96

    def __init__(self, image, time, door, output_queue, classifier=None):
        self.image = image
        self.time = time
        self.door = door
        self.output_queue = output_queue
        self.classifier = self.get_rep if classifier is None else classifier

    def run(self):
        print 'starting to run frjob'
        rep = self.classifier(self.image)
        self.output_queue.put([rep, self.time, self.door, self.image])
        print 'finishing frjob'

    @staticmethod
    def get_rep(img):
        string = np.fromstring(img, dtype='uint8')
        rgb_img = cv2.imdecode(string, cv2.IMREAD_COLOR)
        # depends on the while loop in openface_server.lua being commented out

        # set temporary files
        temp_output = '/tmp/openface-temp-out-{}.txt'\
            .format(binascii.b2a_hex(os.urandom(8)))
        temp_input = '/tmp/openface-temp-in-{}.png'\
            .format(binascii.b2a_hex(os.urandom(8)))

        # set up command
        cmd = 'echo ' + temp_input + ' | ' + \
              '/usr/bin/env th ~/openface/openface/openface_server.lua' + \
              ' -model ~/openface/models/openface/nn4.small2.v1.t7' + \
              ' -imgDim 96 > ' + temp_output

        # save img for net
        bgr_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(temp_input, bgr_img)

        # Run Command
        os.system(cmd)

        # get command result from the output file
        with open(temp_output, 'r') as f:
            output = f.readline()

        # remove temp files
        os.remove(temp_output)
        os.remove(temp_input)

        # form rep from output string
        rep = [float(x) for x in output.strip().split(',')]
        rep = np.array(rep)
        return rep
