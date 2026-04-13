"""
╔══════════════════════════════════════════════════════════════╗
║              Combos Filter  —  v0.1                          ║
║              Made by RivanSoul                               ║
╠══════════════════════════════════════════════════════════════╣
║  Drop .txt files in this folder → python main.py → done      ║
╚══════════════════════════════════════════════════════════════╝

Contact
  Telegram : https://t.me/meowleak
  Discord  : https://discord.gg/qAZwJK2TJU
"""

__version__ = "0.1"
__author__  = "RivanSoul"
__project__ = "Combos Filter"

import re
import os
import sys
import random
import time
from pathlib import Path


if sys.platform == "win32":
    os.system("")          

R  = "\033[91m"   
G  = "\033[92m"   
Y  = "\033[93m"   
C  = "\033[96m"   
B  = "\033[94m"   
BD = "\033[1m"    
DM = "\033[2m"    
RS = "\033[0m"    


_EP_RE    = re.compile(r'[0-9a-zA-Z_.+\-]+@[0-9a-zA-Z_.+\-]+:[^\s]+')
_EMAIL_RE = re.compile(r'[0-9a-zA-Z_.+\-]+@[0-9a-zA-Z_.+\-]+\.[a-zA-Z]{2,}')
_BLANK_RE = re.compile(r'^\s*$')

CHUNK = 16 * 1024 * 1024  


def capture_remover(lines):
    """Extract valid email:pass — normalises url:email:pass automatically."""
    out = []
    for ln in lines:
        ln = ln.rstrip('\r\n')
        m = _EP_RE.search(ln)
        if m:
            out.append(m.group(0))
    return out

def remove_duplicates(lines):
    """Deduplicate; first occurrence wins."""
    seen, out = set(), []
    for ln in lines:
        ln = ln.rstrip('\r\n')
        if ln not in seen:
            seen.add(ln)
            out.append(ln)
    return out

def get_duplicates(lines):
    """Return unique set of lines that appeared more than once."""
    count = {}
    for ln in lines:
        ln = ln.rstrip('\r\n')
        count[ln] = count.get(ln, 0) + 1
    seen, out = set(), []
    for ln in lines:
        ln = ln.rstrip('\r\n')
        if count[ln] > 1 and ln not in seen:
            seen.add(ln)
            out.append(ln)
    return out

def combo_optimiser(lines):
    """Capture Remover → Remove Duplicates → Remove Empty Lines."""
    return remove_empty_lines(remove_duplicates(capture_remover(lines)))

def randomize(lines):
    """Fisher-Yates shuffle."""
    lines = [ln.rstrip('\r\n') for ln in lines]
    random.shuffle(lines)
    return lines

def remove_empty_lines(lines):
    """Drop blank / whitespace-only lines."""
    return [ln.rstrip('\r\n') for ln in lines if not _BLANK_RE.match(ln.rstrip('\r\n'))]

def sort_lines(lines):
    """Alphabetical sort."""
    return sorted(ln.rstrip('\r\n') for ln in lines)

def email_to_user(lines):
    """user@domain.com:pass  →  user:pass"""
    out = []
    for ln in lines:
        ln = ln.rstrip('\r\n')
        result = re.sub(
            r'([0-9a-zA-Z_.+\-]+)@[0-9a-zA-Z_.+\-]+:([^\s]+)',
            r'\1:\2', ln
        )
        if result.strip():
            out.append(result)
    return out

def any_to_email(lines):
    """Extract bare email addresses from any combo format."""
    out = []
    for ln in lines:
        out.extend(_EMAIL_RE.findall(ln.rstrip('\r\n')))
    return out


OPERATIONS = [
    ("Combo Optimiser",        combo_optimiser),
    ("Capture Remover",        capture_remover),
    ("Remove Duplicates",      remove_duplicates),
    ("Get Duplicates",         get_duplicates),
    ("Randomize",              randomize),
    ("Remove Empty Lines",     remove_empty_lines),
    ("Sort Lines",             sort_lines),
    ("Email:Pass → User:Pass", email_to_user),
    ("Any Format → Email",     any_to_email),
]



def _progress(label, pct, width=30):
    filled = int(width * pct / 100)
    bar = "█" * filled + "░" * (width - filled)
    sys.stdout.write(f"\r  {C}{label}{RS} [{G}{bar}{RS}] {Y}{pct:3d}%{RS}   ")
    sys.stdout.flush()

def _read_file(path):
    """Chunked read → list[str]. Shows progress."""
    lines, total, done = [], os.path.getsize(path), 0
    name = Path(path).name
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        while True:
            raw = f.read(CHUNK)
            if not raw:
                break

            batch = raw.splitlines(keepends=True)
            lines.extend(batch)
            done += len(raw.encode('utf-8', errors='replace'))
            _progress(f"  {name}", min(100, int(done / max(total, 1) * 100)))
    print()
    return lines

def _write_file(path, lines):
    """Write list[str] → file with progress."""
    total = len(lines)
    with open(path, 'w', encoding='utf-8') as f:
        for i, ln in enumerate(lines, 1):
            f.write(ln + '\n')
            if i % 50_000 == 0 or i == total:
                _progress("  Writing", int(i / max(total, 1) * 100))
    print()

def _scan_txts():
    """Return sorted list of .txt files in the script's directory."""
    here = Path(__file__).parent
    return sorted(p for p in here.glob("*.txt") if p.name != "output.txt")



def _banner():
    print(f"""
{BD}{C}╔══════════════════════════════════════════════════════════════╗
║         Combos Filter  v{__version__}  —  Made by {__author__}           ║
║  Auto-detect · Multi-select · Merge · Filter · Export        ║
╚══════════════════════════════════════════════════════════════╝{RS}
  {DM}Telegram: t.me/meowleak   |   Discord: discord.gg/qAZwJK2TJU{RS}
""")

def _hr(char="─", n=58):
    return char * n

def _pick_files(txt_files):
    """Show numbered list of .txt files; return selected paths."""
    print(f"  {BD}{Y}── Detected .txt files ──────────────────────────────{RS}\n")

    if not txt_files:
        print(f"  {R}No .txt files found in this folder.{RS}")
        print(f"  {DM}Place your combo files here and re-run the script.{RS}\n")
        return []

    for i, p in enumerate(txt_files, 1):
        mb = p.stat().st_size / 1_048_576
        print(f"    {C}[{i:>2}]{RS}  {p.name}  {DM}({mb:.2f} MB){RS}")

    print(f"\n  {DM}Enter numbers separated by commas — or press Enter to select ALL{RS}")
    print(f"  {DM}Example:  1        →  single file{RS}")
    print(f"  {DM}          1,3,5    →  three files{RS}")
    print(f"  {DM}          (Enter)  →  all files{RS}\n")

    while True:
        raw = input(f"  {BD}>{RS} ").strip()
        if not raw:
            return list(txt_files)

        chosen = []
        valid  = True
        for token in raw.split(','):
            token = token.strip()
            if not token.isdigit():
                print(f"  {R}Invalid input '{token}' — use numbers only.{RS}")
                valid = False
                break
            n = int(token)
            if n < 1 or n > len(txt_files):
                print(f"  {R}Number {n} is out of range (1–{len(txt_files)}).{RS}")
                valid = False
                break
            p = txt_files[n - 1]
            if p not in chosen:
                chosen.append(p)

        if valid and chosen:
            return chosen

def _pick_operation():
    """Show numbered operation menu; return chosen (name, fn)."""
    print(f"\n  {BD}{Y}── Select an operation ──────────────────────────────{RS}\n")
    for i, (name, _) in enumerate(OPERATIONS, 1):
        print(f"    {C}[{i}]{RS}  {name}")
    print()

    while True:
        raw = input(f"  {BD}>{RS} ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(OPERATIONS):
            return OPERATIONS[int(raw) - 1]
        print(f"  {R}Enter a number between 1 and {len(OPERATIONS)}.{RS}")

def _confirm_files(chosen):
    print(f"\n  {G}Selected {len(chosen)} file(s):{RS}")
    for p in chosen:
        print(f"    {DM}• {p.name}{RS}")
    print()



def main():
    _banner()

    while True:
        txt_files = _scan_txts()
        chosen = _pick_files(txt_files)
        if not chosen:
            input(f"  {DM}Press Enter to retry…{RS}")
            print()
            continue

        _confirm_files(chosen)


        op_name, op_fn = _pick_operation()
        print(f"\n  {BD}{G}Operation:{RS} {op_name}\n")


        t0 = time.perf_counter()
        all_lines = []
        file_counts = {}

        print(f"  {BD}Reading…{RS}")
        for p in chosen:
            batch = _read_file(str(p))
            file_counts[p.name] = len(batch)
            all_lines.extend(batch)

        in_count = len(all_lines)

        if len(chosen) > 1:
            print(f"  {DM}Per-file breakdown:{RS}")
            for name, cnt in file_counts.items():
                print(f"    {DM}• {name}: {cnt:,} lines{RS}")

        print(f"  {DM}Total: {in_count:,} lines{RS}\n")


        print(f"  {C}Processing…{RS}")
        result    = op_fn(all_lines)
        out_count = len(result)


        here       = Path(__file__).parent
        slug       = (op_name.lower()
                      .replace(' ', '_')
                      .replace('→', 'to')
                      .replace(':', ''))
        base       = chosen[0].stem if len(chosen) == 1 else "merged"
        out_path   = here / f"{base}_{slug}.txt"

        print(f"  {BD}Writing…{RS}")
        _write_file(str(out_path), result)


        elapsed = time.perf_counter() - t0
        net     = out_count - in_count
        net_str = f"+{net:,}" if net >= 0 else f"{net:,}"

        print(f"""
  {BD}{_hr()}{RS}
  {G}✓  Done in {elapsed:.2f}s{RS}
  {BD}Files read   :{RS}  {len(chosen):>10,}
  {BD}Input lines  :{RS}  {in_count:>10,}
  {BD}Output lines :{RS}  {out_count:>10,}   {G}({net_str} net){RS}
  {BD}Saved to     :{RS}  {out_path.name}
  {BD}{_hr()}{RS}
""")


        again = input(f"  {BD}Run another operation? [y/N]:{RS} ").strip().lower()
        print()
        if again != 'y':
            print(f"  {Y}Goodbye! — {__project__} v{__version__} by {__author__}{RS}\n")
            break


if __name__ == '__main__':
    main()
