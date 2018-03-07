import time

while True:
    f = open('reps_hard_copy.txt', 'r')
    line = f.readline()
    f.close()
    line = line[line.find('(')+1:]
    line = line[:line.find(',')]
    print line
    time.sleep(3)
