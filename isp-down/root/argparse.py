import argparse

def parse_args():
    args = argparse.ArgumentParser()

    args.add_argument("--dry-run",action="store_true")

    return args.parse_args()
