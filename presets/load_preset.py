"""
Preset Loader for Custom Lead Enrichment Engine

This module provides utilities to load and apply industry-specific signal presets.
Presets are stored as JSON files and can be dynamically loaded at runtime.
"""

import json
import os
from pathlib import Path


class PresetLoader:
    """
    Loads and applies industry-specific signal presets

    Presets are JSON files containing pre-configured signals optimized
    for specific industries. This class handles loading, validation, and
    application of these presets.
    """

    def __init__(self, presets_dir=None):
        """
        Initialize preset loader

        Args:
            presets_dir (str, optional): Path to presets directory.
                                        Defaults to current directory.
        """
        if presets_dir is None:
            # Default to the presets directory
            presets_dir = os.path.dirname(os.path.abspath(__file__))

        self.presets_dir = Path(presets_dir)

    def list_available_presets(self):
        """
        List all available preset files

        Returns:
            list: List of preset names (without .json extension)

        Example:
            loader = PresetLoader()
            presets = loader.list_available_presets()
            # ['devtools', 'hrtech', 'security', ...]
        """
        json_files = self.presets_dir.glob('*.json')
        return sorted([f.stem for f in json_files])

    def load_preset(self, preset_name):
        """
        Load a preset from JSON file

        Args:
            preset_name (str): Name of preset (e.g., 'devtools', 'hrtech')

        Returns:
            dict: Preset configuration containing industry, signals, etc.

        Raises:
            FileNotFoundError: If preset file doesn't exist
            json.JSONDecodeError: If preset file is malformed

        Example:
            loader = PresetLoader()
            preset = loader.load_preset('devtools')
        """
        # Add .json extension if not present
        if not preset_name.endswith('.json'):
            preset_name = f"{preset_name}.json"

        preset_path = self.presets_dir / preset_name

        if not preset_path.exists():
            available = self.list_available_presets()
            raise FileNotFoundError(
                f"Preset '{preset_name}' not found. "
                f"Available presets: {', '.join(available)}"
            )

        with open(preset_path, 'r') as f:
            preset = json.load(f)

        return preset

    def get_preset_info(self, preset_name):
        """
        Get summary information about a preset

        Args:
            preset_name (str): Name of preset

        Returns:
            dict: Summary with industry, description, signal count

        Example:
            loader = PresetLoader()
            info = loader.get_preset_info('devtools')
            print(info['industry'])  # "Developer Tools & API Platforms"
        """
        preset = self.load_preset(preset_name)

        return {
            'industry': preset.get('industry', 'Unknown'),
            'description': preset.get('description', ''),
            'signal_count': len(preset.get('signals', {})),
            'example_companies': preset.get('example_companies', []),
            'typical_use_case': preset.get('typical_use_case', '')
        }

    def apply_preset(self, preset_name):
        """
        Apply a preset to config module

        This loads the preset and updates the global config module with
        the preset's signal definitions.

        Args:
            preset_name (str): Name of preset to apply

        Returns:
            dict: Applied preset configuration

        Example:
            # Apply devtools preset
            loader = PresetLoader()
            preset = loader.apply_preset('devtools')

            # Now use enrichment engine with this preset
            engine = CustomEnrichmentEngine()
            result = engine.enrich_with_custom_signals('stripe.com')
        """
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import config

        preset = self.load_preset(preset_name)

        # Update config with preset signals
        config.CUSTOM_SIGNALS = preset['signals']

        print(f"✓ Applied preset: {preset['industry']}")
        print(f"  Signals loaded: {len(preset['signals'])}")

        return preset

    def compare_presets(self, preset_name1, preset_name2):
        """
        Compare two presets side-by-side

        Args:
            preset_name1 (str): First preset name
            preset_name2 (str): Second preset name

        Returns:
            dict: Comparison data

        Example:
            loader = PresetLoader()
            comparison = loader.compare_presets('devtools', 'security')
        """
        preset1 = self.load_preset(preset_name1)
        preset2 = self.load_preset(preset_name2)

        return {
            'preset1': {
                'name': preset_name1,
                'industry': preset1['industry'],
                'signals': list(preset1['signals'].keys())
            },
            'preset2': {
                'name': preset_name2,
                'industry': preset2['industry'],
                'signals': list(preset2['signals'].keys())
            }
        }


def load_preset(preset_name):
    """
    Convenience function to load a preset

    Args:
        preset_name (str): Name of preset

    Returns:
        dict: Preset configuration

    Example:
        from presets.load_preset import load_preset
        preset = load_preset('devtools')
    """
    loader = PresetLoader()
    return loader.load_preset(preset_name)


def apply_preset(preset_name):
    """
    Convenience function to apply a preset to config

    Args:
        preset_name (str): Name of preset to apply

    Returns:
        dict: Applied preset configuration

    Example:
        from presets.load_preset import apply_preset
        apply_preset('hrtech')
    """
    loader = PresetLoader()
    return loader.apply_preset(preset_name)


if __name__ == '__main__':
    """
    Test preset loader functionality

    Run this script to:
    - List available presets
    - Display info for each preset
    - Test loading functionality
    """
    print("=" * 70)
    print("PRESET LOADER TEST")
    print("=" * 70)

    loader = PresetLoader()

    # List all available presets
    print("\nAvailable Presets:")
    print("-" * 70)
    presets = loader.list_available_presets()

    for preset_name in presets:
        try:
            info = loader.get_preset_info(preset_name)
            print(f"\n{preset_name.upper()}")
            print(f"  Industry: {info['industry']}")
            print(f"  Signals: {info['signal_count']}")
            print(f"  Example Companies: {', '.join(info['example_companies'][:2])}...")
        except Exception as e:
            print(f"\n{preset_name.upper()}: Error loading - {e}")

    # Test loading a specific preset
    print("\n" + "=" * 70)
    print("TESTING PRESET LOAD: DevTools")
    print("=" * 70)

    try:
        preset = loader.load_preset('devtools')
        print(f"\n✓ Successfully loaded: {preset['industry']}")
        print(f"  Description: {preset['description'][:80]}...")
        print(f"\n  Signals:")
        for signal_name, signal_data in preset['signals'].items():
            print(f"    • {signal_name}: {signal_data['weight']}% weight")
    except Exception as e:
        print(f"\n✗ Error: {e}")

    print("\n" + "=" * 70)
    print("✓ Preset loader tests completed")
    print("=" * 70)
