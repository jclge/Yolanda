from functools import partial
from PIL import Image
from math import sqrt
from termcolor import colored
from multiprocessing.dummy import Pool as ThreadPool
import sys
import cv2
from pathlib import *
from sys import stdout
from time import clock
import os

RED = 0
GREEN = 0
BLUE = 0
PURPLE = 0
YELLOW = 0
BLACK = 0
WHITE = 0
GREY = 0


def help():
    print "Usage : -directory -type_of_picture -number_of_picture (starting from 1)"
    exit(0)

def main(argv):
    if (len(argv) > 1):
        if (argv[1] == '--help'):
            help()
    if (len(argv) != 6):
        print colored("Error : Not enough arguments, --help for help", 'red')
        exit(84)
    print 'Initialisation...'
    print colored("Getting Video...\n", 'yellow')
    cam = cv2.VideoCapture(argv[5])
    print colored("Success, '" + argv[4] + "' opened" , 'green')
    cur_frame = 1
    framerate = cam.get(cv2.cv.CV_CAP_PROP_FPS)
    framerate = framerate / int(argv[3])
    check_fr = 0
    ret, frame=cam.read()
    while ret:
        if ret and check_fr == int(framerate):
            if (os.path.exists(argv[1] + str(cur_frame) + argv[2]) == False):
                name = argv[1] + str(cur_frame) + argv[2]
                print "File", colored(name, 'blue'), colored(" Created", 'green')
                cv2.imwrite(name, frame)
            check_fr = 0
            cur_frame += 1
        check_fr += 1
        ret, frame=cam.read()
    cur_frame -= 1
    bar_len = 100
    equal = colored('#', 'green')
    sep = colored('=', 'red')
    seconds = clock()
    colors = [[255, 0, 0, "RED"],
    [0, 255, 0, "GREEN"],
    [0, 0, 255, "BLUE"],
    [255, 0, 255, "PURPLE"],
    [255, 255, 0, "YELLOW"],
    [0, 0, 0, "BLACK"],
    [255, 255, 255, "WHITE"],
    [33, 33, 33, "GREY"]]

    i = 1
    a = 1
    j = 0
    h = -1
    u = '%'
    trash = 0
    res = 1000
    print colored("Video has been turned into images\n\n", "green")
    path = argv[1] + '1' + argv[2]
    image = Image.open(path)
    pic = image.load()
    size = image.size
    cm1 = 1
    check_files = ['0'] * cur_frame
    check_files[0] = 0
    ws = 0
    cm = 1
    ptr = 0
    y = size[0]
    x = size[1]
    path = argv[1] + '%s' + argv[2]
    while (cm1 - 1 != cur_frame):
        if (os.path.exists(path % cm1)):
            trash += 1
        else:
            print 'File ', colored(path % cm1, 'blue'), colored(" FAILED", 'red')
            check_files[ws] = path % cm1
            ws += 1
        cm1 += 1
    if (check_files[0] != 0):
        print colored("Error: Invalid files", 'red', attrs=['bold'])
        ws = 0
        print colored("Incriminated files: ", 'red', attrs=['bold'])
        while check_files[ws] != '0':
            print colored('[', 'red'), colored(check_files[ws], 'blue'), colored(']', 'red')
            ws += 1
        exit(84)
    print "Total files : ", colored(cm1 - 1, 'green', attrs=['blink'])
    print colored("Colors being tested :", 'blue')
    while (ptr != 8):
        print colored(colors[ptr][3], 'blue', attrs=['dark'])
        ptr += 1
    stdout.write('Evolution : \n')
    while (cm != cm1):
        image = Image.open(path % cm)
        pic = image.load()
        while (a != x):
            while (i != y):
                list_c = pic[i, a]
                if (list_c[0] < 30 and list_c[1] < 30 and list_c[2] < 30):
                    h = 5
                    j = 5
                elif (list_c[0] > 225 and list_c[1] > 225 and list_c[2] > 225):
                    h = 6
                    j = 5
                elif (list_c[0] < list_c[1] + 30 and list_c[0] > list_c[1] - 30 and list_c[0] < list_c[2] + 30 and list_c[0] > list_c[2] - 30 and list_c[1] < list_c[2] + 30 and list_c[1] > list_c[2]):
                    h = 7
                    j = 5
                while (j != 5):
                    nb = sqrt(( 2 * (colors[j][0] - list_c[0]) ** 2) + (4 * (colors[j][1] - list_c[1]) ** 2) + (3 * (colors[j][2] - list_c[2]) ** 2))
                    if (nb < res):
                        res = nb
                        h = j
                    j += 1
                globals()[colors[h][3]] += 1
                res = 1000
                h = -1
                j = 0
                i += 1
            a += 1
            i = 1
        cm += 1
        a = 1
        cm2 = cm * 100.00 / cm1
        seconds = clock()
        mins = seconds / 60.00
        filled_len = int(round(bar_len * cm2 / float(100)))
        percents = round(100.0 * cm2 / float(100), 1)
        bar = equal * filled_len + sep * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s%s%.1f%s%s%s\r' % (bar, percents, '%', colored(" Time passed : ", 'green'), mins, " minutes", colored(" Image N*", 'blue'), colored(cm - 1, 'blue')))
        sys.stdout.flush()

    print colored("\n\nSUCCESS\n", 'green', attrs=['bold'])
    print colored("Red : ", 'red'), "%.4f" % (RED * 100.00 / ((y * x) * (cm - 1))), "%"
    print colored("Green : ", 'green'), "%.4f" % (GREEN * 100.00 / ((y * x) * (cm - 1))), "%"
    print colored("Yellow : ", 'yellow'), "%.4f" % (YELLOW * 100.00 / ((y * x) * (cm - 1))), "%"
    print colored("Blue : ", 'blue'), "%.4f" % (BLUE * 100.00 / ((y * x) * (cm - 1))), "%"
    print colored("Purple : ", 'magenta'), "%.4f" % (PURPLE * 100.00 / ((y * x) * (cm - 1))), "%"
    print colored("\n--- --- ---", 'red', attrs=['bold'])
    print "\nBlack : ", "%.4f" % (BLACK * 100.00 / ((y * x) * (cm - 1))), "%"
    print "White : ", "%.4f" % (WHITE * 100.00 / ((y * x) * (cm - 1))), "%"
    print "Grey : ", "%.4f" % (GREY * 100.00 / ((y * x) * (cm - 1))), "%"
    fd = open("db.txt", "rw+")
    fd.seek(0, 2)
    db_res = argv[4] + ' , ' + str((RED * 100.00 / ((y * x) * (cm - 1)))) + ' ; ' + str((GREEN * 100.00 / ((y * x) * (cm - 1)))) + ' ; ' + str((BLUE * 100.00 / ((y * x) * (cm - 1)))) + ' ; ' + str((PURPLE * 100.00 / ((y * x) * (cm - 1)))) + ' ; ' + str((GREY * 100.00 / ((y * x) * (cm - 1)))) + ' ; ' + str((WHITE * 100.00 / ((y * x) * (cm - 1)))) + ' ; ' + str((BLACK * 100.00 / ((y * x) * (cm - 1)))) + '\n'
    fd.write(db_res)
    fd.close()

if __name__ == "__main__":
    main(sys.argv)
