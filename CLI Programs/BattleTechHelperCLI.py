#!/usr/bin/env python3
"""
BattleTech helper CLI with cluster weapon support.
Refactored for clean structure and future PWA/Android adaptation.
"""

import random
from tabulate import tabulate

MECH_FACING = ['Front', 'Left', 'Right']
MECH_ALLOWED_TYPE = ['Biped', 'Quad']

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

CLUSTER_HITS_TABLE = {
    '6': {2: 2, 3: 2, 4: 3, 5: 3, 6: 4, 7: 4, 8: 4, 9: 5, 10: 5, 11: 6, 12: 6},
    '10': {2: 3, 3: 4, 4: 5, 5: 6, 6: 6, 7: 6, 8: 6, 9: 8, 10: 8, 11: 10, 12: 10}
}

RANGE_MOD = {'Short': 0, 'Medium': 2, 'Long': 4}

def roll_d6():
    return random.randint(1, 6)

def roll_2d6():
    return roll_d6() + roll_d6()

def get_location(mech_table, face):
    lookup = mech_table.get(roll_2d6(), {})
    return lookup.get(face, 'Unknown')

def build_result(weapon_name, tn, dice_result, hit_miss, location, damage):
    return {
        'Weapon': weapon_name,
        'TN': tn,
        'Dice Result': dice_result,
        'Hit/Miss': hit_miss,
        'Location': location,
        'Damage Result': damage
    }

def calculate_cluster_rows(weapon_data, tn, dice_result, mech_table, face):
    rows = []
    cluster_roll = roll_2d6()
    cluster_hits_key = weapon_data.get('ClusterHitsKey') or str(weapon_data['Damage'])
    cluster_map = CLUSTER_HITS_TABLE.get(cluster_hits_key)

    if not cluster_map or cluster_roll not in cluster_map:
        # Fallback safe behavior: no cluster hits
        return [build_result(weapon_data['Name'], tn, dice_result, 'Hit', 'N/A', 0)]

    hits = cluster_map[cluster_roll]
    cluster_size = weapon_data['ClusterSize']
    missile_damage = weapon_data['MissileDamage']
    full_clusters = hits // cluster_size
    remainder = hits % cluster_size

    for idx in range(full_clusters):
        damage = cluster_size * missile_damage
        location = get_location(mech_table, face)
        rows.append(build_result(f"{weapon_data['Name']} (Cluster {idx+1})", tn, dice_result, 'Hit', location, damage))

    if remainder > 0:
        location = get_location(mech_table, face)
        rows.append(build_result(f"{weapon_data['Name']} (Cluster {full_clusters + 1})", tn, dice_result, 'Hit', location, remainder * missile_damage))

    return rows


def process_weapon(weapon_code, weapon_data, tn, dice_result, mech_table, mech_face):
    if dice_result < tn:
        return [build_result(weapon_data['Name'], tn, dice_result, 'Miss', 'N/A', 'N/A')]

    if weapon_data['Cluster']:
        return calculate_cluster_rows(weapon_data, tn, dice_result, mech_table, mech_face)

    location = get_location(mech_table, mech_face)
    return [build_result(weapon_data['Name'], tn, dice_result, 'Hit', location, weapon_data['Damage'])]


def get_range_mod(distance, weapon_data):
    if distance <= weapon_data['Ranges']['Short']:
        return 'Short', 0
    if distance <= weapon_data['Ranges']['Medium']:
        return 'Medium', RANGE_MOD['Medium']
    if distance <= weapon_data['Ranges']['Long']:
        return 'Long', RANGE_MOD['Long']
    return None, None


def main():
    mech_face = input('Enter Mech Firing Arc (Default is Front/Rear): ') or 'Front'
    if mech_face not in MECH_FACING:
        raise ValueError('Invalid Mech Facing. Allowed Facings are Front, Left, and Right.')

    mech_type = input('Is this a Biped or Quad Mech? (Default is Biped) ') or 'Biped'
    if mech_type not in MECH_ALLOWED_TYPE:
        raise ValueError('Invalid Mech Type, Allowed types are Biped and Quad')

    mech_table = NESTED_BIPED_LOCATION_TABLE if mech_type == 'Biped' else NESTED_QUAD_LOCATION_TABLE

    pilot_skill = int(input('Enter Pilot Skill (Default is 4): ') or 4)
    mech_move = input('Enter Your mech\'s movement this turn (Options are: Walk, Run, Jump, None) (Default is Walk): ') or 'Walk'
    move_mod = {'Walk': 0, 'Run': 1, 'Jump': 2, 'None': 0}.get(mech_move)
    if move_mod is None:
        raise ValueError('Invalid Mech Movement. Allowed movements are Walk, Run, Jump, and None.')

    opponent_tmm = int(input('Enter Opponent Mech\'s TMM (Default is 0): ') or 0)
    distance = int(input('Enter distance to target in hexes (Default is 1): ') or 1)

    print('Available Weapons:')
    for code, details in WEAPONS_MANIFEST.items():
        print(f"{code}: {details['Name']} (Heat: {details['Heat']}, Damage: {details['Damage']})")

    selected = input('Enter weapon codes to fire (comma-separated, e.g., SL,ML): ').upper().split(',')
    selected_weapons = [w.strip() for w in selected if w.strip() in WEAPONS_MANIFEST]
    if not selected_weapons:
        raise ValueError('No valid weapons selected.')

    total_heat = 0
    results = []

    for weapon_code in selected_weapons:
        weapon_data = WEAPONS_MANIFEST[weapon_code]

        bracket, range_mod = get_range_mod(distance, weapon_data)
        if bracket is None:
            results.append(build_result(weapon_data['Name'], 'N/A', 'N/A', 'Unable to fire due to range', 'N/A', 'N/A'))
            continue

        min_range_penalty = max(0, weapon_data.get('MinRange', 0) + 1 - distance)
        tn = pilot_skill + move_mod + range_mod + weapon_data['SpecialRules']['to_hit_mod'] + opponent_tmm + min_range_penalty

        if tn > 12:
            results.append(build_result(weapon_data['Name'], tn, 'N/A', 'Impossible Shot (TN > 12)', 'N/A', 'N/A'))
            total_heat += weapon_data['Heat']
            continue

        dice_result = roll_2d6()
        results.extend(process_weapon(weapon_code, weapon_data, tn, dice_result, mech_table, mech_face))
        total_heat += weapon_data['Heat']

    print(tabulate(results, headers='keys', tablefmt='grid'))
    print(f'Total Heat Generated: {total_heat}')


if __name__ == '__main__':
    main()
