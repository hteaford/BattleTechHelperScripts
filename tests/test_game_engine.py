"""
Unit tests for game_engine.py
"""

import unittest
from unittest.mock import patch
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import (
    roll_d6, roll_2d6, get_location, build_result,
    calculate_cluster_rows, process_weapon, get_range_mod,
    calculate_target_number, resolve_attack
)
from config import (
    NESTED_BIPED_LOCATION_TABLE, WEAPONS_MANIFEST,
    CLUSTER_HITS_TABLE, RANGE_MOD
)


class TestDiceRolling(unittest.TestCase):
    """Test dice rolling functions."""

    def test_roll_d6_range(self):
        """Test that roll_d6 returns values between 1 and 6."""
        for _ in range(100):
            result = roll_d6()
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 6)

    def test_roll_2d6_range(self):
        """Test that roll_2d6 returns values between 2 and 12."""
        for _ in range(100):
            result = roll_2d6()
            self.assertGreaterEqual(result, 2)
            self.assertLessEqual(result, 12)


class TestLocationLookup(unittest.TestCase):
    """Test hit location functions."""

    @patch('game_engine.roll_2d6')
    def test_get_location_front(self, mock_roll):
        """Test location lookup for front facing."""
        mock_roll.return_value = 7  # Should hit Center Torso
        result = get_location(NESTED_BIPED_LOCATION_TABLE, 'Front')
        self.assertEqual(result, 'Center Torso')

    @patch('game_engine.roll_2d6')
    def test_get_location_left(self, mock_roll):
        """Test location lookup for left facing."""
        mock_roll.return_value = 7  # Should hit Left Torso
        result = get_location(NESTED_BIPED_LOCATION_TABLE, 'Left')
        self.assertEqual(result, 'Left Torso')

    @patch('game_engine.roll_2d6')
    def test_get_location_unknown_roll(self, mock_roll):
        """Test location lookup for invalid roll."""
        mock_roll.return_value = 13  # Invalid roll
        result = get_location(NESTED_BIPED_LOCATION_TABLE, 'Front')
        self.assertEqual(result, 'Unknown')


class TestBuildResult(unittest.TestCase):
    """Test result building function."""

    def test_build_result_structure(self):
        """Test that build_result returns correct dictionary structure."""
        result = build_result('Test Weapon', 5, 7, 'Hit', 'Center Torso', 8)
        expected = {
            'Weapon': 'Test Weapon',
            'TN': 5,
            'Dice Result': 7,
            'Hit/Miss': 'Hit',
            'Location': 'Center Torso',
            'Damage Result': 8
        }
        self.assertEqual(result, expected)


class TestRangeCalculations(unittest.TestCase):
    """Test range and modifier calculations."""

    def test_get_range_mod_short(self):
        """Test short range detection."""
        weapon = WEAPONS_MANIFEST['SL']  # Short: 1, Medium: 2, Long: 3
        bracket, mod = get_range_mod(1, weapon)
        self.assertEqual(bracket, 'Short')
        self.assertEqual(mod, 0)

    def test_get_range_mod_medium(self):
        """Test medium range detection."""
        weapon = WEAPONS_MANIFEST['SL']
        bracket, mod = get_range_mod(2, weapon)
        self.assertEqual(bracket, 'Medium')
        self.assertEqual(mod, RANGE_MOD['Medium'])

    def test_get_range_mod_long(self):
        """Test long range detection."""
        weapon = WEAPONS_MANIFEST['SL']
        bracket, mod = get_range_mod(3, weapon)
        self.assertEqual(bracket, 'Long')
        self.assertEqual(mod, RANGE_MOD['Long'])

    def test_get_range_mod_out_of_range(self):
        """Test out of range detection."""
        weapon = WEAPONS_MANIFEST['SL']
        bracket, mod = get_range_mod(4, weapon)
        self.assertIsNone(bracket)
        self.assertIsNone(mod)


class TestTargetNumberCalculation(unittest.TestCase):
    """Test target number calculations."""

    def test_calculate_target_number_basic(self):
        """Test basic TN calculation."""
        tn = calculate_target_number(4, 0, 2, 0, 0, 0)
        self.assertEqual(tn, 6)  # 4 + 0 + 2 + 0 + 0 + 0

    def test_calculate_target_number_with_modifiers(self):
        """Test TN calculation with all modifiers."""
        tn = calculate_target_number(4, 1, 2, -2, 1, 1)
        self.assertEqual(tn, 7)  # 4 + 1 + 2 + (-2) + 1 + 1


class TestWeaponProcessing(unittest.TestCase):
    """Test weapon attack processing."""

    @patch('game_engine.roll_2d6')
    @patch('game_engine.get_location')
    def test_process_weapon_hit(self, mock_location, mock_roll):
        """Test processing a successful weapon hit."""
        mock_roll.return_value = 7  # Hit
        mock_location.return_value = 'Center Torso'

        weapon_data = WEAPONS_MANIFEST['SL']
        results = process_weapon('SL', weapon_data, 5, 7, NESTED_BIPED_LOCATION_TABLE, 'Front')

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['Hit/Miss'], 'Hit')
        self.assertEqual(results[0]['Location'], 'Center Torso')
        self.assertEqual(results[0]['Damage Result'], 3)

    @patch('game_engine.roll_2d6')
    def test_process_weapon_miss(self, mock_roll):
        """Test processing a weapon miss."""
        mock_roll.return_value = 7  # Doesn't matter for miss

        weapon_data = WEAPONS_MANIFEST['SL']
        results = process_weapon('SL', weapon_data, 8, 7, NESTED_BIPED_LOCATION_TABLE, 'Front')

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['Hit/Miss'], 'Miss')
        self.assertEqual(results[0]['Location'], 'N/A')
        self.assertEqual(results[0]['Damage Result'], 'N/A')


class TestClusterWeapons(unittest.TestCase):
    """Test cluster weapon processing."""

    @patch('game_engine.roll_2d6')
    @patch('game_engine.get_location')
    def test_calculate_cluster_rows_srm6(self, mock_location, mock_roll):
        """Test SRM6 cluster calculation."""
        mock_roll.return_value = 6  # 4 hits on SRM6 table
        mock_location.return_value = 'Center Torso'

        weapon_data = WEAPONS_MANIFEST['SRM6']
        results = calculate_cluster_rows(weapon_data, 5, 7, NESTED_BIPED_LOCATION_TABLE, 'Front')

        # SRM6 with 4 hits should create 4 separate results (ClusterSize=1)
        self.assertEqual(len(results), 4)
        for result in results:
            self.assertEqual(result['Damage Result'], 2)  # MissileDamage=2
            self.assertEqual(result['Location'], 'Center Torso')

    @patch('game_engine.roll_2d6')
    @patch('game_engine.get_location')
    def test_calculate_cluster_rows_lrm10(self, mock_location, mock_roll):
        """Test LRM10 cluster calculation."""
        mock_roll.return_value = 6  # 6 hits on LRM10 table
        mock_location.return_value = 'Center Torso'

        weapon_data = WEAPONS_MANIFEST['LRM10']
        results = calculate_cluster_rows(weapon_data, 5, 7, NESTED_BIPED_LOCATION_TABLE, 'Front')

        # LRM10 with 6 hits and ClusterSize=5 should create 2 results (1 full cluster + 1 remainder)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['Damage Result'], 5)  # 5 * 1 = 5 damage
        self.assertEqual(results[1]['Damage Result'], 1)  # 1 * 1 = 1 damage


class TestResolveAttack(unittest.TestCase):
    """Test complete attack resolution."""

    def test_resolve_attack_invalid_facing(self):
        """Test attack resolution with invalid facing."""
        mech_config = {
            'face': 'Invalid',
            'type': 'Biped',
            'pilot_skill': 4,
            'movement': 'Walk',
            'opponent_tmm': 0
        }
        with self.assertRaises(ValueError):
            resolve_attack(mech_config, ['SL'], 1)

    def test_resolve_attack_invalid_type(self):
        """Test attack resolution with invalid mech type."""
        mech_config = {
            'face': 'Front',
            'type': 'Invalid',
            'pilot_skill': 4,
            'movement': 'Walk',
            'opponent_tmm': 0
        }
        with self.assertRaises(ValueError):
            resolve_attack(mech_config, ['SL'], 1)

    def test_resolve_attack_no_valid_weapons(self):
        """Test attack resolution with no valid weapons."""
        mech_config = {
            'face': 'Front',
            'type': 'Biped',
            'pilot_skill': 4,
            'movement': 'Walk',
            'opponent_tmm': 0
        }
        with self.assertRaises(ValueError):
            resolve_attack(mech_config, ['INVALID'], 1)

    @patch('game_engine.roll_2d6')
    @patch('game_engine.get_location')
    def test_resolve_attack_success(self, mock_location, mock_roll):
        """Test successful attack resolution."""
        mock_roll.return_value = 7  # Hit
        mock_location.return_value = 'Center Torso'

        mech_config = {
            'face': 'Front',
            'type': 'Biped',
            'pilot_skill': 4,
            'movement': 'Walk',
            'opponent_tmm': 0
        }

        result = resolve_attack(mech_config, ['SL'], 1)

        self.assertIn('results', result)
        self.assertIn('total_heat', result)
        self.assertEqual(result['total_heat'], 1)  # SL heat
        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['results'][0]['Hit/Miss'], 'Hit')


if __name__ == '__main__':
    unittest.main()