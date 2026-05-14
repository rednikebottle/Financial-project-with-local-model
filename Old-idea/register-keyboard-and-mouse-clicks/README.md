# Keyboard Clicks

This small script sends keyboard events from ASCII codes or literal strings using `pynput`.

Usage

Install dependency:

```bash
pip install pynput
```

Examples:

```bash
# send ascii codes (72 101 108 108 111 == "Hello")
python keyboard-clicks.py --ascii 72 101 108 108 111

# send a string with a small delay between keys
python keyboard-clicks.py --string "Hello, world!" --delay 0.05
```

Combos and special keys

You can send combos using `--combo` with `+` between keys. Examples:

```bash
# send Ctrl+Alt+Delete
python keyboard-clicks.py --combo "ctrl+alt+delete"

# send Command+Shift+A (Mac)
python keyboard-clicks.py --combo "cmd+shift+a"

# send multiple combos in sequence
python keyboard-clicks.py --combo "ctrl+c" "ctrl+v"
```

Supported keys: `alt`, `alt_l`, `alt_r`, `backspace`, `caps_lock`, `cmd` (Mac/Windows Win key), `ctrl`, `ctrl_l`, `ctrl_r`, `delete`, `down`, `up`, `left`, `right`, `end`, `home`, `enter`, `esc`, `f1..f20`, `page_up`, `page_down`, `shift`, `shift_l`, `shift_r`, `space`, `tab`, and single characters like `a`, `1`, `,`, `.`.

Notes:
- On macOS grant Accessibility permission to Terminal/Python to allow synthetic input.
- Behavior of some keys (like `cmd`/Windows key) can vary by platform.

Notes

- On macOS you may need to grant the terminal/app Accessibility permissions to allow synthetic input.
- For special keys use their ASCII values (e.g. Enter = 13, Tab = 9).
