#!/usr/bin/env python3
"""
Simple test runner for the Quant API.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py btc          # Run BTC API tests only
    python run_tests.py analysis     # Run analysis tests only
    python run_tests.py integration  # Run integration tests only
    python run_tests.py unit         # Run unit tests only
"""

import sys
import subprocess
from pathlib import Path


def run_tests(test_type: str = "all") -> int:
    """Run tests based on specified type"""
    
    test_commands = {
        "all": ["pytest", "tests/", "-v"],
        "btc": ["pytest", "tests/test_btc_api.py", "-v"],
        "analysis": ["pytest", "tests/test_analysis_api.py", "-v"],
        "volume": ["pytest", "tests/test_volume_analyzer.py", "-v"],
        "integration": ["pytest", "tests/test_integration.py", "-v"],
        "unit": ["pytest", "tests/test_btc_api.py", "tests/test_analysis_api.py", "tests/test_volume_analyzer.py", "-v"]
    }
    
    if test_type not in test_commands:
        print(f"Invalid test type: {test_type}")
        print(f"Available options: {', '.join(test_commands.keys())}")
        return 1
    
    print(f"Running {test_type} tests...")
    
    try:
        result = subprocess.run(test_commands[test_type], check=False)
        return result.returncode
    except FileNotFoundError:
        print("Error: pytest not found. Please install test dependencies:")
        print("pip install -r requirements.txt")
        return 1


def main():
    """Main test runner function"""
    test_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    exit_code = run_tests(test_type)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
