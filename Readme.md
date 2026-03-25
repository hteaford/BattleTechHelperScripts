# BattleTech Helper Scripts

A collection of Python utilities for the BattleTech tabletop game, providing dice rolling and hit location calculations through both CLI and GUI interfaces.

## What this is supposed to help with?

I created this repo because I like playing Battletech and I wanted to write some python scripts to help with playing the tabletop game. The project is being refactored for cross-platform deployment (Linux, Android, Windows) using Kivy.

## Project Status

**Phase 1: Game Logic Extraction ✅ COMPLETE**
- ✅ Extracted pure game logic into `game_engine.py`
- ✅ Moved all game data to `config.py`
- ✅ Created comprehensive unit tests (35 tests passing)
- ✅ Created CLI wrapper for testing compatibility

**Phase 2: Kivy GUI (Desktop First) ✅ BASIC IMPLEMENTATION COMPLETE**
- ✅ Created Kivy GUI with mech configuration forms
- ✅ Added weapon selection interface
- ✅ Implemented results display and session history
- ✅ Tested GUI launch on Linux
- 🔄 Needs: Windows testing, UI refinements

**Phase 3: Android APK Build 📋 PLANNED**
- Package for Android deployment
- Test on mobile devices

**Phase 4: Desktop Packaging 📋 PLANNED**
- Create Windows/Linux executables

## Project Structure

```
BattleTechHelperScripts/
├── ProjectPlan.md          # Detailed project plan and phases
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── config.py              # Game data and constants
├── game_engine.py         # Pure game logic functions
├── cli.py                 # CLI wrapper for testing
├── tests/                 # Unit tests
│   ├── test_game_engine.py
│   └── test_config.py
├── legacy/                # Archived old code (future)
└── kivy_app.py            # Kivy GUI (Phase 2)
```

## Requirements

- **Python 3.13** (Kivy currently has compatibility issues with Python 3.14)
- Dependencies listed in `requirements.txt`
- **Cluster Weapons**: SRM6, LRM10, MRM10 with proper hit distribution
- **Range Modifiers**: Short/Medium/Long range bracket detection
- **Target Number Calculation**: Pilot skill + movement + range + weapon modifiers
- **Heat Tracking**: Accumulates heat from all fired weapons

### Planned Features
- **Session History**: Track attack results within a session
- **Equipment Loadouts**: Save and load mech configurations
- **Advanced Rules**: Special ammo types, weapon modes
- **Cross-Platform GUI**: Kivy-based interface for desktop and mobile

## Installation & Usage

### Requirements
- Python 3.8+
- Dependencies: `pip install -r requirements.txt`

### Running Tests
```bash
python -m pytest tests/ -v
```

### CLI Usage
```bash
python cli.py
```

## Development

### Architecture Principles
1. **Separation of Concerns**: Game logic is pure functions with no I/O
2. **Single Source of Truth**: All game data centralized in `config.py`
3. **Testability**: Comprehensive unit tests for all calculations
4. **Extensibility**: Modular design for easy feature additions

### Contributing
1. Run tests before committing: `python -m pytest tests/`
2. Follow existing code style and patterns
3. Add tests for new features
4. Update documentation as needed

## License

This project is for personal use and BattleTech tabletop gaming assistance.