"""
BattleTech game configuration data.
Contains all game tables, weapon definitions, and constants.
"""

# Mech configuration
MECH_FACING = ['Front', 'Left', 'Right']
MECH_ALLOWED_TYPE = ['Biped', 'Quad']

# Hit location tables
NESTED_BIPED_LOCATION_TABLE = {
    2: {'Front': 'Center Torso*', 'Left': 'Left Torso*', 'Right': 'Right Torso*'},
    3: {'Front': 'Right Arm', 'Left': 'Left Leg', 'Right': 'Right Leg'},
    4: {'Front': 'Right Arm', 'Left': 'Left Arm', 'Right': 'Right Arm'},
    5: {'Front': 'Right Leg', 'Left': 'Left Arm', 'Right': 'Right Arm'},
    6: {'Front': 'Right Torso', 'Left': 'Left Leg', 'Right': 'Right Leg'},
    7: {'Front': 'Center Torso', 'Left': 'Left Torso', 'Right': 'Right Torso'},
    8: {'Front': 'Left Torso', 'Left': 'Center Torso', 'Right': 'Center Torso'},
    9: {'Front': 'Left Leg', 'Left': 'Right Torso', 'Right': 'Left Torso'},
    10: {'Front': 'Left Arm', 'Left': 'Right Arm', 'Right': 'Left Arm'},
    11: {'Front': 'Left Arm', 'Left': 'Right Leg', 'Right': 'Left Leg'},
    12: {'Front': 'Head', 'Left': 'Head', 'Right': 'Head'}
}

NESTED_QUAD_LOCATION_TABLE = {
    2: {'Front': 'Center Torso*', 'Left': 'Left Torso*', 'Right': 'Right Torso*'},
    3: {'Front': 'Right Front Leg', 'Left': 'Left Rear Leg', 'Right': 'Right Rear Leg'},
    4: {'Front': 'Right Front Leg', 'Left': 'Left Front Leg', 'Right': 'Right Front Leg'},
    5: {'Front': 'Right Rear Leg', 'Left': 'Left Front Leg', 'Right': 'Right Front Leg'},
    6: {'Front': 'Right Torso', 'Left': 'Left Rear Leg', 'Right': 'Right Rear Leg'},
    7: {'Front': 'Center Torso', 'Left': 'Left Torso', 'Right': 'Right Torso'},
    8: {'Front': 'Left Torso', 'Left': 'Center Torso', 'Right': 'Center Torso'},
    9: {'Front': 'Left Rear Leg', 'Left': 'Right Torso', 'Right': 'Left Torso'},
    10: {'Front': 'Left Front Leg', 'Left': 'Right Front Leg', 'Right': 'Left Front Leg'},
    11: {'Front': 'Left Front Leg', 'Left': 'Right Rear Leg', 'Right': 'Left Rear Leg'},
    12: {'Front': 'Head', 'Left': 'Head', 'Right': 'Head'}
}

# Weapon definitions
WEAPONS_MANIFEST = {
    'SL': {'Name': 'Small Laser', 'Heat': 1, 'Damage': 3, 'Ranges': {'Short': 1, 'Medium': 2, 'Long': 3}, 'Cluster': False, 'SpecialRules': {'to_hit_mod': 0}},
    'ML': {'Name': 'Medium Laser', 'Heat': 3, 'Damage': 5, 'Ranges': {'Short': 3, 'Medium': 7, 'Long': 10}, 'Cluster': False, 'SpecialRules': {'to_hit_mod': 0}},
    'LL': {'Name': 'Large Laser', 'Heat': 5, 'Damage': 8, 'Ranges': {'Short': 5, 'Medium': 10, 'Long': 15}, 'Cluster': False, 'SpecialRules': {'to_hit_mod': 0}},
    'PSL': {'Name': 'Small Pulse Laser', 'Heat': 2, 'Damage': 3, 'Ranges': {'Short': 1, 'Medium': 2, 'Long': 3}, 'Cluster': False, 'SpecialRules': {'to_hit_mod': -2}},
    'PML': {'Name': 'Medium Pulse Laser', 'Heat': 4, 'Damage': 6, 'Ranges': {'Short': 2, 'Medium': 4, 'Long': 6}, 'Cluster': False, 'SpecialRules': {'to_hit_mod': -2}},
    'PLL': {'Name': 'Large Pulse Laser', 'Heat': 10, 'Damage': 9, 'Ranges': {'Short': 3, 'Medium': 7, 'Long': 10}, 'Cluster': False, 'SpecialRules': {'to_hit_mod': -2}},
    'PPC': {'Name': 'Particle Projector Cannon', 'Heat': 10, 'Damage': 10, 'Ranges': {'Short': 3, 'Medium': 6, 'Long': 12}, 'MinRange': 3, 'Cluster': False, 'SpecialRules': {'to_hit_mod': 0}},
    'AC20': {'Name': 'Autocannon/20', 'Heat': 7, 'Damage': 20, 'Ranges': {'Short': 3, 'Medium': 8, 'Long': 15}, 'Cluster': False, 'SpecialRules': {'to_hit_mod': 0}},
    'LRM10': {'Name': 'Long-Range Missile/10', 'Heat': 4, 'Damage': 10, 'Ranges': {'Short': 6, 'Medium': 14, 'Long': 21}, 'MinRange': 6, 'Cluster': True, 'ClusterSize': 5, 'MissileDamage': 1, 'ClusterHitsKey': '10', 'SpecialRules': {'to_hit_mod': 0}},
    'MRM10': {'Name': 'Medium-Range Missile/10', 'Heat': 2, 'Damage': 10, 'Ranges': {'Short': 3, 'Medium': 8, 'Long': 15}, 'Cluster': True, 'ClusterSize': 5, 'MissileDamage': 1, 'ClusterHitsKey': '10', 'SpecialRules': {'to_hit_mod': 1}},
    'SRM6': {'Name': 'Short-Range Missile/6', 'Heat': 4, 'Damage': 6, 'Ranges': {'Short': 3, 'Medium': 6, 'Long': 9}, 'Cluster': True, 'ClusterSize': 1, 'MissileDamage': 2, 'ClusterHitsKey': '6', 'SpecialRules': {'to_hit_mod': 0}}
}

# Cluster weapon hit tables
CLUSTER_HITS_TABLE = {
    '6': {2: 2, 3: 2, 4: 3, 5: 3, 6: 4, 7: 4, 8: 4, 9: 5, 10: 5, 11: 6, 12: 6},
    '10': {2: 3, 3: 4, 4: 5, 5: 6, 6: 6, 7: 6, 8: 6, 9: 8, 10: 8, 11: 10, 12: 10}
}

# Range modifiers
RANGE_MOD = {'Short': 0, 'Medium': 2, 'Long': 4}

# Movement modifiers
MOVEMENT_MODIFIERS = {'Walk': 0, 'Run': 1, 'Jump': 2, 'None': 0}