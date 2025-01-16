#!/usr/bin/env python3

import argparse
import json
import os
from typing import List, Dict
from pathlib import Path


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description='Merge multiple Postman collections into one'
    )
    parser.add_argument(
        '-i', '--input',
        nargs='+',
        required=False,
        help='Input files or directory containing Postman collections'
    )
    parser.add_argument(
        '-f', '--file',
        help='File containing collection paths (one per line)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file name (optional)'
    )
    return parser.parse_args()


def load_collection(file_path: str) -> Dict:
    """
    Load a Postman collection from a JSON file.
    
    Args:
        file_path (str): Path to the collection file
        
    Returns:
        dict: Loaded collection data
        
    Raises:
        json.JSONDecodeError: If file is not valid JSON
        FileNotFoundError: If file doesn't exist
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_collection_files(input_paths: List[str]) -> List[str]:
    """
    Get all collection files from input paths.
    
    Args:
        input_paths (List[str]): List of file paths or directories
        
    Returns:
        List[str]: List of collection file paths
    """
    if not input_paths:
        return []
    collection_files = []
    for path in input_paths:
        if os.path.isdir(path):
            # If path is directory, get all .json files
            collection_files.extend([
                os.path.join(path, f) for f in os.listdir(path)
                if f.endswith('.json')
            ])
        else:
            collection_files.append(path)
    return collection_files


def merge_collections(collections: List[Dict]) -> Dict:
    """
    Merge multiple Postman collections into one.
    
    Args:
        collections (List[Dict]): List of collection data
        
    Returns:
        Dict: Merged collection
    """
    if not collections:
        raise ValueError("No collections to merge")

    # Use the first collection as base
    merged = collections[0].copy()
    
    # Generate merged name from all collection names
    collection_names = set()
    for collection in collections:
        collection_names.add(collection['info']['name'])
    
    merged['info']['name'] = ' + '.join(sorted(collection_names))
    
    # Merge items (requests and folders)
    for collection in collections[1:]:
        if 'item' in collection:
            merged['item'].extend(collection['item'])

    return merged


def main():
    """Main function to execute the collection merger."""
    args = parse_arguments()
    
    try:
        input_paths = []
        if args.input:
            input_paths.extend(args.input)
        
        # Add paths from file if specified
        if args.file:
            with open(args.file, 'r') as f:
                file_paths = [line.strip() for line in f if line.strip()]
                input_paths.extend(file_paths)
        
        if not input_paths:
            raise ValueError("No input provided. Use either -i/--input or -f/--file")
            
        # Get all collection files
        collection_files = get_collection_files(input_paths)
        
        if not collection_files:
            raise ValueError("No JSON files found in the specified input paths")
        
        # Load all collections
        collections = [load_collection(f) for f in collection_files]
        
        # Merge collections
        merged_collection = merge_collections(collections)
        
        # Generate output filename if not provided
        if not args.output:
            output_name = merged_collection['info']['name'].replace(' + ', '_')
            output_path = f"{output_name}_merged.json"
        else:
            output_path = args.output
        
        # Write merged collection to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(merged_collection, f, indent=2)
        
        print(f"Successfully merged collections into: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
