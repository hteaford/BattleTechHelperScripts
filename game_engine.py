"""
BattleTech game engine.
Contains all pure game logic functions with no I/O operations.
"""

import random
from config import (
    MECH_FACING, MECH_ALLOWED_TYPE,
    NESTED_BIPED_LOCATION_TABLE, NESTED_QUAD_LOCATION_TABLE,
    WEAPONS_MANIFEST, CLUSTER_HITS_TABLE, RANGE_MOD, MOVEMENT_MODIFIERS
)


def roll_d6():
    """Roll a single d6 die."""
    return random.randint(1, 6)


def roll_2d6():
    """Roll two d6 dice and return their sum."""
    return roll_d6() + roll_d6()


def get_location(mech_table, face):
    """
    Get hit location based on mech table and facing.

    Args:
        mech_table: Dictionary mapping 2d6 rolls to location dictionaries
        face: String representing mech facing ('Front', 'Left', 'Right')

    Returns:
        String representing the hit location
    """
    roll = roll_2d6()
    lookup = mech_table.get(roll, {})
    return lookup.get(face, 'Unknown')


def build_result(weapon_name, tn, dice_result, hit_miss, location, damage):
    """
    Build a result dictionary for a weapon attack.

    Args:
        weapon_name: Name of the weapon
        tn: Target number
        dice_result: Result of the 2d6 roll
        hit_miss: 'Hit', 'Miss', or other status
        location: Hit location or 'N/A'
        damage: Damage dealt or 'N/A'

    Returns:
        Dictionary with attack result data
    """
    return {
        'Weapon': weapon_name,
        'TN': tn,
        'Dice Result': dice_result,
        'Hit/Miss': hit_miss,
        'Location': location,
        'Damage Result': damage
    }


def calculate_cluster_rows(weapon_data, tn, dice_result, mech_table, face):
    """
    Calculate cluster weapon hits and locations.

    Args:
        weapon_data: Weapon configuration dictionary
        tn: Target number
        dice_result: 2d6 roll result
        mech_table: Mech hit location table
        face: Mech facing

    Returns:
        List of result dictionaries for each cluster hit
    """
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
    """
    Process a single weapon attack.

    Args:
        weapon_code: Weapon code (e.g., 'SL', 'LRM10')
        weapon_data: Weapon configuration dictionary
        tn: Target number
        dice_result: 2d6 roll result
        mech_table: Mech hit location table
        mech_face: Mech facing

    Returns:
        List of result dictionaries (single for non-cluster, multiple for cluster)
    """
    if dice_result < tn:
        return [build_result(weapon_data['Name'], tn, dice_result, 'Miss', 'N/A', 'N/A')]

    if weapon_data['Cluster']:
        return calculate_cluster_rows(weapon_data, tn, dice_result, mech_table, mech_face)

    location = get_location(mech_table, mech_face)
    return [build_result(weapon_data['Name'], tn, dice_result, 'Hit', location, weapon_data['Damage'])]


def get_range_mod(distance, weapon_data):
    """
    Determine range bracket and modifier for a weapon at given distance.

    Args:
        distance: Distance to target in hexes
        weapon_data: Weapon configuration dictionary

    Returns:
        Tuple of (range_bracket, range_modifier) or (None, None) if out of range
    """
    if distance <= weapon_data['Ranges']['Short']:
        return 'Short', 0
    if distance <= weapon_data['Ranges']['Medium']:
        return 'Medium', RANGE_MOD['Medium']
    if distance <= weapon_data['Ranges']['Long']:
        return 'Long', RANGE_MOD['Long']
    return None, None


def calculate_target_number(pilot_skill, movement_mod, range_mod, weapon_mod, opponent_tmm, min_range_penalty):
    """
    Calculate the target number for an attack.

    Args:
        pilot_skill: Pilot's gunnery skill
        movement_mod: Movement modifier
        range_mod: Range modifier
        weapon_mod: Weapon-specific modifier
        opponent_tmm: Opponent's target movement modifier
        min_range_penalty: Minimum range penalty

    Returns:
        Integer target number
    """
    return pilot_skill + movement_mod + range_mod + weapon_mod + opponent_tmm + min_range_penalty


def resolve_attack(mech_config, weapons, distance):
    """
    Resolve a complete attack sequence.

    Args:
        mech_config: Dictionary with mech configuration
            - 'face': Mech facing ('Front', 'Left', 'Right')
            - 'type': Mech type ('Biped', 'Quad')
            - 'pilot_skill': Pilot gunnery skill
            - 'movement': Movement type ('Walk', 'Run', 'Jump', 'None')
            - 'opponent_tmm': Opponent's TMM
        weapons: List of weapon codes to fire
        distance: Distance to target in hexes

    Returns:
        Dictionary with attack results and total heat
    """
    # Validate mech configuration
    if mech_config['face'] not in MECH_FACING:
        raise ValueError(f'Invalid Mech Facing. Allowed Facings are {", ".join(MECH_FACING)}.')

    if mech_config['type'] not in MECH_ALLOWED_TYPE:
        raise ValueError(f'Invalid Mech Type. Allowed types are {", ".join(MECH_ALLOWED_TYPE)}.')

    # Get mech table
    mech_table = NESTED_BIPED_LOCATION_TABLE if mech_config['type'] == 'Biped' else NESTED_QUAD_LOCATION_TABLE

    # Get movement modifier
    movement_mod = MOVEMENT_MODIFIERS.get(mech_config['movement'])
    if movement_mod is None:
        raise ValueError(f'Invalid Mech Movement. Allowed movements are {", ".join(MOVEMENT_MODIFIERS.keys())}.')

    # Validate weapons
    valid_weapons = [w for w in weapons if w in WEAPONS_MANIFEST]
    if not valid_weapons:
        raise ValueError('No valid weapons selected.')

    total_heat = 0
    results = []

    for weapon_code in valid_weapons:
        weapon_data = WEAPONS_MANIFEST[weapon_code]

        # Check range
        bracket, range_mod = get_range_mod(distance, weapon_data)
        if bracket is None:
            results.append(build_result(weapon_data['Name'], 'N/A', 'N/A', 'Unable to fire due to range', 'N/A', 'N/A'))
            total_heat += weapon_data['Heat']
            continue

        # Calculate minimum range penalty
        min_range_penalty = max(0, weapon_data.get('MinRange', 0) + 1 - distance)

        # Calculate target number
        tn = calculate_target_number(
            mech_config['pilot_skill'],
            movement_mod,
            range_mod,
            weapon_data['SpecialRules']['to_hit_mod'],
            mech_config['opponent_tmm'],
            min_range_penalty
        )

        if tn > 12:
            results.append(build_result(weapon_data['Name'], tn, 'N/A', 'Impossible Shot (TN > 12)', 'N/A', 'N/A'))
            total_heat += weapon_data['Heat']
            continue

        # Roll to hit
        dice_result = roll_2d6()
        results.extend(process_weapon(weapon_code, weapon_data, tn, dice_result, mech_table, mech_config['face']))
        total_heat += weapon_data['Heat']

    return {
        'results': results,
        'total_heat': total_heat
    }