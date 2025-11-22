"""
File Operations Tool

Provides utilities for reading and writing portfolio data, reports, and trade orders.
Supports CSV, JSON, and formatted text output.
"""

import csv
import json
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from datetime import datetime
import os


def read_portfolio_csv(filepath: str) -> List[Dict[str, Any]]:
    """
    Read a portfolio CSV file and return as list of dictionaries.

    Expected CSV format:
    - Header row with column names
    - Common columns: ticker, shares, cost_basis, current_price, etc.

    Args:
        filepath: Path to CSV file

    Returns:
        List of dictionaries, one per row, with column names as keys

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If CSV is malformed or empty
        PermissionError: If file cannot be read

    Example:
        >>> portfolio = read_portfolio_csv('portfolio.csv')
        >>> for position in portfolio:
        >>>     print(f"{position['ticker']}: {position['shares']} shares")
    """
    # Validate filepath
    if not filepath:
        raise ValueError("Filepath cannot be empty")

    filepath = str(filepath).strip()
    file_path = Path(filepath)

    # Check file exists
    if not file_path.exists():
        raise FileNotFoundError(f"Portfolio file not found: {filepath}")

    # Check file is readable
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Cannot read file: {filepath}")

    # Check file extension
    if file_path.suffix.lower() != '.csv':
        raise ValueError(f"Expected CSV file, got: {file_path.suffix}")

    try:
        with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
            # Detect dialect and read
            sample = csvfile.read(1024)
            csvfile.seek(0)

            # Try to detect dialect
            try:
                dialect = csv.Sniffer().sniff(sample)
            except csv.Error:
                # Fall back to excel dialect
                dialect = csv.excel

            reader = csv.DictReader(csvfile, dialect=dialect)

            # Validate header exists
            if not reader.fieldnames:
                raise ValueError("CSV file has no header row")

            # Read all rows
            portfolio = []
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 for header)
                # Skip empty rows
                if not any(row.values()):
                    continue

                # Convert numeric fields if they look numeric
                processed_row = {}
                for key, value in row.items():
                    if value is None:
                        processed_row[key] = None
                        continue

                    value = value.strip()

                    # Try to convert to number
                    try:
                        # Try int first
                        if '.' not in value and 'e' not in value.lower():
                            processed_row[key] = int(value)
                        else:
                            processed_row[key] = float(value)
                    except (ValueError, AttributeError):
                        # Keep as string
                        processed_row[key] = value

                portfolio.append(processed_row)

            if not portfolio:
                raise ValueError("CSV file contains no data rows")

            return portfolio

    except csv.Error as e:
        raise ValueError(f"CSV parsing error at line {e.args[0] if e.args else 'unknown'}: {str(e)}") from e
    except UnicodeDecodeError as e:
        raise ValueError(f"File encoding error: {str(e)}. Expected UTF-8.") from e
    except Exception as e:
        raise RuntimeError(f"Failed to read portfolio CSV: {str(e)}") from e


def write_report(data: Union[str, Dict, List], filepath: str, format: str = 'auto') -> str:
    """
    Write a report file in various formats.

    Supports text, JSON, and formatted reports with automatic formatting.

    Args:
        data: Report data - can be string (written as-is), dict, or list
        filepath: Output file path
        format: Output format - 'auto', 'text', 'json', 'markdown'
                'auto' detects from file extension

    Returns:
        Absolute path to created file

    Raises:
        ValueError: If data or filepath is invalid
        PermissionError: If cannot write to filepath
        RuntimeError: If write operation fails

    Example:
        >>> report_data = {'ticker': 'AAPL', 'beta': 1.2, 'recommendation': 'BUY'}
        >>> write_report(report_data, 'report.json')
        >>> write_report("Analysis complete", 'report.txt')
    """
    # Validate inputs
    if data is None:
        raise ValueError("Data cannot be None")

    if not filepath:
        raise ValueError("Filepath cannot be empty")

    filepath = str(filepath).strip()
    file_path = Path(filepath)

    # Create parent directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Determine format
    if format == 'auto':
        ext = file_path.suffix.lower()
        if ext == '.json':
            format = 'json'
        elif ext == '.md':
            format = 'markdown'
        else:
            format = 'text'

    try:
        # Generate content based on format
        if format == 'json':
            # Write as JSON
            if isinstance(data, str):
                # If data is string, wrap it
                content = json.dumps({'content': data}, indent=2)
            else:
                content = json.dumps(data, indent=2, default=str)

        elif format == 'markdown':
            # Write as Markdown
            if isinstance(data, str):
                content = data
            else:
                content = _format_as_markdown(data)

        else:  # text
            # Write as plain text
            if isinstance(data, str):
                content = data
            elif isinstance(data, dict):
                content = _format_dict_as_text(data)
            elif isinstance(data, list):
                content = _format_list_as_text(data)
            else:
                content = str(data)

        # Add timestamp and header
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if format != 'json':
            header = f"Report Generated: {timestamp}\n{'=' * 70}\n\n"
            content = header + content

        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(file_path.absolute())

    except PermissionError as e:
        raise PermissionError(f"Cannot write to {filepath}: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to write report: {str(e)}") from e


def write_trade_order_json(order_data: Dict[str, Any], filepath: str) -> str:
    """
    Write a trade order to JSON file with validation.

    Validates required fields and creates a standardized trade order file.

    Args:
        order_data: Dictionary containing order details
                    Required fields: ticker, action, quantity
                    Optional: price, order_type, expiration, strategy, etc.
        filepath: Output JSON file path

    Returns:
        Absolute path to created file

    Raises:
        ValueError: If required fields are missing or invalid
        RuntimeError: If write operation fails

    Example:
        >>> order = {
        >>>     'ticker': 'AAPL',
        >>>     'action': 'BUY',
        >>>     'quantity': 100,
        >>>     'order_type': 'LIMIT',
        >>>     'price': 150.00
        >>> }
        >>> write_trade_order_json(order, 'orders/aapl_buy.json')
    """
    # Validate order_data
    if not isinstance(order_data, dict):
        raise ValueError(f"order_data must be a dictionary, got {type(order_data)}")

    # Required fields
    required_fields = ['ticker', 'action', 'quantity']
    missing_fields = [f for f in required_fields if f not in order_data]

    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    # Validate field values
    if not order_data['ticker'] or not isinstance(order_data['ticker'], str):
        raise ValueError("ticker must be a non-empty string")

    valid_actions = ['BUY', 'SELL', 'BUY_TO_OPEN', 'SELL_TO_CLOSE', 'BUY_TO_CLOSE', 'SELL_TO_OPEN']
    action = str(order_data['action']).upper()
    if action not in valid_actions:
        raise ValueError(f"action must be one of {valid_actions}, got '{action}'")

    try:
        quantity = float(order_data['quantity'])
        if quantity <= 0:
            raise ValueError("quantity must be positive")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid quantity: {order_data['quantity']}") from e

    # Create order with standardized fields
    order = {
        'ticker': str(order_data['ticker']).upper().strip(),
        'action': action,
        'quantity': quantity,
        'timestamp': datetime.now().isoformat(),
        'status': order_data.get('status', 'PENDING')
    }

    # Add optional fields
    optional_fields = [
        'price', 'order_type', 'expiration', 'strategy', 'notes',
        'stop_loss', 'take_profit', 'time_in_force', 'account'
    ]

    for field in optional_fields:
        if field in order_data:
            order[field] = order_data[field]

    # Add metadata
    order['metadata'] = {
        'created_at': datetime.now().isoformat(),
        'file_version': '1.0'
    }

    # Validate filepath
    if not filepath:
        raise ValueError("Filepath cannot be empty")

    filepath = str(filepath).strip()
    file_path = Path(filepath)

    # Ensure .json extension
    if file_path.suffix.lower() != '.json':
        file_path = file_path.with_suffix('.json')

    # Create parent directory if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Write JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(order, f, indent=2, default=str)

        return str(file_path.absolute())

    except PermissionError as e:
        raise PermissionError(f"Cannot write to {filepath}: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to write trade order: {str(e)}") from e


def _format_dict_as_text(data: Dict, indent: int = 0) -> str:
    """Format dictionary as readable text."""
    lines = []
    indent_str = "  " * indent

    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{indent_str}{key}:")
            lines.append(_format_dict_as_text(value, indent + 1))
        elif isinstance(value, list):
            lines.append(f"{indent_str}{key}:")
            lines.append(_format_list_as_text(value, indent + 1))
        else:
            lines.append(f"{indent_str}{key}: {value}")

    return "\n".join(lines)


def _format_list_as_text(data: List, indent: int = 0) -> str:
    """Format list as readable text."""
    lines = []
    indent_str = "  " * indent

    for i, item in enumerate(data):
        if isinstance(item, dict):
            lines.append(f"{indent_str}[{i}]:")
            lines.append(_format_dict_as_text(item, indent + 1))
        elif isinstance(item, list):
            lines.append(f"{indent_str}[{i}]:")
            lines.append(_format_list_as_text(item, indent + 1))
        else:
            lines.append(f"{indent_str}- {item}")

    return "\n".join(lines)


def _format_as_markdown(data: Union[Dict, List]) -> str:
    """Format data as Markdown."""
    if isinstance(data, dict):
        lines = ["# Report\n"]
        for key, value in data.items():
            lines.append(f"## {key}\n")
            if isinstance(value, (dict, list)):
                lines.append("```json")
                lines.append(json.dumps(value, indent=2, default=str))
                lines.append("```\n")
            else:
                lines.append(f"{value}\n")
        return "\n".join(lines)
    else:
        return f"```json\n{json.dumps(data, indent=2, default=str)}\n```"


if __name__ == "__main__":
    # Example usage and testing
    import tempfile
    import sys

    print("File Operations Tool Test")
    print("=" * 70)

    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Test 1: Write and read CSV
        print("\n1. Testing CSV Portfolio Operations:")
        print("-" * 70)

        csv_file = tmpdir / "test_portfolio.csv"

        # Create sample CSV
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['ticker', 'shares', 'cost_basis', 'current_price'])
            writer.writeheader()
            writer.writerow({'ticker': 'AAPL', 'shares': '100', 'cost_basis': '150.00', 'current_price': '175.50'})
            writer.writerow({'ticker': 'TSLA', 'shares': '50', 'cost_basis': '200.00', 'current_price': '245.75'})

        # Read it back
        portfolio = read_portfolio_csv(str(csv_file))
        print(f"Read {len(portfolio)} positions:")
        for pos in portfolio:
            print(f"  {pos['ticker']}: {pos['shares']} shares @ ${pos['current_price']}")

        # Test 2: Write report (text)
        print("\n2. Testing Text Report:")
        print("-" * 70)

        report_data = {
            'analysis': 'AAPL Analysis',
            'beta': 1.23,
            'recommendation': 'BUY',
            'target_price': 200.00
        }

        report_file = tmpdir / "report.txt"
        result = write_report(report_data, str(report_file), format='text')
        print(f"Report written to: {result}")

        with open(report_file, 'r') as f:
            print("Content preview:")
            print(f.read()[:200] + "...")

        # Test 3: Write report (JSON)
        print("\n3. Testing JSON Report:")
        print("-" * 70)

        json_file = tmpdir / "report.json"
        result = write_report(report_data, str(json_file), format='json')
        print(f"JSON report written to: {result}")

        with open(json_file, 'r') as f:
            loaded = json.load(f)
            print("Loaded data:")
            print(json.dumps(loaded, indent=2))

        # Test 4: Write trade order
        print("\n4. Testing Trade Order:")
        print("-" * 70)

        order = {
            'ticker': 'AAPL',
            'action': 'BUY',
            'quantity': 100,
            'order_type': 'LIMIT',
            'price': 175.00,
            'notes': 'Test order'
        }

        order_file = tmpdir / "orders" / "aapl_buy.json"
        result = write_trade_order_json(order, str(order_file))
        print(f"Order written to: {result}")

        with open(result, 'r') as f:
            saved_order = json.load(f)
            print("Order details:")
            print(json.dumps(saved_order, indent=2))

        print("\n" + "=" * 70)
        print("All tests completed successfully!")
