<div align="center">

```
 ██████╗ ██████╗ ███╗   ███╗██████╗  ██████╗ ███████╗
██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔═══██╗██╔════╝
██║     ██║   ██║██╔████╔██║██████╔╝██║   ██║███████╗
██║     ██║   ██║██║╚██╔╝██║██╔══██╗██║   ██║╚════██║
╚██████╗╚██████╔╝██║ ╚═╝ ██║██████╔╝╚██████╔╝███████║
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝  ╚═════╝ ╚══════╝
         F I L T E R
```

**Combos Filter** · `v0.1` · Made by **RivanSoul**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Version](https://img.shields.io/badge/Version-0.1-cyan?style=flat-square)]()
[![License](https://img.shields.io/badge/License-Private-red?style=flat-square)]()
[![Telegram](https://img.shields.io/badge/Telegram-MeowLeak-2CA5E0?style=flat-square&logo=telegram)](https://t.me/meowleak)
[![Discord](https://img.shields.io/badge/Discord-MeowMal-5865F2?style=flat-square&logo=discord)](https://discord.gg/7RRv93nXCp)

*Drop. Run. Filter. Done.*

</div>

---

## Overview

**Combos Filter** is a Python CLI tool for cleaning, deduplicating, transforming, and extracting credential combo lists at scale.

**No setup. No config. No path prompts.**  
Drop your `.txt` combo files in the same folder as the script, run it, and follow the interactive menu.

---

## Workflow

```
1. Drop your .txt combo files into the script folder
2. Run:  python main.py
3. Select one or more files from the auto-detected list
4. Choose an operation
5. Output is saved to the same folder automatically
```

---

## Features

| # | Operation | Description |
|---|-----------|-------------|
| 1 | **Combo Optimiser** | Full pipeline: Capture Remover → Dedup → Remove Empty Lines |
| 2 | **Capture Remover** | Extracts valid `email:pass` from any dirty format |
| 3 | **Remove Duplicates** | Deduplicates lines, first occurrence wins |
| 4 | **Get Duplicates** | Returns lines that appeared more than once |
| 5 | **Randomize** | Shuffles lines using Fisher-Yates algorithm |
| 6 | **Remove Empty Lines** | Drops blank and whitespace-only lines |
| 7 | **Sort Lines** | Alphabetical / lexicographic sort |
| 8 | **Email:Pass → User:Pass** | `user@domain.com:pass` → `user:pass` |
| 9 | **Any Format → Email** | Extracts bare email addresses from any combo |

**What else it does:**

- 📂 **Auto-detects** all `.txt` files in its own directory — no path typing
- 🔢 **Numbered file list** — pick by number (`1`, `1,3`, or Enter for all)
- 🔀 **Multi-file merge** — selected files are merged before processing
- ⚡ **High-volume** — chunked streaming I/O, handles millions of lines
- 🧹 **Auto-normalises** `url:email:pass` → `email:pass`
- 💾 **Smart output names** — `input_combo_optimiser.txt` / `merged_sort_lines.txt`
- 📊 **Progress bars** — real-time read/write percentage
- 🔁 **Loop menu** — run multiple operations in one session

---

## Requirements

```
Python 3.10+
No external packages — stdlib only
```

---

## Usage

### Step 1 — Place your combo files

Put all `.txt` files in the **same folder** as `main.py`:

```
📁 ComboFilter/
├── main.py
├── dump1.txt
├── dump2.txt
└── accounts.txt
```

### Step 2 — Run the script

```bash
python main.py
```

### Step 3 — Select files

```
── Detected .txt files ──────────────────────────────

     [1]  dump1.txt        (12.40 MB)
     [2]  dump2.txt         (8.75 MB)
     [3]  accounts.txt      (2.10 MB)

  Enter numbers separated by commas — or press Enter to select ALL
  Example:  1        →  single file
            1,3,5    →  three files
            (Enter)  →  all files
```

### Step 4 — Choose an operation

```
── Select an operation ──────────────────────────────

    [1]  Combo Optimiser
    [2]  Capture Remover
    [3]  Remove Duplicates
    [4]  Get Duplicates
    [5]  Randomize
    [6]  Remove Empty Lines
    [7]  Sort Lines
    [8]  Email:Pass → User:Pass
    [9]  Any Format → Email
```

### Step 5 — Output

The processed file is saved automatically in the same folder:

```
  ──────────────────────────────────────────────────────────
  ✓  Done in 1.83s
  Files read   :           3
  Input lines  :   2,450,000
  Output lines :   1,980,341   (+net)
  Saved to     :  merged_combo_optimiser.txt
  ──────────────────────────────────────────────────────────
```

---

## Supported Combo Formats

| Format | Example |
|--------|---------|
| `email:pass` | `user@gmail.com:password123` |
| `url:email:pass` | `https://netflix.com:user@gmail.com:password123` |
| `url:login:pass` | `https://netflix.com:mylogin:password123` |
| Mixed / dirty lines | Automatically normalised or skipped |

---

## Output Naming

| Scenario | Output filename |
|----------|----------------|
| 1 file selected | `{original_name}_{operation}.txt` |
| 2+ files selected | `merged_{operation}.txt` |

**Examples:**
```
dump1_combo_optimiser.txt
merged_remove_duplicates.txt
accounts_any_format_to_email.txt
```

---

## Examples

### Clean a large dirty dump

**Input (`dump1.txt`):**
```
https://netflix.com:john@gmail.com:hunter2
user@yahoo.com:qwerty123
user@yahoo.com:qwerty123
notavalidline
   
admin@hotmail.com:abc!DEF9
```

**Operation `1` — Combo Optimiser → Output:**
```
john@gmail.com:hunter2
user@yahoo.com:qwerty123
admin@hotmail.com:abc!DEF9
```

---

### Merge 3 files and remove all duplicates

**Select:** `1,2,3` → all files merged  
**Operation `3` — Remove Duplicates**  
**Result:** Single deduplicated output file  

---

### Convert all combos to User:Pass format

**Operation `8` — Email:Pass → User:Pass**

```
# Input
john@gmail.com:mypassword
admin@outlook.com:securepass99

# Output
john:mypassword
admin:securepass99
```

---

## File Structure

```
📁 Script folder/
├── main.py          ← Combos Filter (run this)
├── README.md        ← Documentation
├── your_combo.txt   ← Drop files here
└── output.txt       ← Results appear here
```

---

## Contact & Support

| Platform | Link |
|----------|------|
| 💬 **Telegram** | [@MeowLeak](https://t.me/meowleak) |
| 🎮 **Discord** | [discord.gg/qAZwJK2TJU](https://discord.gg/qAZwJK2TJU) |

---

<div align="center">

**Combos Filter v0.1** — Made by **RivanSoul**  
*Drop. Run. Filter. Done.*

</div>
