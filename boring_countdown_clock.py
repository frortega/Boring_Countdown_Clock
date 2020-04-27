#!/usr/bin/env pythonw
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

# Set default timer values
defHH = 0
defMM = 15
defSS = 0


class countdown_timer(object):
    def __init__(self, HH, MM, SS, song_filename = 'tunes/during.ogg',
                 finish_sound_filename = 'tunes/finish.ogg',
                 play_song = False, 
                 play_finish = True):
        self.song_filename = song_filename
        self.song = None
        self.finish_sound_filename = finish_sound_filename
        self.finish_sound = None
        self.playing = False
        self.play_song_bool = play_song
        self.play_finish_bool = play_finish
        if song_filename is not None:
            self.init_sound_device()
        self.remaining_time = {'hours':int(HH), 'minutes':int(MM), 'seconds':int(SS)}
        self.remaining_time_str = ''
        self.set_remaining_time_str()
        self.total_time = datetime.timedelta(**self.remaining_time) 
        self.start_time = None
        self.end_time = None
        self.updated = True
        self.started = False
        self.finished = False

    def add_hour(self):
        if not self.started:
            self.remaining_time['hours'] += 1
            self.total_time = datetime.timedelta(**self.remaining_time)
            self.set_remaining_time_str()

    def remove_hour(self):
        if not self.started and self.remaining_time['hours'] > 0:
            self.remaining_time['hours'] -= 1
            self.total_time = datetime.timedelta(**self.remaining_time)
            self.set_remaining_time_str()

    def add_minute(self):
        if not self.started and self.remaining_time['minutes'] < 59:
            self.remaining_time['minutes'] += 1
            self.total_time = datetime.timedelta(**self.remaining_time)
            self.set_remaining_time_str()
    
    def remove_minute(self):
        if not self.started and self.remaining_time['minutes'] > 0:
            self.remaining_time['minutes'] -= 1
            self.total_time = datetime.timedelta(**self.remaining_time)
            self.set_remaining_time_str()

    def add_second(self):
        if not self.started and self.remaining_time['seconds'] < 59:
            self.remaining_time['seconds'] += 1
            self.total_time = datetime.timedelta(**self.remaining_time)
            self.set_remaining_time_str()
    
    def remove_second(self):
        if not self.started and self.remaining_time['seconds'] > 0:
            self.remaining_time['seconds'] -= 1
            self.total_time = datetime.timedelta(**self.remaining_time)
            self.set_remaining_time_str()

    def start(self):
        if not self.started:
            self.play_song()
            self.start_time = datetime.datetime.now()
            self.end_time = self.start_time + self.total_time
            self.started = True

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
            one_sec = datetime.timedelta(seconds = 1)  
            time_remaining = self.end_time - current_time + one_sec
            self.remaining_time['hours'] = int(time_remaining.total_seconds()/3600.0)
            self.remaining_time['minutes'] = int((time_remaining.total_seconds() -
                                             self.remaining_time['hours'] * 3600) / 60.0)
            self.remaining_time['seconds'] = int(time_remaining.total_seconds() 
                                            - self.remaining_time['hours'] * 3600   
                                            -  self.remaining_time['minutes'] * 60)
        self.set_remaining_time_str()
    
    def get_remaining_time(self):
        if not self.started:
            self.start()
        self.set_remaining_time()    
        return [self.remaining_time_str, self.remaining_time, self.updated]    
    
    def init_sound_device(self):
        try:
            import pygame
            pygame.init()
            pygame.mixer.init()
            self.song = pygame.mixer.Sound(self.song_filename)
            self.finish_sound = pygame.mixer.Sound(self.finish_sound_filename)
        except ImportError:
            msg = '\n****************************************************\n'
            msg += 'To listen the final tune you need to install pygame.\n'
            msg += 'Use pip install pygame .\n'
            msg += '****************************************************\n'
            print(msg)


    def play_song(self):
        if self.song is not None and self.play_song_bool:
            if not self.playing:
                self.playing = True
                self.song.play(-1)

    def stop_song(self):
        if self.song is not None and self.play_song_bool:
            if self.playing:
                self.playing = False
                self.song.stop()

    def play_finish(self):
        if self.finish_sound is not None and self.play_finish_bool:
            if not self.playing:
                self.finish_sound.play(3)
                self.playing = True
        else:
            print('No song defined.')

       
def tictoc():
    
    if countdown.started:
        # get the remaining time string
        time_str, time_dict, updated = countdown.get_remaining_time()
        # change display every 200 miliseconds if time string was updated
        if updated:
            clock.config(text=time_str)
    else:
        # get and show initial time
        time_str = countdown.remaining_time_str
        clock.config(text=time_str)

    if not countdown.finished:
        clock.after(200, tictoc)
    else:
        countdown.stop_song()
        countdown.play_finish()

def button_add_hour():
    countdown.add_hour()
    time_str = countdown.remaining_time_str
    clock.config(text=time_str)

def button_remove_hour():
    countdown.remove_hour()
    time_str = countdown.remaining_time_str
    clock.config(text=time_str)

def button_add_minute():
    countdown.add_minute()
    time_str = countdown.remaining_time_str
    clock.config(text=time_str)

def button_remove_minute():
    countdown.remove_minute()
    time_str = countdown.remaining_time_str
    clock.config(text=time_str)

def button_add_second():
    countdown.add_second()
    time_str = countdown.remaining_time_str
    clock.config(text=time_str)

def button_remove_second():
    countdown.remove_second()
    time_str = countdown.remaining_time_str
    clock.config(text=time_str)

def button_action():
    if not countdown.started:
        countdown.start()
        start_button.config(text = 'EXIT', command = root.destroy)
        
def button_song():
    if countdown.playing:
        music_button.config(text = 'TURN MUSIC ON')
        countdown.stop_song()
    else:
        music_button.config(text = 'TURN MUSIC OFF')
        countdown.play_song() 
         

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='A basic and boring countdown clock.')
    parser.add_argument('-H', action = 'store', default = defHH, type = int, 
                        required = False,
                        dest = 'hours', help='define hours for countdown (default: 0)')
    parser.add_argument('-M', action = 'store', default = defMM, type = int, 
                        required = False, dest = 'minutes', 
                        help='define minutes for countdown (default: 10 or 0 if -S is given)')
    parser.add_argument('-S', action = 'store', default = defSS, type = int, 
                        required = False, dest = 'seconds', 
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
    parser.add_argument('--no_song', dest='play_song', action='store_const',
                        const=False, default=True,
                        help='if present does not play the default song during countdown.')
    args = parser.parse_args()

    # add rule for default 
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
    clock.pack(fill='both', expand=100, side = tk.TOP)
    countdown = countdown_timer(args.hours, args.minutes, args.seconds,
                                play_song = args.play_song)
    start_button = tk.Button(root, text='START', command=button_action)
    start_button.pack(side = tk.BOTTOM)
    if args.play_song:
        music_button = tk.Button(root, text='TURN MUSIC OFF', command=button_song)
        music_button.pack(side = tk.RIGHT)
    # buttons to setup time
    Hplus = tk.Button(root, text='+H', command=button_add_hour)
    Hplus.pack(side = tk.LEFT)
    Hminus = tk.Button(root, text='-H', command=button_remove_hour)
    Hminus.pack(side = tk.LEFT)

    Mplus = tk.Button(root, text='+M', command=button_add_minute)
    Mplus.pack(side = tk.LEFT)
    Mminus = tk.Button(root, text='-M', command=button_remove_minute)
    Mminus.pack(side = tk.LEFT)
    
    Splus = tk.Button(root, text='+S', command=button_add_second)
    Splus.pack(side = tk.LEFT)
    Sminus = tk.Button(root, text='-S', command=button_remove_second)
    Sminus.pack(side = tk.LEFT)
    tictoc()
    root.mainloop()
