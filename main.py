from PIL import Image
from math import sqrt
from termcolor import colored
import sys
import cv2
from pathlib import *
import colorama
from sys import stdout
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn import datasets
from sklearn import metrics
import tensorflow as tf
import pandas as pd
import random
from time import time
import shutil
from numba import cuda
import csv
import os

argv = None
data = None
RED = 0
GREEN = 0
BLUE = 0
PURPLE = 0
YELLOW = 0
BLACK = 0
WHITE = 0
GREY = 0

def help():
    print("python Yolanda [directory] [type_of_picture] [number_of_frames_per_second] [name] [video_source]")
    exit()

#euclidean difference calculation
def euclidean_difference(value_1, value_2, value_3, value_color_1, value_color_2, value_color_3):
    return(sqrt(( 2 * (value_color_1 - value_1) ** 2) + (4 * (value_color_2 - value_1) ** 2) + (3 * (value_color_3 - value_3) ** 2)))

class Yolanda:
    def __init__(self):
        colorama.init()
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

    #split videos into images
    def create_images(self):
        global argv
        print ('Initialisation...')
        print (colored("Getting Video...\n", 'yellow'))
        self.cam = cv2.VideoCapture(argv[5])
        print (colored("Success, '" + argv[4] + "' opened" , 'green'))
        self.cur_frame = 1
        self.framerate = self.cam.get(cv2.CAP_PROP_FPS)
        self.framerate = self.framerate / float(argv[3])
        self.check_fr = 0
        self.ret, self.frame=self.cam.read()
        while self.ret:
            if self.ret and self.check_fr == float(self.framerate):
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
        print(colored("Video has been turned into images\n\n", "green"))
        self.colors = [[255, 0, 0, "RED"],
        [0, 255, 0, "GREEN"],
        [0, 0, 255, "BLUE"],
        [255, 0, 255, "PURPLE"],
        [255, 255, 0, "YELLOW"],
        [0, 0, 0, "BLACK"],
        [255, 255, 255, "WHITE"],
        [33, 33, 33, "GREY"]]

    #checking args
    def error_management(self):
        global argv
        if (len(argv) > 1):
            if (argv[1] == '--help'):
                help()
        if (len(argv) != 6):
            print (colored("Error : Not enough arguments, --help for help", 'red'))
            exit()

    #variables initalization
    def initialize_main_variables(self):
        global argv
        self.i = 1
        self.a = 1
        self.j = 0
        self.h = -1
        self.trash = 0
        self.res = 1000
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
    
        #print of results
    def print_results(self):
        print (colored("\n\nSUCCESS\n", 'green', attrs=['bold']))
        print (colored("Red : ", 'red'), "%.4f" % (RED * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print (colored("Green : ", 'green'), "%.4f" % (GREEN * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print (colored("Yellow : ", 'yellow'), "%.4f" % (YELLOW * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print (colored("Blue : ", 'blue'), "%.4f" % (BLUE * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print (colored("Purple : ", 'magenta'), "%.4f" % (PURPLE * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print (colored("\n--- --- ---", 'red', attrs=['bold']))
        print ("\nBlack : ", "%.4f" % (BLACK * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print ("White : ", "%.4f" % (WHITE * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")
        print ("Grey : ", "%.4f" % (GREY * 100.00 / ((self.y * self.x) * (self.cm - 1))), "%")

    #Checking images extracted
    def check_files_integrity(self):
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

    # Setting time to display the charging bar and set the bar itself
    def set_time(self):
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

    # Adding colors to globals
    def set_colors(self):
        globals()[self.colors[self.h][3]] += 1

    # get .csv and parse it into pandas dataset
    def get_dataset(self, set):
        global data
        data = pd.read_csv(set, delimiter=',')
        data = data.drop(['NAME'], axis=1)
        data_to_analyse = data.drop(['TYPE'], axis=1)
        data = data[['TYPE']].values.tolist()
        tuples = [tuple(y) for y in data_to_analyse.values]
        return (tuples)

    # KNN
    def neirest_neighbors(self):
        global data
        tuples = self.get_dataset("db.csv")
        nparray = np.array(tuples, dtype=None, copy=True, order='K', subok=False, ndmin=0)
        data = np.ravel(data)
        analysis = np.array(data, dtype=None, copy=True, order='K', subok=False, ndmin=0)
        K = 3
        model = KNeighborsClassifier(n_neighbors = K)
        model.fit(nparray, analysis)
        print (colored("It looks like it is from the genre: ", 'green'))
        res = model.predict([[(RED * 100.00 / ((self.y * self.x) * (self.cm - 1))),(GREEN * 100.00 / ((self.y * self.x) * (self.cm - 1))),(BLUE * 100.00 / ((self.y * self.x) * (self.cm - 1))),(PURPLE * 100.00 / ((self.y * self.x) * (self.cm - 1))),(YELLOW * 100.00 / ((self.y * self.x) * (self.cm - 1))),(GREY * 100.00 / ((self.y * self.x) * (self.cm - 1))),(WHITE * 100.00 / ((self.y * self.x) * (self.cm - 1))),(BLACK * 100.00 / ((self.y * self.x) * (self.cm - 1)))]])
        print(colored(res[0], 'green', attrs=['bold']))
        return (res[0])

    #main loop, checking colors
    def main_loop(self):
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
                        self.nb = euclidean_difference(self.list_c[0], self.list_c[1], self.list_c[2], self.colors[self.j][0], self.colors[self.j][1], self.colors[self.j][2])
                        if (self.nb < self.res):
                            self.res = self.nb
                            self.h = self.j
                        self.j += 1
                    self.set_colors()
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

    # main
    def main(self):
        global argv
        self.error_management()
        self.create_images()
        self.initialize_main_variables()
        self.check_files_integrity()
        print ("Total files : ", colored(self.cm1 - 1, 'green', attrs=['blink']))
        print (colored("Colors being tested :", 'blue'))
        while (self.ptr != 8):
            print (colored(self.colors[self.ptr][3], 'blue', attrs=['dark']))
            self.ptr += 1
        self.set_time()
        self.main_loop()
        self.print_results()
        result = self.neirest_neighbors()
        fd = open("db.csv", "r+")
        fd.seek(0, 2)
        db_res = argv[4] + ',' + str((RED * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str((GREEN * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str((BLUE * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str((PURPLE * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str((YELLOW * 100.00 / ((self.y * self.x) * (self.cm - 1)))) +',' + str((GREY * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str((WHITE * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str((BLACK * 100.00 / ((self.y * self.x) * (self.cm - 1)))) + ',' + str(result) + '\n'
        if (input("\nWould you like to save this in the dataset, as if ? y/N: ") == 'y'):
           fd.write(db_res)
           print(colored('\nDone!', 'green'))
        fd.close()

#checking gpu & calling Yolanda 
if __name__ == "__main__":
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            tf.config.experimental.set_virtual_device_configuration(
                gpus[0],
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024),
                tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPU,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            print(e)
    argv = sys.argv
    Yolanda().main()