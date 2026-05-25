import argparse
from pathlib import Path

from .config import load_config
from .sampler import generate_lhs
from .formatters import save_experiments


def main():
    parser = argparse.ArgumentParser(
        prog="doe",
        description="Easy design of experiments for ML.",
    )
    parser.add_argument("config", type=str, help="YAML config file")
    parser.add_argument(
        "-o", "--output", type=str, default=None,
        help="Output file (csv/yaml/json)"
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print configs without saving"
    )
    args = parser.parse_args()

    # 1. Load and validate config
    cfg = load_config(args.config)

    # CLI seed takes precedence
    if args.seed is not None:
        cfg["seed"] = args.seed

    # 2. Generate experiments
    experiments = generate_lhs(cfg)

    # 3. Output
    if args.dry_run:
        print(f"\nGenerated {len(experiments)} experiments (dry run):")
        for i, exp in enumerate(experiments[:5], 1):
            print(f"  #{i}: {exp}")
        if len(experiments) > 5:
            print(f"  ... and {len(experiments) - 5} more")
        return

    out_path = args.output or cfg.get("output", "experiments.csv")
    save_experiments(experiments, out_path)
    print(f"\nSaved {len(experiments)} experiments -> {out_path}")

    # Preview
    print("\nPreview (first 3):")
    for i, exp in enumerate(experiments[:3], 1):
        print(f"  #{i}: {exp}")


if __name__ == "__main__":
    main()
