#!/usr/bin/env python3
"""Move the mouse pointer in a given direction with smooth animation.

Defaults: move 20 pixels to the right with a smooth ease-in/out animation.

Failsafe: you can abort the action by moving the mouse to the
top-left corner (0,0) which raises pyautogui.FailSafeException,
or by pressing Ctrl-C to raise KeyboardInterrupt.
"""

from __future__ import annotations

import argparse
import sys

try:
    import pyautogui
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: pyautogui\n"
        "Install it with: python3 -m pip install pyautogui"
    ) from exc


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Move the mouse smoothly in a direction")
    parser.add_argument(
        "-D",
        "--direction",
        choices=("right", "left", "up", "down"),
        default="right",
        help="Direction to move the mouse",
    )
    parser.add_argument("--distance", type=int, default=20, help="Pixels to move (default: 20)")
    parser.add_argument("--duration", type=float, default=0.5, help="Animation duration in seconds")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    # Ensure the built-in failsafe is enabled (top-left corner abort)
    pyautogui.FAILSAFE = True

    args = parse_args(argv)

    mapping = {
        "right": (args.distance, 0),
        "left": (-args.distance, 0),
        "up": (0, -args.distance),
        "down": (0, args.distance),
    }

    dx, dy = mapping[args.direction]

    try:
        # Smoothly move the mouse using an easing function for smooth start/stop.
        pyautogui.moveRel(dx, dy, duration=args.duration, tween=pyautogui.easeInOutQuad)
    except pyautogui.FailSafeException:
        print("Aborted: mouse moved to top-left failsafe (0,0)")
        return 1
    except KeyboardInterrupt:
        print("Aborted by user (KeyboardInterrupt)")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
