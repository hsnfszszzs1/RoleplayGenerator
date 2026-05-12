#!/usr/bin/env python3
"""
RoleplayGenerator v1.0 - CLI
"""

import argparse
from core.parameters import RoleplayParameters
from core.roleplay_physics import RoleplayPhysics
from core.prompt_builder import PromptBuilder

def main():
    parser = argparse.ArgumentParser(description="RoleplayGenerator v1.0")
    parser.add_argument("--use-waidrin", action="store_true", help="Use waidrin engine")
    parser.add_argument("--message", type=str, default="Hello there...", help="User message")
    args = parser.parse_args()

    print("🎭 RoleplayGenerator v1.0 - Custom Precision Mode")
    print("=" * 50)

    params = RoleplayParameters(
        character_name="Elias Voss",
        personality_traits="dominant, teasing, sarcastic, secretly caring",
        speech_style="confident, low voice, occasional vulgar",
        setting="rainy penthouse at midnight",
        mood="intense and seductive",
        emotional_intensity="75%",
        sexual_tension=70
    )

    physics = RoleplayPhysics()
    builder = PromptBuilder(params, physics)

    print("\n--- System Prompt Preview ---")
    print(builder.build_system_prompt()[:600] + "...")

    if args.use_waidrin:
        from integrations.waidrin_adapter import WaidrinAdapter
        adapter = WaidrinAdapter(params, physics)
        adapter.initialize_session()
        response = adapter.send_message(args.message)
        print(f"\n[Response]\n{response}")
    else:
        print("\n--- Final Prompt ---")
        print(builder.build_user_prompt(args.message))

if __name__ == "__main__":
    main()