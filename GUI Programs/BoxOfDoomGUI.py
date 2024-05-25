###Python program to create box of doom rolls.
###Features: Identify firing arc, randomly select number between 2 and 12, output the results in order
###Optional Features: add option to enable house rule through armor crit 
import random
import sys
import tkinter as tk
from tkinter import StringVar
from tkinter import IntVar
from tkinter import OptionMenu
class Redirect:
    def __init__(self,widget):
        self.widget = widget
    def write(self, text):
        self.widget.insert('end', text)

# Create the main window
DOOM_BOX = tk.Tk()
DOOM_BOX.title("Box Of Doom")
DOOM_BOX.geometry("820x550")
###Variable Collection
#Dice
DICE_ROLL = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
DOOM_DICE_TO_ROLL = IntVar()
DOOM_DICE_TO_ROLL_DEF = OptionMenu(DOOM_BOX, DOOM_DICE_TO_ROLL, 1)
#Mech Facing
MECH_FACING = ['Front', 'Left', 'Right']
MECH_FACING_DEF = StringVar(DOOM_BOX)
MECH_FACING_DEF.set(MECH_FACING[0])
#Mech Type
MECH_TYPE_OPTIONS = ['Biped', 'Quad']
MECH_TYPE = StringVar(DOOM_BOX)
MECH_TYPE.set(MECH_TYPE_OPTIONS[0])

#Hit Location Tables
NESTED_BIPED_LOCATION_TABLE = {
    2: {"Front": "Center Torso", "Left": "Left Torso", "Right": "Right Torso"},
    3: {"Front": 'Right Arm', "Left": 'Left Leg', "Right": 'Right Leg'},
    4: {"Front": 'Right Arm', "Left": 'Left Arm', "Right": 'Right Arm'},
    5: {"Front": 'Right Leg ', "Left": 'Left Arm', "Right": 'Right Arm'},
    6: {"Front": 'Right Torso', "Left": 'Left Leg', "Right": 'Right Leg'},
    7: {"Front": 'Center Torso', "Left": 'Left Torso', "Right": 'Right Torso'},
    8: {"Front": 'Left Torso', "Left": 'Center Torso', "Right": 'Center Torso'},
    9: {"Front": 'Left Leg', "Left": 'Right Torso', "Right": 'Left Torso'},
    10: {"Front": 'Left Arm', "Left": 'Right Arm', "Right": 'Left Arm' },
    11: {"Front": 'Left Arm', "Left": 'Right Leg', "Right": 'Left Leg'},
    12: {"Front": 'Head', "Left": 'Head', "Right": 'Head'}
}
NESTED_QUAD_LOCATION_TABLE = {
    2: {"Front": "Center Torso", "Left": "Left Torso", "Right": "Right Torso"},
    3: {"Front": 'Right Front Leg', "Left": 'Left Rear Leg', "Right": 'Right Rear Leg'},
    4: {"Front": 'Right Front Leg', "Left": 'Left Front Leg', "Right": 'Right Front Leg'},
    5: {"Front": 'Right Rear Leg', "Left": 'Left Front Leg', "Right": 'Right Front Leg'},
    6: {"Front": 'Right Torso', "Left": 'Left Rear Leg', "Right": 'Right Rear Leg'},
    7: {"Front": 'Center Torso', "Left": 'Left Torso', "Right": 'Right Torso'},
    8: {"Front": 'Left Torso', "Left": 'Center Torso', "Right": 'Center Torso'},
    9: {"Front": 'Left Rear Leg', "Left": 'Right Torso', "Right": 'Left Torso'},
    10: {"Front": 'Left Front Leg', "Left": 'Right Front Leg', "Right": 'Left Front Leg'},
    11: {"Front": 'Left Front Leg', "Left": 'Right Rear Leg', "Right": 'Left Rear Leg'},
    12: {"Front": 'Head', "Left": 'Head', "Right": 'Head'}
}
### Function
def MULTI_ROLL():
    CLEAR_DOOM_RESULTS()
    if MECH_TYPE.get() == 'Quad':
        MECH_LOOKUP_TABLE = NESTED_QUAD_LOCATION_TABLE
    if MECH_TYPE.get() == 'Biped':
        MECH_LOOKUP_TABLE = NESTED_BIPED_LOCATION_TABLE
    DOOM_DICE_TO_ROLL_DEF = int(NUM_OF_DOOM_DICE_ENTRY.get())
    DOOM_DICE_TO_ROLL_DEF += 1
    for DICE_TO_ROLL in range(1,DOOM_DICE_TO_ROLL_DEF):
        DICE_ROLLED = int(random.choice(DICE_ROLL))
        LOCATION = MECH_LOOKUP_TABLE.get(DICE_ROLLED)
        FIRING_ARC_LOCATION = LOCATION[MECH_FACING_DEF.get()]
        print(f"Dice Roll: Dice Roll: {DICE_TO_ROLL} Dice Result: {DICE_ROLLED} Location: {FIRING_ARC_LOCATION}")

def CLEAR_DOOM_RESULTS():
    DOOM_ROLL_RESULTS.delete('1.0', tk.END)

###Widgets
NUM_DICE_OF_DOOM_LABEL = tk.Label(DOOM_BOX, text="Number of Dice")
NUM_OF_DOOM_DICE_ENTRY = tk.Entry(DOOM_BOX)
ROLL_BOX_OF_DOOM_BUTTON = tk.Button(DOOM_BOX, text="Roll Dice", command=MULTI_ROLL)
BOX_OF_DOOM_RESULTS_LABEL = tk.Label(DOOM_BOX, text="Doom Results")
MECH_FACING_LABEL = tk.Label(DOOM_BOX, text="Mech Facing")
MECH_FACING_ENTRY = OptionMenu(DOOM_BOX, MECH_FACING_DEF, *MECH_FACING)
MECH_TYPE_LABEL = tk.Label(DOOM_BOX, text='Type of Mech')
MECH_TYPE_INPUT = OptionMenu(DOOM_BOX, MECH_TYPE, *MECH_TYPE_OPTIONS)
DOOM_ROLL_RESULTS = tk.Text(DOOM_BOX, wrap=tk.WORD)
SCROLL_LABEL = tk.Label(DOOM_BOX, text="Box scrolls, No scroll bar appears" )

sys.stdout = Redirect(DOOM_ROLL_RESULTS)

#Place widgets on the grid
NUM_DICE_OF_DOOM_LABEL.grid(row = 0,column = 0, sticky='w')
NUM_OF_DOOM_DICE_ENTRY.grid(row = 0, column= 1, sticky='w')
MECH_FACING_LABEL.grid(row = 1,column = 0, sticky='w')
MECH_FACING_ENTRY.grid(row = 1,column = 1, sticky='w')
MECH_TYPE_LABEL.grid(row = 2,column = 0, sticky='w')
MECH_TYPE_INPUT.grid(row = 2,column = 1, sticky='w')
ROLL_BOX_OF_DOOM_BUTTON.grid(row = 4,column = 1, sticky='w')
BOX_OF_DOOM_RESULTS_LABEL.grid(row = 5,column = 0, sticky='w')
DOOM_ROLL_RESULTS.grid(row=6, column = 0)
SCROLL_LABEL.grid(row=6, column=1, sticky='wn' )

#Start the GUI event Loop
DOOM_BOX.mainloop()