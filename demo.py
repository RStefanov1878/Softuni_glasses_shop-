"""One-command demo: print the committed catalogue as a readable table.

Runs end-to-end against the sample dataset using the Module A data layer, with
no web server needed.

    python demo.py
"""

from pathlib import Path

import catalogue

BASE_DIR = Path(__file__).resolve().parent


def main():
    glasses = catalogue.load_glasses(BASE_DIR / "data" / "glasses.json")
    cats = catalogue.categories(glasses)

    print(
        f"Glasses Catalogue - {len(glasses)} items "
        f"across {len(cats)} categories: {', '.join(cats)}\n"
    )
    header = f"{'ID':>2}  {'NAME':<18} {'CATEGORY':<11} {'PRICE':>8}  COLOUR"
    print(header)
    print("-" * len(header))
    for g in glasses:
        price = "$" + format(g["price"], ".2f")
        print(
            f"{g['id']:>2}  {g['name']:<18} {g['category']:<11} {price:>8}  {g['color']}"
        )


if __name__ == "__main__":
    main()
