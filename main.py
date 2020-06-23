from PIL import Image
from math import sqrt
from termcolor import colored
import sys
import cv2
from pathlib import *
from sys import stdout
import numpy
import random
from time import time
import shutil
import csv
import os

argv = None

def help():
    print("python Yolanda [directory] [type_of_picture] [number_of_frames_per_second] [name] [video_source]")
    exit()

class Yolanda:
    def __init__(self):
        self.cam = None
        self.cur_frame = None
        self.framerate = None
        self.check_fr = None
        self.ret = None
        self.frame = None
        self.name = None
        self.bar_len = None
        self.equal = None
        self.sep = None
        self.colors = None
        self.i = None
        self.a = None
        self.j = None
        self.h = None
        self.trash = None
        self.res = None
        self.path = None
        self.image = None
        self.size = None
        self.pic = None
        self.cm1 = None
        self.check_files = None
        self.ws = None
        self.cm = None
        self.ptr = None
        self.nb = None
        self.y = None
        self.x = None
        self.total_pix = None
        self.list_c = None
        self.cm2 = None
        self.t0 = None
        self.seconds = None
        self.mins = None
        self.estim = None
        self.filled_len = None
        self.percents = None
        self.remain = None
        self.bar = None
        self.list_c = None
        self.RED = 0
        self.GREEN = 0
        self.BLUE = 0
        self.PURPLE = 0
        self.YELLOW = 0
        self.BLACK = 0
        self.WHITE = 0
        self.GREY = 0

    def main(self):
        global argv
        if (len(argv) > 1):
            if (argv[1] == '--help'):
                help()
        if (len(argv) != 6):
            print (colored("Error : Not enough arguments, --help for help", 'red'))
            exit()
        print ('Initialisation...')
        print (colored("Getting Video...\n", 'yellow'))
        self.cam = cv2.VideoCapture(argv[5])
        print (colored("Success, '" + argv[4] + "' opened" , 'green'))
        self.cur_frame = 1
        self.framerate = self.cam.get(cv2.CAP_PROP_FPS)
        self.framerate = self.framerate / int(argv[3])
        self.check_fr = 0
        self.ret, self.frame=self.cam.read()
        while self.ret:
            if self.ret and self.check_fr == int(self.framerate):
                if (os.path.exists(argv[1] + str(self.cur_frame) + argv[2]) == False):
                    self.name = argv[1] + str(self.cur_frame) + argv[2]
                    print ("File", colored(self.name, 'blue'), colored(" Created", 'green'))
                    cv2.imwrite(self.name, self.frame)
                self.check_fr = 0
                self.cur_frame += 1
            self.check_fr += 1
            self.ret, self.frame=self.cam.read()
        self.cur_frame -= 1
        self.bar_len = 100
        self.equal = colored('#', 'green')
        self.sep = colored('=', 'red')
        self.seconds = time()
        self.colors = [[255, 0, 0, "RED"],
        [0, 255, 0, "GREEN"],
        [0, 0, 255, "BLUE"],
        [255, 0, 255, "PURPLE"],
        [255, 255, 0, "YELLOW"],
        [0, 0, 0, "BLACK"],
        [255, 255, 255, "WHITE"],
        [33, 33, 33, "GREY"]]

        self.i = 1
        self.a = 1
        self.j = 0
        self.h = -1
        self.trash = 0
        self.res = 1000
        print (colored("Video has been turned into images\n\n", "green"))
        self.path = argv[1] + '1' + argv[2]
        self.image = Image.open(self.path)
        self.pic = self.image.load()
        self.size = self.image.size
        self.cm1 = 1
        self.check_files = ['0'] * self.cur_frame
        self.check_files[0] = 0
        self.ws = 0
        self.cm = 1
        self.ptr = 0
        self.y = self.size[0]
        self.x = self.size[1]
        self.total_pix = self.y * self.x
        self.path = argv[1] + '%s' + argv[2]
        while (self.cm1 - 1 != self.cur_frame):
            if (os.path.exists(self.path % self.cm1)):
                self.trash += 1
            else:
                print ('File ', colored(self.path % self.cm1, 'blue'), colored(" FAILED", 'red'))
                self.check_files[self.ws] = self.path % self.cm1
                self.ws += 1
            self.cm1 += 1
        if (self.check_files[0] != 0):
            print (colored("Error: Invalid files", 'red', attrs=['bold']))
            self.ws = 0
            print (colored("Incriminated files: ", 'red', attrs=['bold']))
            while self.check_files[self.ws] != '0':
                print (colored('[', 'red'), colored(self.check_files[self.ws], 'blue'), colored(']', 'red'))
                self.ws += 1
            exit()
        print ("Total files : ", colored(self.cm1 - 1, 'green', attrs=['blink']))
        print (colored("Colors being tested :", 'blue'))
        while (self.ptr != 8):
            print (colored(self.colors[self.ptr][3], 'blue', attrs=['dark']))
            self.ptr += 1
        self.cm2 = self.cm * 100.00 / self.cm1
        self.t0 = time()
        self.seconds = time() - self.t0
        self.mins = self.seconds / 60.00
        self.estim = self.total_pix * 0.0000045 * self.cm1 / 60.00
        print("Estimitated time: ", int(self.estim), " minutes")
        self.filled_len = int(round(self.bar_len * self.cm2 / float(100)))
        self.percents = round(100.0 * self.cm2 / float(100), 1)
        self.bar = self.equal * self.filled_len + self.sep * (self.bar_len - self.filled_len)
        stdout.write('Evolution : \n')
        sys.stdout.write('[%s] %s%s%s%.1f%s%s%s\r' % (self.bar, self.percents, '%', colored(" Time passed : ", 'green'), self.mins, " minutes", colored(" Image N*", 'blue'), colored(self.cm - 1, 'blue')))
        sys.stdout.flush()
        while (self.cm != self.cm1):
            self.image = Image.open(self.path % self.cm)
            self.pic = self.image.load()
            while (self.a != self.x):
                while (self.i != self.y):
                    self.list_c = self.pic[self.i, self.a]
                    if (self.list_c[0] < 30 and self.list_c[1] < 30 and self.list_c[2] < 30):
                        self.h = 5
                        self.j = 5
                    elif (self.list_c[0] > 225 and self.list_c[1] > 225 and self.list_c[2] > 225):
                        self.h = 6
                        self.j = 5
                    elif (self.list_c[0] < self.list_c[1] + 30 and self.list_c[0] > self.list_c[1] - 30 and self.list_c[0] < self.list_c[2] + 30 and self.list_c[0] > self.list_c[2] - 30 and self.list_c[1] < self.list_c[2] + 30 and self.list_c[1] > self.list_c[2]):
                        self.h = 7
                        self.j = 5
                    while (self.j != 5):
                        self.nb = sqrt(( 2 * (self.colors[self.j][0] - self.list_c[0]) ** 2) + (4 * (self.colors[self.j][1] - self.list_c[1]) ** 2) + (3 * (self.colors[self.j][2] - self.list_c[2]) ** 2))
                        if (self.nb < self.res):
                            self.res = self.nb
                            self.h = self.j
                        self.j += 1
                    self.colors[self.h][3] += 1
                    self.res = 1000
                    self.h = -1
                    self.j = 0
                    self.i += 1
                self.a += 1
                self.i = 1
            self.cm += 1
            self.a = 1
            self.cm2 = self.cm * 100.00 / self.cm1
            self.seconds = time() - self.t0
            self.mins = self.seconds / 60.00
            self.filled_len = int(round(self.bar_len * self.cm2 / float(100)))
            self.percents = round(100.0 * self.cm2 / float(100), 1)
            self.bar = self.equal * self.filled_len + self.sep * (self.bar_len - self.filled_len)
            self.remain = (self.mins / self.percents) * (100 - self.percents)
            self.remain = float("{0:.2f}".format(self.remain))
            sys.stdout.write('[%s] %s%s%s%.1f%s%s%s%s%s%s\r' % (self.bar, self.percents, '%', colored(" Time passed : ", 'green'), self.mins, " minutes", colored(" Image N*", 'blue'), colored(self.cm - 1, 'blue'), colored(" Time Remaining: ", 'red'), colored(str(self.remain), 'red'), colored(' minutes       ', 'red')))
            sys.stdout.flush()

        print (colored("\n\nSUCCESS\n", 'green', attrs=['bold']))
        print (colored("Red : ", 'red'), "%.4f" % (self.RED * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print (colored("Green : ", 'green'), "%.4f" % (self.GREEN * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print (colored("Yellow : ", 'yellow'), "%.4f" % (self.YELLOW * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print (colored("Blue : ", 'blue'), "%.4f" % (self.BLUE * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print (colored("Purple : ", 'magenta'), "%.4f" % (self.PURPLE * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print (colored("\n--- --- ---", 'red', attrs=['bold']))
        print ("\nBlack : ", "%.4f" % (self.BLACK * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print ("White : ", "%.4f" % (self.WHITE * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print ("Grey : ", "%.4f" % (self.GREY * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        fd = open("db.csv", "r+")
        fd.seek(0, 2)
        db_res = argv[4] + ',' + str((self.RED * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str((self.GREEN * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str((self.BLUE * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str((self.PURPLE * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str((self.YELLOW * 100.00 / ((self.y * self.x) * (self.cm - 1)))) +',' + str((self.GREY * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str((self.WHITE * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str((self.BLACK * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + '\n'
        fd.write(db_res)
        fd.close()
        for the_file in os.listdir("test/"):
            file_path = os.path.join("test/", the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        filename = 'db.csv'
        raw_data = open(filename, 'rt')
        reader = csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
        x = list(reader)
        data = numpy.array(x)

if __name__ == "__main__":
    argv = sys.argv
    Yolanda().main()