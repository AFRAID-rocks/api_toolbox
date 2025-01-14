#!/usr/bin/env python3

"""
Postman Collection Validator Script.

This script validates whether files are valid Postman collections.
It can process multiple files or entire directories.
"""

import argparse
import json
from typing import List, Tuple
from pathlib import Path


def is_valid_postman_collection(file_path: str) -> Tuple[bool, str]:
    """
    Check if a file is a valid Postman collection.

    Args:
        file_path (str): Path to the file to check

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            collection = json.load(file)

        # Check for required Postman collection fields
        if not isinstance(collection, dict):
            return False, "Not a JSON object"

        required_fields = ['info', 'item']
        missing_fields = [field for field in required_fields 
                         if field not in collection]

        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"

        # Check info section
        if not isinstance(collection['info'], dict):
            return False, "Info section is not an object"

        return True, "Looks like a valid Postman collection"

    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"


def process_input_path(input_path: str, max_depth: int = 5) -> List[str]:
    """
    Process input path and return list of files to check.

    Args:
        input_path (str): Input path (file or directory)
        max_depth (int): Maximum directory depth for recursive search

    Returns:
        List[str]: List of file paths to process
    """
    path = Path(input_path)
    if path.is_file():
        return [str(path)]
    elif path.is_dir():
        # Using rglob for recursive search of all .json files
        return [str(p) for p in path.rglob('*.json') 
                if len(p.relative_to(path).parts) <= max_depth]
    else:
        return []


def write_to_file(file_path: str, content: List[str]) -> None:
    """
    Write content to a file.

    Args:
        file_path (str): Path to output file
        content (List[str]): List of strings to write
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        print(f"\nResults written to {file_path}")
    except Exception as e:
        print(f"Error writing to output file: {str(e)}")


def process_normal_mode(files_to_check: List[str]) -> List[str]:
    """
    Process files in normal mode with detailed output.

    Args:
        files_to_check (List[str]): List of files to check

    Returns:
        List[str]: List of formatted results
    """
    results = []
    for file_path in files_to_check:
        is_valid, message = is_valid_postman_collection(file_path)
        status = "Valid" if is_valid else "Invalid"
        result = f"{file_path}: {status} - {message}"
        results.append(result)
        print(result)
    return results


def main():
    """Main function to run the collection checker."""
    parser = argparse.ArgumentParser(
        description='Validate Postman collection files'
    )
    parser.add_argument(
        '-i', '--input',
        nargs='+',
        required=True,
        help='Input files or directories to check'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file to write results'
    )
    parser.add_argument(
        '-d', '--discover',
        action='store_true',
        help='Enable discovery mode to only list valid Postman collections'
    )
    parser.add_argument(
        '--depth',
        type=int,
        default=5,
        help='Maximum directory depth for recursive search (default: 5)'
    )

    args = parser.parse_args()

    # Process all input paths
    files_to_check = []
    for input_path in args.input:
        files_to_check.extend(process_input_path(input_path, args.depth))

    if not files_to_check:
        print("No files found to check!")
        return

    # Check each file and collect valid collections
    valid_collections = []
    for file_path in files_to_check:
        is_valid, _ = is_valid_postman_collection(file_path)
        if is_valid:
            valid_collections.append(file_path)

    # Handle output based on mode
    if args.discover:
        # In discovery mode, only print valid collection paths
        for path in valid_collections:
            print(path)
        if args.output:
            write_to_file(args.output, valid_collections)
    else:
        # Normal mode with detailed output
        results = process_normal_mode(files_to_check)
        if args.output:
            write_to_file(args.output, results)


if __name__ == "__main__":
    main()
