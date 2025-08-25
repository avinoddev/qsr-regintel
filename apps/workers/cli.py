# apps/workers/cli.py
import argparse
from .pipeline import discover, fetch, parse, normalize, verify, publish

def run_demo(jurisdiction: str | None):
    j = jurisdiction or "CA"
    families = ["predictive_scheduling", "meal_periods", "youth_labor"]

    urls = discover.run(j)
    for u in urls:
        raw = fetch.run(u)             # <-- returns dict now
        text = parse.run(u, raw)
        for fam in families:
            rule = normalize.run(j, fam, text, raw)   # <-- include raw meta
            rule = verify.run(rule)
            publish.run(rule)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jurisdiction", dest="jurisdiction", default=None)
    parser.add_argument("command", nargs="?", default="run-demo")
    args = parser.parse_args()
    if args.command == "run-demo":
        run_demo(args.jurisdiction)
