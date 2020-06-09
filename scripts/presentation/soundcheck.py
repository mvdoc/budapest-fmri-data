#!/usr/bin/env python
"""This script will run part of the movie, and will let the subject choose
the volume. It will then save the volume and use it for the experiment"""
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual, gui, event, logging
from psychopy import sound, core
import time as ptime
import serial
import os
from os.path import join as pjoin, exists as pexists
import json
import csv
import datetime
import shutil

debug = False

# add a new level name called bids
# we will use this level to log information that will be saved
# in the _events.tsv file for this run
BIDS = 26
logging.addLevel(BIDS, 'BIDS')


def logbids(msg, t=None, obj=None):
    """logbids(message)
    logs a BIDS related message
    """
    logging.root.log(msg, level=BIDS, t=t, obj=obj)


logging.console.setLevel(logging.INFO)  # receive nearly all messages
time_template = '%Y%m%dT%H%M%S'


def write_subjectlog(fn, info):
    fieldnames = ['subject_id', 'volume', 'timestamp']
    info_save = {key: info.get(key, '') for key in fieldnames}
    with open(fn, 'ab') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        info_save['timestamp'] = datetime.datetime.now().isoformat()
        writer.writerow(info_save)


def write_subjectvolume(fn, subjdict):
    """subjdict is a dictionary subid -> volume"""
    # read
    if os.path.exists(fn):
        with open(fn, 'rb') as f:
            subjectvolume = json.load(f)
            subjectvolume.update(subjdict)
    else:
        subjectvolume = subjdict
    with open(fn, 'wb') as f:
        json.dump(subjectvolume, f, indent=True)


lastinfo = {
    'subject_id': 'sidXXXXXX',
}

# load config
instructions = """
Loading movie. Please wait.
"""
# fixation_s = config['fixation_s']
fixation_s = 0.5
subjectvolume_fn = 'subjectvolume.json'

# ask info to experimenter
info = {
    'subject_id': lastinfo['subject_id'],
    'scanner?': True
}
infdlg = gui.DlgFromDict(dictionary=info,
                         title="Soundcheck for Movie Presentation",
                         order=['subject_id', 'scanner?']
                         )
if not infdlg.OK:
    core.quit()

subj = info['subject_id']

time = core.Clock()
STIMDIR = "stim"

# log_fn = config['log_template'].format(
#     subj=subj,
#     task_name=config['task_name'],
#     timestamp=ptime.strftime(time_template),
# )
# log_fn = pjoin(RESDIR, log_fn)
# log_responses = logging.LogFile(log_fn, level=logging.INFO)


def move_halted_log(fn=None):
    # flush log
    if fn:
        logging.flush()
        shutil.move(fn, fn.replace('.txt', '__halted.txt'))
    # quit
    core.quit()

# set up global key for quitting; if that happens, log will be moved to
# {log_fn}__halted.txt
event.globalKeys.add(key='q',
                     modifiers=['ctrl'],
                     func=move_halted_log,
                     # func_args=[log_fn],
                     name='quit experiment gracefully')

print "Opening screen"
tbegin = time.getTime()
using_scanner = info['scanner?']
# Setting up visual
if using_scanner:
    size = [1024, 768]
    fullscr = True
    allowGUI = False
else:
    size = [1024, 768]
    fullscr = False
    allowGUI = True
scrwin = visual.Window(size=size,
                       allowGUI=allowGUI, units='pix',
                       screen=0, rgb=[-1, -1, -1],
                       fullscr=fullscr)
# loading movie clip
print "Loading movie part"
#clip = pjoin(STIMDIR, 'budapest_soundcheck.mp4')
clip = pjoin(STIMDIR, 'budapest_soundcheck.mp4')
loading = visual.TextStim(scrwin,
                          text=instructions,
                          height=31)
loading.draw()
scrwin.flip()


def set_volume(movie, volume):
    movie._audioStream.setVolume(volume)


movie = visual.MovieStim3(scrwin, clip,
                          # this looks nice if file is in 16:9
                          # and frame size is 720 x 406
                          size=(1024, 577))
# start with a volume that's halfway
START_VOLUME = 0.20
set_volume(movie, START_VOLUME)

cross_hair = visual.TextStim(scrwin, text='+', height=31,
                             pos=(0, 0), color='#FFFFFF')


intro_msg = """
You will watch a segment of the movie.
You can change the volume using the keypad: '1' will decrease it, while '2' will increase it.

There is a delay between the time you press the button and the time the volume changes,
so wait a couple of seconds before changing the volume again.

Please find a volume that is comfortable and lets you hear the dialogues clearly.
This volume will be used for the entire session.

When in doubt, prefer higher volume.

Ready?
"""
intro = visual.TextStim(scrwin, text=intro_msg, units='pix', wrapWidth=800)

# Start of experiment
intro.draw()
scrwin.flip()
event.waitKeys(keyList=['return'])

# set up timer for experiment starting from first trigger
logging.exp("EXPERIMENT STARTING")
timer_exp = core.Clock()
trunbegin = timer_exp.getTime()
lasttrigger = trunbegin
cross_hair.draw()
scrwin.flip()
# setup bids log
logbids("onset\tduration\tframeidx\tvideotime\tlasttrigger")
# duration will be filled later
template_bids = '{onset:.3f}\t{{duration:.3f}}\t{frameidx}\t{videotime:.3f}' \
                '\t{lasttrigger:.3f}'

# wait for fixation
# core.wait(fixation_s)
while timer_exp.getTime() - trunbegin < fixation_s:
    pass

# start by showing the movie and also a text with the
# instructions to increase the volume
template_instruction = "Press 1 to increase the volume\t" \
                       "Press 2 to decrease the volume\n" \
                       "\t\t\t\tCurrent volume {0:3d}%"
text = visual.TextStim(scrwin, template_instruction.format(int(START_VOLUME*100)),
                       pos=(0, -350), units='pix', wrapWidth=800)
logging.exp("MOVIE STARTING")
logging.flush()
volume = START_VOLUME
while movie.status != visual.FINISHED:
    movie.draw()
    text.draw()
    scrwin.flip()
    keys = event.getKeys(['1', '2'])
    if keys:
        if keys[-1] == '1':
            volume = min(1., volume + 0.05)
        elif keys[-1] == '2':
            volume = max(0., volume - 0.05)
        set_volume(movie, volume)
        text.text = template_instruction.format(int(volume*100))
        logging.exp("Changed volume to {0:.2f}".format(volume))
    if debug and time.getTime() - tbegin > 10:
        break

    # save times
logging.exp("MOVIE FINISHED")
scrwin.flip()
# save volume
subjdictvolume = {info['subject_id']: volume}
write_subjectvolume(subjectvolume_fn, subjdictvolume)
core.wait(2)
# wait 10 seconds at the end
cross_hair.draw()
core.wait(fixation_s)
tend = time.getTime()
logging.exp("EXPERIMENT FINISHED")
logging.exp("Done in {0:.2f}s".format(tend-tbegin))
logging.flush()
scrwin.close()
core.quit()
