"""
Unit tests for config.py data validation
"""

import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    MECH_FACING, MECH_ALLOWED_TYPE,
    NESTED_BIPED_LOCATION_TABLE, NESTED_QUAD_LOCATION_TABLE,
    WEAPONS_MANIFEST, CLUSTER_HITS_TABLE, RANGE_MOD, MOVEMENT_MODIFIERS
)


class TestMechConfiguration(unittest.TestCase):
    """Test mech configuration data."""

    def test_mech_facing_valid(self):
        """Test that MECH_FACING contains expected values."""
        expected = ['Front', 'Left', 'Right']
        self.assertEqual(MECH_FACING, expected)

    def test_mech_types_valid(self):
        """Test that MECH_ALLOWED_TYPE contains expected values."""
        expected = ['Biped', 'Quad']
        self.assertEqual(MECH_ALLOWED_TYPE, expected)


class TestLocationTables(unittest.TestCase):
    """Test hit location table structure."""

    def test_biped_table_structure(self):
        """Test that biped location table has correct structure."""
        # Should have entries for rolls 2-12
        for roll in range(2, 13):
            self.assertIn(roll, NESTED_BIPED_LOCATION_TABLE)
            locations = NESTED_BIPED_LOCATION_TABLE[roll]
            self.assertIn('Front', locations)
            self.assertIn('Left', locations)
            self.assertIn('Right', locations)

    def test_quad_table_structure(self):
        """Test that quad location table has correct structure."""
        # Should have entries for rolls 2-12
        for roll in range(2, 13):
            self.assertIn(roll, NESTED_QUAD_LOCATION_TABLE)
            locations = NESTED_QUAD_LOCATION_TABLE[roll]
            self.assertIn('Front', locations)
            self.assertIn('Left', locations)
            self.assertIn('Right', locations)

    def test_location_values_not_empty(self):
        """Test that all location entries have non-empty values."""
        for table_name, table in [('Biped', NESTED_BIPED_LOCATION_TABLE),
                                  ('Quad', NESTED_QUAD_LOCATION_TABLE)]:
            with self.subTest(table=table_name):
                for roll, locations in table.items():
                    for facing, location in locations.items():
                        self.assertNotEqual(location, '')
                        self.assertIsNotNone(location)


class TestWeaponsManifest(unittest.TestCase):
    """Test weapon manifest data."""

    def test_weapon_codes_unique(self):
        """Test that all weapon codes are unique."""
        codes = list(WEAPONS_MANIFEST.keys())
        self.assertEqual(len(codes), len(set(codes)))

    def test_weapon_required_fields(self):
        """Test that all weapons have required fields."""
        required_fields = ['Name', 'Heat', 'Damage', 'Ranges', 'Cluster', 'SpecialRules']

        for code, weapon in WEAPONS_MANIFEST.items():
            with self.subTest(weapon=code):
                for field in required_fields:
                    self.assertIn(field, weapon, f"Weapon {code} missing field {field}")

    def test_weapon_ranges_structure(self):
        """Test that weapon ranges have correct structure."""
        for code, weapon in WEAPONS_MANIFEST.items():
            with self.subTest(weapon=code):
                ranges = weapon['Ranges']
                self.assertIn('Short', ranges)
                self.assertIn('Medium', ranges)
                self.assertIn('Long', ranges)

                # Short <= Medium <= Long
                self.assertLessEqual(ranges['Short'], ranges['Medium'])
                self.assertLessEqual(ranges['Medium'], ranges['Long'])

    def test_cluster_weapons_have_cluster_fields(self):
        """Test that cluster weapons have required cluster fields."""
        cluster_required = ['ClusterSize', 'MissileDamage', 'ClusterHitsKey']

        for code, weapon in WEAPONS_MANIFEST.items():
            if weapon['Cluster']:
                with self.subTest(weapon=code):
                    for field in cluster_required:
                        self.assertIn(field, weapon, f"Cluster weapon {code} missing field {field}")

    def test_weapon_damage_positive(self):
        """Test that weapon damage values are positive."""
        for code, weapon in WEAPONS_MANIFEST.items():
            with self.subTest(weapon=code):
                self.assertGreater(weapon['Damage'], 0)
                self.assertGreaterEqual(weapon['Heat'], 0)

    def test_weapon_names_unique(self):
        """Test that weapon names are unique."""
        names = [weapon['Name'] for weapon in WEAPONS_MANIFEST.values()]
        self.assertEqual(len(names), len(set(names)))


class TestClusterHitsTable(unittest.TestCase):
    """Test cluster hits table data."""

    def test_cluster_table_keys_exist(self):
        """Test that cluster table has expected keys."""
        expected_keys = ['6', '10']  # For SRM6 and LRM10/MRM10
        for key in expected_keys:
            self.assertIn(key, CLUSTER_HITS_TABLE)

    def test_cluster_rolls_valid(self):
        """Test that cluster table has valid roll entries (2-12)."""
        for weapon_key, rolls in CLUSTER_HITS_TABLE.items():
            with self.subTest(weapon=weapon_key):
                for roll in range(2, 13):
                    self.assertIn(roll, rolls)
                    hits = rolls[roll]
                    self.assertIsInstance(hits, int)
                    self.assertGreaterEqual(hits, 0)


class TestModifiers(unittest.TestCase):
    """Test modifier constants."""

    def test_range_mod_structure(self):
        """Test that range modifiers have expected structure."""
        expected = {'Short': 0, 'Medium': 2, 'Long': 4}
        self.assertEqual(RANGE_MOD, expected)

    def test_movement_modifiers_structure(self):
        """Test that movement modifiers have expected structure."""
        expected = {'Walk': 0, 'Run': 1, 'Jump': 2, 'None': 0}
        self.assertEqual(MOVEMENT_MODIFIERS, expected)


if __name__ == '__main__':
    unittest.main()