"""
BattleTech Helper - Kivy GUI Application
Phase 2: Desktop GUI with session history
"""
__version__ = "3.13.0"

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.core.window import Window
import os
import sys
import os

# Configure bundled fonts for cross-platform compatibility
def setup_fonts():
    """Set up bundled fonts for the application."""
    # Get the directory where the executable/script is located
    if hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller bundle
        font_dir = os.path.join(sys._MEIPASS, 'fonts')
    else:
        # Running as script
        font_dir = os.path.join(os.path.dirname(__file__), 'fonts')

    # Register the bundled font
    from kivy.core.text import LabelBase
    font_path = os.path.join(font_dir, 'DejaVuSansMono.ttf')
    if os.path.exists(font_path):
        LabelBase.register(name='monospace', fn_regular=font_path)
        print(f"Registered bundled monospace font: {font_path}")
    else:
        print(f"Bundled font not found: {font_path}")

# Set up fonts before creating the app
setup_fonts()

from game_engine import resolve_attack
from config import WEAPONS_MANIFEST, MECH_FACING, MECH_ALLOWED_TYPE


class AttackResult:
    """Represents a single attack result for display."""
    def __init__(self, weapon, tn, dice_result, hit_miss, location, damage):
        self.weapon = weapon
        self.tn = tn
        self.dice_result = dice_result
        self.hit_miss = hit_miss
        self.location = location
        self.damage = damage


class SessionHistory:
    """Manages session attack history."""
    def __init__(self):
        self.history = []

    def add_attack(self, results, total_heat):
        """Add an attack to history."""
        # Calculate total damage and location breakdown
        total_damage = 0
        location_damage = {}
        hit_count = 0

        for result in results:
            if result['Hit/Miss'] == 'Hit':
                hit_count += 1
                damage = result['Damage Result']
                if isinstance(damage, int):
                    total_damage += damage
                    location = result['Location']
                    location_damage[location] = location_damage.get(location, 0) + damage

        # Format location breakdown
        location_parts = []
        for location, damage in sorted(location_damage.items()):
            location_parts.append(f"{location}: {damage}")

        location_summary = ", ".join(location_parts) if location_parts else "No hits"

        self.history.append({
            'results': results,
            'total_heat': total_heat,
            'total_damage': total_damage,
            'hit_count': hit_count,
            'location_summary': location_summary,
            'timestamp': len(self.history) + 1
        })

    def clear_history(self):
        """Clear all session history."""
        self.history.clear()

    def get_history(self):
        """Get all historical attacks."""
        return self.history


class WeaponRow(BoxLayout):
    """A single weapon selection row with quantity."""

    def __init__(self, weapon_selector, weapon_code='ML', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(40)
        self.weapon_selector = weapon_selector

        # Weapon dropdown
        weapon_codes = list(WEAPONS_MANIFEST.keys())
        self.weapon_spinner = Spinner(
            text=weapon_code if weapon_code in weapon_codes else weapon_codes[0],
            values=weapon_codes,
            size_hint_x=0.6
        )
        self.add_widget(self.weapon_spinner)

        # Quantity input
        self.qty_input = TextInput(
            text='1',
            multiline=False,
            size_hint_x=0.2,
            input_filter='int'
        )
        self.add_widget(self.qty_input)

        # Remove button
        remove_btn = Button(
            text='Remove',
            size_hint_x=0.2,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        remove_btn.bind(on_press=self.remove_row)
        self.add_widget(remove_btn)

    def remove_row(self, instance):
        """Remove this row from weapon selector."""
        self.weapon_selector.remove_row(self)

    def get_weapons(self):
        """Return expanded list of weapon codes for this row."""
        try:
            qty = int(self.qty_input.text or 1)
            qty = max(1, min(qty, 6))  # Clamp to 1-6
        except ValueError:
            qty = 1
        return [self.weapon_spinner.text] * qty


class WeaponSelector(BoxLayout):
    """Widget for selecting weapons to fire with quantities."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(180)
        self.weapon_rows = []

        # Title
        self.add_widget(Label(text='Select Weapons to Fire', size_hint_y=None, height=dp(30)))

        # Scrollable container for weapon rows
        self.rows_container = GridLayout(cols=1, size_hint_y=None, spacing=dp(5), padding=dp(5))
        self.rows_container.bind(minimum_height=self.rows_container.setter('height'))

        # Add initial row
        initial_row = WeaponRow(self, weapon_code='ML')
        self.weapon_rows.append(initial_row)
        self.rows_container.add_widget(initial_row)

        scroll = ScrollView(size_hint=(1, None), height=dp(110))
        scroll.add_widget(self.rows_container)
        self.add_widget(scroll)

        # Add Weapon button
        add_btn = Button(
            text='Add Weapon',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        add_btn.bind(on_press=self.add_row)
        self.add_widget(add_btn)

    def add_row(self, instance):
        """Add a new weapon selection row."""
        new_row = WeaponRow(self, weapon_code='ML')
        self.weapon_rows.append(new_row)
        self.rows_container.add_widget(new_row)

    def remove_row(self, row):
        """Remove a weapon selection row."""
        if len(self.weapon_rows) > 1:  # Keep at least one row
            self.weapon_rows.remove(row)
            self.rows_container.remove_widget(row)

    def get_selected_weapons(self):
        """Get expanded list of weapon codes (one per quantity)."""
        weapons = []
        for row in self.weapon_rows:
            weapons.extend(row.get_weapons())
        return weapons


class MechConfig(BoxLayout):
    """Widget for mech configuration inputs."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(260)

        # Mech Facing
        facing_layout = BoxLayout(size_hint_y=None, height=dp(40))
        facing_layout.add_widget(Label(text='Mech Facing:', size_hint_x=0.3))
        self.facing_spinner = Spinner(
            text='Front',
            values=MECH_FACING,
            size_hint_x=0.7
        )
        facing_layout.add_widget(self.facing_spinner)
        self.add_widget(facing_layout)

        # Mech Type
        type_layout = BoxLayout(size_hint_y=None, height=dp(40))
        type_layout.add_widget(Label(text='Mech Type:', size_hint_x=0.3))
        self.type_spinner = Spinner(
            text='Biped',
            values=MECH_ALLOWED_TYPE,
            size_hint_x=0.7
        )
        type_layout.add_widget(self.type_spinner)
        self.add_widget(type_layout)

        # Gunnery Skill
        gunnery_layout = BoxLayout(size_hint_y=None, height=dp(40))
        gunnery_layout.add_widget(Label(text='Gunnery Skill:', size_hint_x=0.3))
        self.gunnery_spinner = Spinner(
            text='4',
            values=['0', '1', '2', '3', '4', '5', '6', '7'],
            size_hint_x=0.7
        )
        gunnery_layout.add_widget(self.gunnery_spinner)
        self.add_widget(gunnery_layout)

        # Movement
        move_layout = BoxLayout(size_hint_y=None, height=dp(40))
        move_layout.add_widget(Label(text='Movement:', size_hint_x=0.3))
        self.move_spinner = Spinner(
            text='Walk',
            values=['Walk', 'Run', 'Jump', 'None'],
            size_hint_x=0.7
        )
        move_layout.add_widget(self.move_spinner)
        self.add_widget(move_layout)

        # Opponent TMM
        tmm_layout = BoxLayout(size_hint_y=None, height=dp(40))
        tmm_layout.add_widget(Label(text='Opponent TMM:', size_hint_x=0.3))
        self.tmm_input = TextInput(
            text='0',
            multiline=False,
            size_hint_x=0.7
        )
        tmm_layout.add_widget(self.tmm_input)
        self.add_widget(tmm_layout)

        # Distance
        dist_layout = BoxLayout(size_hint_y=None, height=dp(40))
        dist_layout.add_widget(Label(text='Distance (hexes):', size_hint_x=0.3))
        self.dist_input = TextInput(
            text='1',
            multiline=False,
            size_hint_x=0.7
        )
        dist_layout.add_widget(self.dist_input)
        self.add_widget(dist_layout)

    def get_config(self):
        """Get mech configuration as dictionary."""
        return {
            'face': self.facing_spinner.text,
            'type': self.type_spinner.text,
            'pilot_skill': int(self.gunnery_spinner.text or 4),
            'movement': self.move_spinner.text,
            'opponent_tmm': int(self.tmm_input.text or 0)
        }

    def get_distance(self):
        """Get distance to target."""
        return int(self.dist_input.text or 1)


class ResultsDisplay(BoxLayout):
    """Widget for displaying attack results."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(180)

        # Results title
        self.add_widget(Label(text='Attack Results', size_hint_y=None, height=dp(30)))

        # Scrollable results area
        scroll = ScrollView(size_hint_y=None, height=dp(120))
        self.results_text = TextInput(
            readonly=True,
            multiline=True,
            size_hint_y=None,
            font_name='monospace'  # Use our bundled monospace font
        )
        self.results_text.bind(minimum_height=self.results_text.setter('height'))
        scroll.add_widget(self.results_text)
        self.add_widget(scroll)

        # Heat display
        self.heat_label = Label(
            text='Total Heat: 0',
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(self.heat_label)

    def display_results(self, results, total_heat):
        """Display attack results."""
        if not results:
            self.results_text.text = "No results to display."
            self.heat_label.text = "Total Heat: 0"
            return

        # Format results as table-like text with weapon names on left, stats on right
        result_lines = []
        result_lines.append("Weapon".ljust(35) + "  " + "TN  Roll  Result    Location        Damage")
        result_lines.append("-" * 85)

        for result in results:
            weapon = str(result['Weapon'])[:34].ljust(35)
            tn = str(result['TN']).rjust(2)
            roll = str(result['Dice Result']).rjust(2)
            hit_miss = str(result['Hit/Miss']).ljust(8)
            location = str(result['Location'])[:14].ljust(14)
            damage = str(result['Damage Result'])
            result_lines.append(f"{weapon}  {tn}   {roll}   {hit_miss}  {location}  {damage}")

        self.results_text.text = "\n".join(result_lines)
        self.heat_label.text = f"Total Heat: {total_heat}"


class HistoryDisplay(BoxLayout):
    """Widget for displaying session history."""

    def __init__(self, session_history, **kwargs):
        super().__init__(**kwargs)
        self.session_history = session_history
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(160)

        # History title
        self.add_widget(Label(text='Session History', size_hint_y=None, height=dp(30)))

        # Scrollable history text area
        scroll = ScrollView(size_hint_y=None, height=dp(90))
        self.history_text = TextInput(
            readonly=True,
            multiline=True,
            size_hint_y=None,
            font_name='monospace'  # Use our bundled monospace font
        )
        self.history_text.bind(minimum_height=self.history_text.setter('height'))
        scroll.add_widget(self.history_text)
        self.add_widget(scroll)

        # Clear history button
        clear_btn = Button(
            text='Clear History',
            size_hint_y=None,
            height=dp(40)
        )
        clear_btn.bind(on_press=self.clear_history)
        self.add_widget(clear_btn)

        self.update_display()

    def update_display(self):
        """Update history display."""
        history = self.session_history.get_history()
        if not history:
            self.history_text.text = "No attacks in session history."
            return

        lines = []
        for attack in history:
            lines.append(f"Attack {attack['timestamp']}: {attack['hit_count']} hits, Total Damage {attack['total_damage']}, Heat {attack['total_heat']}, {attack['location_summary']}")

        self.history_text.text = "\n".join(lines)

    def clear_history(self, instance):
        """Clear session history."""
        self.session_history.clear_history()
        self.update_display()


class BattleTechApp(BoxLayout):
    """Main application layout."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(2)
        self.padding = dp(2)

        # Session history
        self.session_history = SessionHistory()

        # Title
        title = Label(
            text='BattleTech Helper',
            size_hint_y = None,
            height=dp(50),
            font_size=dp(24)
        )
        self.add_widget(title)

        # Mech configuration (fixed height)
        self.mech_config = MechConfig()
        self.add_widget(self.mech_config)

        # Weapon selector (fixed height with internal scroll)
        self.weapon_selector = WeaponSelector()
        self.add_widget(self.weapon_selector)

        # Fire button
        fire_btn = Button(
            text='Fire Weapons',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.8, 0.2, 0.2, 1),
            font_size=dp(18)
        )
        fire_btn.bind(on_press=self.fire_weapons)
        self.add_widget(fire_btn)

        # Results display (fixed height with internal scroll)
        self.results_display = ResultsDisplay()
        self.add_widget(self.results_display)

        # History display (fixed height with internal scroll)
        self.history_display = HistoryDisplay(self.session_history)
        self.add_widget(self.history_display)

    def fire_weapons(self, instance):
        """Execute weapon attack."""
        try:
            # Get configuration
            mech_config = self.mech_config.get_config()
            distance = self.mech_config.get_distance()
            weapons = self.weapon_selector.get_selected_weapons()

            if not weapons:
                self.show_error("No weapons selected!")
                return

            # Resolve attack
            result = resolve_attack(mech_config, weapons, distance)

            # Display results
            self.results_display.display_results(result['results'], result['total_heat'])

            # Add to history
            self.session_history.add_attack(result['results'], result['total_heat'])
            self.history_display.update_display()

        except ValueError as e:
            self.show_error(str(e))
        except Exception as e:
            self.show_error(f"Unexpected error: {str(e)}")

    def show_error(self, message):
        """Show error popup."""
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()


class BattleTechHelperApp(App):
    """Main Kivy application."""

    def build(self):
        """Build the application."""
        # Set window size for desktop
        Window.size = (800, 1000)
        return BattleTechApp()


if __name__ == '__main__':
    BattleTechHelperApp().run()