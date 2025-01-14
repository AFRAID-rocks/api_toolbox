#!/usr/bin/env python3

"""
Postman Collection Validator Script.

This script validates whether files are valid Postman collections.
It can process multiple files or entire directories.
"""

import argparse
import json
from pathlib import Path

def is_valid_postman_collection(file_path: str) -> bool:
    """Check if a file is a valid Postman collection."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            collection = json.load(file)
        return (isinstance(collection, dict) 
                and 'info' in collection 
                and 'item' in collection 
                and isinstance(collection['info'], dict))
    except:
        return False

def find_json_files(input_path: str, max_depth: int = 5) -> list[str]:
    """Find all JSON files in the given path."""
    path = Path(input_path)
    if path.is_file():
        return [str(path)]
    return [str(p) for p in path.rglob('*.json') 
            if len(p.relative_to(path).parts) <= max_depth]

def main():
    parser = argparse.ArgumentParser(description='Validate Postman collection files')
    parser.add_argument('-i', '--input', nargs='+', required=True)
    parser.add_argument('-o', '--output')
    parser.add_argument('-d', '--discover', action='store_true')
    parser.add_argument('--depth', type=int, default=5)
    args = parser.parse_args()

    # Find all JSON files
    files = []
    for path in args.input:
        files.extend(find_json_files(path, args.depth))

    if not files:
        print("No files found to check!")
        return

    # Check files and prepare output
    results = []
    for file in files:
        is_valid = is_valid_postman_collection(file)
        status = "Valid" if is_valid else "Invalid"
        message = f"{file}: {status}"
        print(message)
        if is_valid:
            results.append(file)


    # Write results if output file specified
    if args.output and results:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write('\n'.join(results))
            print(f"\nResults written to {args.output}")
        except Exception as e:
            print(f"Error writing to output file: {str(e)}")

if __name__ == "__main__":
    main()
