#!/usr/bin/env python
"""
Prof. Francisco Hernan Ortega Culaciati
ortega.francisco@uchile.cl
Departamento de Geofisica - FCFM
Universidad de Chile

April 25, 2020

"""
import sys, argparse
if sys.version_info.major == 2: # Python 2
    import Tkinter as tk
elif sys.version_info.major >= 3:
    import tkinter as tk
else:
    raise NameError('Unsuported Python version {}'.format(sys.version_info.major))

import datetime

class countdown_timer(object):
    def __init__(self, HH, MM, SS, song_filename = 'tunes/bella_ciao.ogg'):
        self.song_filename = song_filename
        self.song = None
        if song_filename is not None:
            self.init_sound_device()
        self.remaining_time = {'hours':int(HH), 'minutes':int(MM), 'seconds':int(SS)}
        self.total_time = datetime.timedelta(**self.remaining_time) 
        self.start_time = datetime.datetime.now()
        self.end_time = self.start_time + self.total_time
        self.updated = True
        self.remaining_time_str = ''
        self.set_remaining_time_str()
        self.finished = False

    def set_remaining_time_str(self):
        if self.remaining_time['hours'] > 0:
            time_str = '{hours:02d}:{minutes:02d}:{seconds:02d}'.format(
                                                                 **self.remaining_time)
        else:
            time_str = '{minutes:02d}:{seconds:02d}'.format(**self.remaining_time)
        if time_str != self.remaining_time_str:
            self.updated = True
        else:
            self.updated = False
        self.remaining_time_str = time_str

    def set_remaining_time(self):
        current_time = datetime.datetime.now()
        if self.end_time <= current_time:
            self.remaining_time = {'hours':0, 'minutes':0, 'seconds':0}
            self.finished = True
        else:   
            time_remaining = self.end_time - current_time
            self.remaining_time['hours'] = int(time_remaining.total_seconds()/3600.0)
            self.remaining_time['minutes'] = int((time_remaining.total_seconds() -
                                             self.remaining_time['hours'] * 3600) / 60.0)
            self.remaining_time['seconds'] = int(time_remaining.total_seconds() 
                                            - self.remaining_time['hours'] * 3600   
                                            -  self.remaining_time['minutes'] * 60)
        self.set_remaining_time_str()
    
    def get_remaining_time(self):
        self.set_remaining_time()    
        return [self.remaining_time_str, self.remaining_time, self.updated]    
    
    def init_sound_device(self):
        try:
            import pygame
            pygame.init()
            pygame.mixer.init()
            self.song = pygame.mixer.Sound(self.song_filename)
        except ImportError:
            msg = '\n****************************************************\n'
            msg += 'To listen the final tune you need to install pygame.\n'
            msg += 'Use pip install pygame .\n'
            msg += '****************************************************\n'
            print(msg)


    def play_song(self):
        if self.song is not None:
            self.song.play()
        else:
            msg = '\n****************************************************\n'
            msg += 'To listen the final tune you need to install pygame.\n'
            msg += 'Use pip install pygame .\n'
            msg += '****************************************************\n'
            print(msg)
       
def tictoc():
    # get the remaining time string
    time_str, time_dict, updated = countdown.get_remaining_time()
    # change display every 200 miliseconds if time string was updated
    if updated:
        clock.config(text=time_str)
    if not countdown.finished:
        clock.after(200, tictoc)
    else:
        countdown.play_song()


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='A basic and boring countdown clock.')
    parser.add_argument('-H', action = 'store', default = 0, type = int, required = False,
                        dest = 'hours', help='define hours for countdown (default: 0)')
    parser.add_argument('-M', action = 'store', default = 10, type = int, 
                        required = False, dest = 'minutes', 
                        help='define minutes for countdown (default: 10 or 0 if -S is given)')
    parser.add_argument('-S', action = 'store', default = 0, type = int, required = False,
                        dest = 'seconds', 
                        help='define seconds for countdown (default: 0)')
    parser.add_argument('--tcolor', action = 'store', default = 'white', type = str, 
                        required = False, dest = 'text_color',
                        help='define Tk color numbers (default: white)')
    parser.add_argument('--bcolor', action = 'store', default = 'black', type = str, 
                        required = False, dest = 'background_color', 
                        help='define Tk background color (default: black)')
    parser.add_argument('--font', action = 'store', default = 'courier', type = str,
                        required = False, dest = 'font',
                        help='define font type of clock numbers (default: courier)')
    parser.add_argument('--font_size', action = 'store', default = 160, type = int,
                        required = False, dest = 'font_size',
                        help='define font type size of clock numbers (default: 160)')
    parser.add_argument('--font_style', action = 'store', default = 'bold', type = str,
                        required = False, dest = 'font_style',
                        help='define font type style of clock numbers (default: bold)')
    args = parser.parse_args()
    print(args)
    print(sys.argv)
    if '-S' in sys.argv:
        if '-M' not in sys.argv:
            # if seconds are given but not minutes explicitly with -M set default
            # minuntes to zero.
            args.minutes = 0
    # initialize basic GUI
    root = tk.Tk()
    root.title("Boring Countdown Clock (http://www.github.com/frortega)")
    font = (args.font, args.font_size, args.font_style)
    clock = tk.Label(root, font= font, bg=args.background_color, fg=args.text_color)
    clock.pack(fill='both', expand=100)
    countdown = countdown_timer(args.hours, args.minutes, args.seconds)


    tictoc()
    root.mainloop()
