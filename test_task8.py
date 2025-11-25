import sys
import os
import subprocess
import json

# Helper to extract a sample document UUID
def get_sample_document_uuid():
    try:
        with open('data/issuu_sample.json', 'r') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    doc_uuid = data.get('env_doc_id') or data.get('subject_doc_id')
                    if doc_uuid:
                        return doc_uuid
    except Exception as e:
        print(f"Error reading sample data: {e}")
    return None

# Test all CLI commands for Task 8
def test_cli_commands():
    if not os.path.exists('data/issuu_sample.json'):
        print("X Sample data not found. Please download issuu_sample.json to data/ folder")
        return False

    print("\nTesting Task 8 Command Line Interface")
    print("=" * 60)

    # Get sample document UUID
    sample_doc = get_sample_document_uuid()
    if not sample_doc:
        print("X Could not find a sample document UUID")
        return False

    print(f"Using sample document: {sample_doc[:16]}...")

    test_cases = [
        # Task 2a: Country histogram
        {
            'name': 'Task 2a - Country Views',
            'cmd': [sys.executable, 'main.py', '-t', '2a', '-d', sample_doc, '-f', 'data/issuu_sample.json'],
            'expect_success': True
        },
        # Task 2b: Continent histogram
        {
            'name': 'Task 2b - Continent Views',
            'cmd': [sys.executable, 'main.py', '-t', '2b', '-d', sample_doc, '-f', 'data/issuu_sample.json'],
            'expect_success': True
        },
        # Task 3a: Raw browsers
        {
            'name': 'Task 3a - Raw Browsers',
            'cmd': [sys.executable, 'main.py', '-t', '3a', '-f', 'data/issuu_sample.json'],
            'expect_success': True
        },
        # Task 3b: Simplified browsers
        {
            'name': 'Task 3b - Simplified Browsers',
            'cmd': [sys.executable, 'main.py', '-t', '3b', '-f', 'data/issuu_sample.json'],
            'expect_success': True
        },
        # Task 4: Top readers
        {
            'name': 'Task 4 - Top Readers',
            'cmd': [sys.executable, 'main.py', '-t', '4', '-f', 'data/issuu_sample.json'],
            'expect_success': True
        },
        # Task 5d: Also likes
        {
            'name': 'Task 5d - Also Likes',
            'cmd': [sys.executable, 'main.py', '-t', '5d', '-d', sample_doc, '-f', 'data/issuu_sample.json'],
            'expect_success': True
        },
        # Task 6: Graph generation
        {
            'name': 'Task 6 - Graph Generation',
            'cmd': [sys.executable, 'main.py', '-t', '6', '-d', sample_doc, '-f', 'data/issuu_sample.json'],
            'expect_success': True
        }
    ]

    passed = 0
    total = len(test_cases)

    for test in test_cases:
        print(f"\nTesting: {test['name']}")
        print(f"  Command: {' '.join(test['cmd'])}")
        try:
            result = subprocess.run(test['cmd'], capture_output=True, text=True, timeout=30)
            if test['expect_success'] and result.returncode == 0:
                print(f"  PASS (exit code {result.returncode})")
                passed += 1
            elif not test['expect_success'] and result.returncode != 0:
                print(f"  PASS (expected failure, exit code {result.returncode})")
                passed += 1
            else:
                print(f"  X FAIL (exit code {result.returncode})")
                if result.stderr:
                    print(f"  Error output: {result.stderr[:200]}...")
        except subprocess.TimeoutExpired:
            print(f"  TIMEOUT command took too long")
        except Exception as e:
            print(f"  X ERROR - {e}")

    print(f"\nResults: {passed}/{total} tests passed")
    return passed == total


# Test that CLI shows help message
def test_cli_help():
    print("\nTesting CLI help...")
    try:
        result = subprocess.run([sys.executable, 'main.py', '-h'], capture_output=True, text=True)
        if result.returncode == 0 and 'usage:' in result.stdout.lower():
            print("  Help command works")
            return True
        else:
            print("  X Help command failed")
            return False
    except Exception as e:
        print(f"  X Help command error: {e}")
        return False

# Test invalid commands
def test_invalid_commands():
    print("\nTesting error handling...")

    error_cases = [
        {
            'name': 'Missing required file',
            'cmd': [sys.executable, 'main.py', '-t', '2a', '-d', 'test'],
            'expect_error': True
        },
        {
            'name': 'Invalid task ID',
            'cmd': [sys.executable, 'main.py', '-t', 'invalid', '-f', 'data/issuu_sample.json'],
            'expect_error': True
        },
        {
            'name': 'Missing document UUID for task 2a',
            'cmd': [sys.executable, 'main.py', '-t', '2a', '-f', 'data/issuu_sample.json'],
            'expect_error': True
        }
    ]

    passed = 0
    for test in error_cases:
        print(f"  Testing: {test['name']}")
        try:
            result = subprocess.run(test['cmd'], capture_output=True, text=True)
            if test['expect_error'] and result.returncode != 0:
                print(f"    Correctly produced error (exit code {result.returncode})")
                passed += 1
            else:
                print(f"    X Should have failed but didn't (exit code {result.returncode})")
        except Exception as e:
            print(f"    X Unexpected error: {e}")

    return passed == len(error_cases)

# Main execution
if __name__ == "__main__":
    print("Task 8 Command Line Interface Tests")
    print("=" * 50)

    help_ok = test_cli_help()
    errors_ok = test_invalid_commands()
    main_ok = test_cli_commands()

    print("\n" + "=" * 50)
    print("FINAL RESULTS:")
    print(f"Help command: {'PASS' if help_ok else 'FAIL'}")
    print(f"Error handling: {'PASS' if errors_ok else 'FAIL'}")
    print(f"Main functionality: {'PASS' if main_ok else 'FAIL'}")

    if help_ok and errors_ok and main_ok:
        print("\nTASK 8 COMPLETE CLI is working")
        sys.exit(0)
    else:
        print("\nX TASK 8 INCOMPLETE Some CLI tests failed")
        sys.exit(1)
