from multiprocessing import Process, Queue, Lock
import numpy as np
from termcolor import colored


class FaceManager:
    FACE_MATCH_THRESHOLD = 1.0
    REPS_HARD_COPY_FILE = 'reps_hard_copy.txt'
    TIME_HARD_COPY_FILE = 'cumulative_time_hard_copy.txt'
    MINIMUM_TIME_SPENT_IN_ROOM = 5.0
    SHOULD_LOAD_REPS = False

    def __init__(self, should_load):
        self.entering_faces = Queue()
        self.exiting_faces = Queue()

        self.faces_in_room = []
        self.faces_in_room_lock = Lock()

        self.total_time = 0.0

        self.process = Process(target=self.run)

        self.door_0_queue = Queue()
        self.door_1_queue = Queue()

        if self.SHOULD_LOAD_REPS:
            self.load_reps_from_hard_copy()

        if should_load:
            self.load_total_time_from_hard_copy()

        self.process.start()

    def add_face_to_room(self, new_face):
        self.faces_in_room_lock.acquire()
        already_in_room = []

        for x in self.faces_in_room:
            already_in_room.append(self.faces_match(new_face[0], x[0], 0.5))

        if not any(already_in_room):
            self.faces_in_room.append(new_face)
        self.faces_in_room_lock.release()

    def output_time(self, time_spent, door, exit_time):
        if time_spent > self.MINIMUM_TIME_SPENT_IN_ROOM:
            if door == 0:
                self.door_0_queue.put(time_spent)
            else:
                self.door_1_queue.put(time_spent)

        self.save_total_time_to_hard_copy()

        print('this face was in the room for: ' + str(time_spent) +
              ' seconds. they left by door ' + str(door))

    def get_output_queue(self, door):
        return self.door_0_queue if door == 0 else self.door_1_queue

    def remove_face_from_room(self, new_face):
        # remove all matching faces in the room
        match, not_match = self.partition_faces(new_face)

        self.faces_in_room_lock.acquire()
        self.faces_in_room = not_match
        self.faces_in_room_lock.release()

        matching_entry_times = [face[1] for face in match]

        # only output the longest time found
        if len(matching_entry_times) > 0:
            entry_time = max(matching_entry_times)
            time_in_room = new_face[1] - entry_time
            self.total_time += time_in_room
            self.output_time(time_in_room, new_face[2], new_face[1])

    def partition_faces(self, face):
        self.faces_in_room_lock.acquire()
        match = filter(
            lambda x: self.faces_match(x[0], face[0]), self.faces_in_room)
        not_match = filter(
            lambda x: not self.faces_match(x[0], face[0]), self.faces_in_room)
        self.faces_in_room_lock.release()

        return match, not_match

    def save_reps_to_hard_copy(self):
        f = open(self.REPS_HARD_COPY_FILE, 'w')

        self.faces_in_room_lock.acquire()
        array = np.array(self.faces_in_room)
        np.save(f, array)
        self.faces_in_room_lock.release()

        f.close()

    def load_reps_from_hard_copy(self):
        f = open(self.REPS_HARD_COPY_FILE, 'r')
        array = np.load(f)

        self.faces_in_room_lock.acquire()
        self.faces_in_room = []
        for rep in array:
            self.faces_in_room.append(rep)
        self.faces_in_room_lock.release()

    def save_total_time_to_hard_copy(self):
        f = open(self.TIME_HARD_COPY_FILE, 'w')
        f.write(str(self.get_cumulative_time()))
        f.close()

    def load_total_time_from_hard_copy(self):
        f = open(self.TIME_HARD_COPY_FILE, 'r')
        self.total_time = int(f.readline().rstrip())
        f.close()

    def run(self):
        old_num_faces = 0
        while True:
            if not self.entering_faces.empty():
                print('handling an entering face')
                self.add_face_to_room(self.entering_faces.get())
            new_num_faces = self.get_num_faces()

            if old_num_faces != new_num_faces:
                self.save_reps_to_hard_copy()
                print colored(
                    'number of faces in room: ' + str(new_num_faces), 'green')
            old_num_faces = new_num_faces

            if not self.exiting_faces.empty():
                print('handling an exiting face')
                self.remove_face_from_room(self.exiting_faces.get())

            new_num_faces = self.get_num_faces()
            if old_num_faces != new_num_faces:
                self.save_reps_to_hard_copy()
                print colored(
                    'number of faces in room: ' + str(new_num_faces), 'green')
            old_num_faces = new_num_faces

    def get_num_faces(self):
        self.faces_in_room_lock.acquire()
        num_faces_in_room = len(self.faces_in_room)
        self.faces_in_room_lock.release()
        return num_faces_in_room

    @staticmethod
    def faces_match(a, b, threshold=1.0):
        if a is None or b is None:
            return False

        if len(a) != len(b):  # Check they're same length
            return False

        d = a - b
        dot = np.dot(d, d)
        print colored('dot = ' + str(dot), 'yellow')
        return dot < threshold  # This number comes from openface docs

    def get_cumulative_time(self):
        print colored(
            'total time requested: ' + str(self.total_time), 'yellow')
        return self.total_time
