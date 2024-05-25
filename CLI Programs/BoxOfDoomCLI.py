###Python program to create box of doom rolls.
###Features: Identify firing arc, randomly select number between 2 and 12, output the results in order
###Optional Features: add option to enable house rule through armor crit 
import random
###Variable Collection
DICE_ROLL = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
TOTAL_DICE_TO_ROLL = int(input("Enter Number of Dice to roll(Default of 1): ") or 1)

MECH_FACING = ['Front', 'Left', 'Right']
MECH_FACE = input("Enter Mech Firing Arc(Default is Front/Rear): ")
if not MECH_FACE:
    MECH_FACE = 'Front'
if MECH_FACE not in MECH_FACING:
   raise ValueError("Invalid Mech Facing. Allowed Facings are Front, Left,  and Right.")

MECH_ALLOWED_TYPE = [ 'Biped', 'Quad']
MECH_TYPE = input("Is this a Biped or Quad Mech? (Default is Biped) ")
if not MECH_TYPE:
    MECH_TYPE = 'Biped'
if MECH_TYPE not in MECH_ALLOWED_TYPE:
     raise ValueError("Invalid Mech Type, Allowed types are Biped and Quad")

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
    4: {"Front": 'Right Fron Leg', "Left": 'Left Front Leg', "Right": 'Right Front Leg'},
    5: {"Front": 'Right Rear Leg', "Left": 'Left Front Leg', "Right": 'Right Front Leg'},
    6: {"Front": 'Right Torso', "Left": 'Left Rear Leg', "Right": 'Right Rear Leg'},
    7: {"Front": 'Center Torso', "Left": 'Left Torso', "Right": 'Right Torso'},
    8: {"Front": 'Left Torso', "Left": 'Center Torso', "Right": 'Center Torso'},
    9: {"Front": 'Left Rear Leg', "Left": 'Right Torso', "Right": 'Left Torso'},
    10: {"Front": 'Left Front Leg', "Left": 'Right Front Leg', "Right": 'Left Front Leg'},
    11: {"Front": 'Left Front Leg', "Left": 'Right Rear Leg', "Right": 'Left Rear Leg'},
    12: {"Front": 'Head', "Left": 'Head', "Right": 'Head'}
}

if MECH_TYPE == 'Biped':
    MECH_LOOKUP_TABLE = NESTED_BIPED_LOCATION_TABLE
else:
    MECH_LOOKUP_TABLE = NESTED_QUAD_LOCATION_TABLE
### Function
def DICE_ROLLER():
    DICE_ROLLED = int(random.choice(DICE_ROLL))
    LOCATION = MECH_LOOKUP_TABLE.get(DICE_ROLLED)
    FIRING_ARC_LOCATION = LOCATION[MECH_FACE]
    print(f"Dice roll: {DICE_TO_ROLL} Dice Result: {DICE_ROLLED} Location: {FIRING_ARC_LOCATION}")

#Output Section
for DICE_TO_ROLL in range(TOTAL_DICE_TO_ROLL):
    DICE_ROLLER()