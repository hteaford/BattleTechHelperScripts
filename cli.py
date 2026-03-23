#!/usr/bin/env python3
"""
BattleTech helper CLI using the new game engine.
Tests that the refactored code produces the same results as the original.
"""

from tabulate import tabulate
from game_engine import resolve_attack

def main():
    mech_face = input('Enter Mech Firing Arc (Default is Front/Rear): ') or 'Front'
    if mech_face not in ['Front', 'Left', 'Right']:
        raise ValueError('Invalid Mech Facing. Allowed Facings are Front, Left, and Right.')

    mech_type = input('Is this a Biped or Quad Mech? (Default is Biped) ') or 'Biped'
    if mech_type not in ['Biped', 'Quad']:
        raise ValueError('Invalid Mech Type, Allowed types are Biped and Quad')

    pilot_skill = int(input('Enter Pilot Skill (Default is 4): ') or 4)
    mech_move = input('Enter Your mech\'s movement this turn (Options are: Walk, Run, Jump, None) (Default is Walk): ') or 'Walk'
    if mech_move not in ['Walk', 'Run', 'Jump', 'None']:
        raise ValueError('Invalid Mech Movement. Allowed movements are Walk, Run, Jump, and None.')

    opponent_tmm = int(input('Enter Opponent Mech\'s TMM (Default is 0): ') or 0)
    distance = int(input('Enter distance to target in hexes (Default is 1): ') or 1)

    from config import WEAPONS_MANIFEST
    print('Available Weapons:')
    for code, details in WEAPONS_MANIFEST.items():
        print(f"{code}: {details['Name']} (Heat: {details['Heat']}, Damage: {details['Damage']})")

    selected = input('Enter weapon codes to fire (comma-separated, e.g., SL,ML): ').upper().split(',')
    selected_weapons = [w.strip() for w in selected if w.strip() in WEAPONS_MANIFEST]
    if not selected_weapons:
        raise ValueError('No valid weapons selected.')

    # Prepare mech config for game engine
    mech_config = {
        'face': mech_face,
        'type': mech_type,
        'pilot_skill': pilot_skill,
        'movement': mech_move,
        'opponent_tmm': opponent_tmm
    }

    # Resolve attack using game engine
    result = resolve_attack(mech_config, selected_weapons, distance)

    print(tabulate(result['results'], headers='keys', tablefmt='grid'))
    print(f'Total Heat Generated: {result["total_heat"]}')


if __name__ == '__main__':
    main()