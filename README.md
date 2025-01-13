# Postman Collection Tools

A set of Python utilities for working with Postman collections.

## Features

- **Collection Checker**: Validates Postman collection files
- **Collection Merger**: Combines multiple Postman collections into a single collection

## Installation

1. Clone this repository
2. Ensure Python 3.6+ is installed
3. No additional dependencies required - uses Python standard library only

## Usage

### Collection Checker

Validates whether files are valid Postman collections.

```python
python collectionChecker.py -i <input_paths> [options]
```

#### Options

```
- `-i, --input`: Input files or directories to check (required, accepts multiple)
- `-o, --output`: Output file to write results
- `-d, --discover`: Enable discovery mode to only list valid collections
- `--depth`: Maximum directory depth for recursive search (default: 5)
```

#### Examples

```bash
python collectionChecker.py -i ./collections -o ./results.txt --discover --depth 3
```

# Check a single file

```bash
python collectionChecker.py -i ./collections/collection.json
```

# Check multiple files and directories

```bash
python collectionChecker.py -i ./collections ./collections2
```

# Save results to file

```bash
python collectionChecker.py -i ./collections -o ./results.txt
```
