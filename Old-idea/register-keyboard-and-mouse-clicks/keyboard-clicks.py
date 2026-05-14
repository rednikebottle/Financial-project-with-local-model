#!/usr/bin/env python3
"""
Send keyboard events from ASCII codes or strings using pynput.

Examples:
  python keyboard-clicks.py --ascii 72 101 108 108 111  # types Hello
  python keyboard-clicks.py --string "Hello, world!" --delay 0.05

Note: install dependency with `pip install pynput`.
"""
from __future__ import annotations

import argparse
import time
from typing import List

try:
    from pynput.keyboard import Controller, Key
except Exception as e:  # pragma: no cover
    raise SystemExit("pynput is required: pip install pynput") from e


SPECIAL_KEY_MAP = {
    13: Key.enter,
    9: Key.tab,
    8: Key.backspace,
    27: Key.esc,
    32: ' ',
}


# Extended name -> Key mapping (includes synonyms)
NAME_MAP = {
    'alt': 'alt',
    'alt_l': 'alt_l',
    'alt_r': 'alt_r',
    'backspace': 'backspace',
    'caps_lock': 'caps_lock',
    'cmd': 'cmd',
    'command': 'cmd',
    'ctrl': 'ctrl',
    'control': 'ctrl',
    'ctrl_l': 'ctrl_l',
    'ctrl_r': 'ctrl_r',
    'delete': 'delete',
    'down': 'down',
    'up': 'up',
    'left': 'left',
    'right': 'right',
    'end': 'end',
    'home': 'home',
    'enter': 'enter',
    'esc': 'esc',
    'page_down': 'page_down',
    'pageup': 'page_up',
    'page_up': 'page_up',
    'page': 'page_up',
    'shift': 'shift',
    'shift_l': 'shift_l',
    'shift_r': 'shift_r',
    'space': 'space',
    'tab': 'tab',
}


def _key_attr(name: str):
    """Resolve a `pynput.keyboard.Key` attribute by name, or return None."""
    try:
        return getattr(Key, name)
    except Exception:
        return None


def key_name_to_keytoken(name: str):
    """Convert a token name (like 'ctrl', 'enter', 'f5', 'a') to either a Key or a single-character string.

    Returns Key instance or single-character string.
    """
    n = name.strip().lower()
    if not n:
        raise ValueError('empty key name')

    # strip optional prefixes
    if n.startswith('key.'):
        n = n[4:]

    # function keys f1..f20
    if n.startswith('f') and n[1:].isdigit():
        attr = 'f' + n[1:]
        k = _key_attr(attr)
        if k:
            return k

    # direct map from NAME_MAP
    if n in NAME_MAP:
        mapped = NAME_MAP[n]
        k = _key_attr(mapped)
        if k:
            return k
    # try direct Key attribute
    k = _key_attr(n)
    if k:
        return k

    # last resort: single character
    if len(n) == 1:
        return n

    # allow textual names like 'comma', 'period'
    textual = {
        'comma': ',',
        'period': '.',
        'slash': '/',
        'backslash': '\\',
        'minus': '-',
        'equals': '=',
    }
    if n in textual:
        return textual[n]

    raise ValueError(f'Unknown key name: {name}')


def is_modifier_token(tok) -> bool:
    """Return True for modifier Key tokens."""
    mods = {Key.ctrl, Key.ctrl_l, Key.ctrl_r, Key.shift, Key.shift_l, Key.shift_r, Key.alt, Key.alt_l, Key.alt_r, getattr(Key, 'cmd', None)}
    return tok in mods


def send_combo(combo: str, delay: float = 0.0) -> None:
    """Send a single combo like 'ctrl+alt+delete' or 'cmd+shift+a'."""
    kb = Controller()
    parts = [p.strip() for p in combo.split('+') if p.strip()]
    if not parts:
        return

    # map names to tokens (Key or char)
    tokens = [key_name_to_keytoken(p) for p in parts]

    # separate modifiers and action keys
    modifiers = [t for t in tokens if isinstance(t, Key) and is_modifier_token(t)]
    others = [t for t in tokens if t not in modifiers]

    # press modifiers
    for m in modifiers:
        kb.press(m)

    # for each non-modifier token, press/release or type
    for t in others:
        if isinstance(t, Key):
            kb.press(t)
            kb.release(t)
        else:
            kb.type(t)
        if delay:
            time.sleep(delay)

    # release modifiers in reverse order
    for m in reversed(modifiers):
        kb.release(m)



def ascii_codes_from_args(values: List[str]) -> List[int]:
    codes: List[int] = []
    for v in values:
        v = v.strip()
        if not v:
            continue
        # allow decimal numbers
        try:
            codes.append(int(v))
            continue
        except ValueError:
            pass
        # allow single-character input
        if len(v) == 1:
            codes.append(ord(v))
            continue
        raise ValueError(f"Invalid ascii/code value: {v}")
    return codes


def send_ascii_codes(codes: List[int], delay: float = 0.0) -> None:
    kb = Controller()
    for code in codes:
        if code in SPECIAL_KEY_MAP:
            key = SPECIAL_KEY_MAP[code]
            if isinstance(key, str):
                kb.type(key)
            else:
                kb.press(key)
                kb.release(key)
        else:
            try:
                ch = chr(code)
            except Exception:
                continue
            kb.type(ch)
        if delay:
            time.sleep(delay)


def send_string(s: str, delay: float = 0.0) -> None:
    kb = Controller()
    for ch in s:
        kb.type(ch)
        if delay:
            time.sleep(delay)


def main() -> None:
    ap = argparse.ArgumentParser(description="Send keyboard events from ASCII codes or string")
    ap.add_argument("--ascii", nargs="*", help="ASCII codes (decimal) or single chars to send", default=[])
    ap.add_argument("--string", help="Send a literal string instead of ascii codes")
    ap.add_argument("--combo", nargs="*", help="Send key combos, e.g. ctrl+alt+delete or cmd+shift+a", default=[])
    ap.add_argument("--delay", type=float, default=0.0, help="Delay between keystrokes in seconds")
    args = ap.parse_args()

    if not args.ascii and not args.string:
        ap.error("provide --ascii or --string")

    if args.ascii:
        codes = ascii_codes_from_args(args.ascii)
        print(f"Sending ASCII codes: {codes}")
        send_ascii_codes(codes, delay=args.delay)

    if args.string:
        print(f"Sending string: {args.string!r}")
        send_string(args.string, delay=args.delay)

    if args.combo:
        for c in args.combo:
            print(f"Sending combo: {c}")
            send_combo(c, delay=args.delay)


if __name__ == "__main__":
    main()
