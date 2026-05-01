# ![Renzo](renzo.png)

# Renzo

> A terminal-based HTML editor that makes building websites fast, visual, and keyboard-driven.

Renzo is a CLI tool that lets you edit HTML files directly in your terminal. It gives you a live tree view of your document structure, an inline property inspector, and a real-time browser preview — all without ever touching a text editor.

---

## Features

- **tag tree view** — See your entire HTML structure as a collapsible tree
- **Inline property editor** — Edit tag attributes directly from the terminal
- **Tag search** — Browse and insert HTML tags by name with descriptions
- **Live browser preview** — Your page hot-reloads in the browser as you edit (served at `http://127.0.0.1:5090`)
- **Clipboard save** — Copy the generated HTML to your clipboard instantly with `Ctrl+S`

---

## Requirements

- Python 3.8+
- pip packages:

```bash
pip install blessed flask pyperclip 
```
- NOTE : not all of these packages work with the pipx command so please use pip install blessed flask pyperclip --break-system-packages if you are on linux
- package will be auto installed if you run them through pip

---

## Running Renzo

```bash
pip install renzo
renzo 
```

The browser preview will be available at `http://127.0.0.1:5090` immediately on launch.


---

## Keybindings

### tag Tree (left panel)

| Key | Action |
|-----|--------|
| `j` / `↑` | Move selection up |
| `k` / `↓` | Move selection down |
| `Enter` | Edit selected text tag / open property inspector |
| `Esc` | Confirm edit and return |
| `n` | Open tag search to insert a new tag |
| `i` | Insert a new text (inner) tag below selection |
| `x` | Delete selected tag/property |
| `Ctrl+↓` | Move tag down |
| `Ctrl+↑` | Move tag up |
| `Ctrl+→` | Increase tag indent |
| `Ctrl+←` | Decrease tag indent |
| `Ctrl+Shift+↓` | Move tag group down |
| `Ctrl+Shift+↑` | Move tag group up |
| `Ctrl+S` | Save (copies HTML to clipboard) |

### Property Inspector (right panel)

| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate between properties |
| `Enter` | Edit selected property value (or toggle boolean) |
| `Esc` | Confirm edit / return to tag tree |
| `n` | Add a new property |
| `x` | Delete selected property |

### Tag Search panel

| Key | Action |
|-----|--------|
| Any character | Type to filter tags |
| `↑` / `↓` | Navigate results |
| `Enter` | Insert selected tag as a child of current tag |
| `Esc` | Close and return to tag tree |

---

## Workflow Example

Here is a typical flow for adding a styled button to your page:

1. Navigate to the `body` tag in the tree
2. Press `n` to open tag search, type `button`, press `Enter` to insert it
3. Press `Enter` on the new `button` tag to open the property inspector
4. Press `n` to add a `class` property, type `btn`, press `Enter`
5. Press `Esc` to return to the tree
6. Press `i` to insert inner text, type `Click me`, press `Enter`
7. Check your browser at `http://127.0.0.1:5090` to see the result
8. Press `Ctrl+S` to copy the finished HTML to your clipboard

---

## Known Limitations

- Very large documents may cause rendering slowness in the terminal due to full-screen redraws on every frame.
- Ctrl+Shift+Up/Down (group move) has some edge-case bugs with deeply nested structures.

---

## License

MIT