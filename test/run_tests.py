#!/usr/bin/env python3
"""
Test runner script for Hacker News Analytics Dashboard.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"\n✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Command not found: {cmd[0]}")
        return False


def run_unit_tests():
    """Run unit tests."""
    return run_command([
        sys.executable, "-m", "pytest", 
        "tests/unit/", 
        "-v", 
        "--tb=short"
    ], "Unit Tests")


def run_integration_tests():
    """Run integration tests."""
    return run_command([
        sys.executable, "-m", "pytest", 
        "tests/integration/", 
        "-v", 
        "--tb=short"
    ], "Integration Tests")


def run_e2e_tests():
    """Run end-to-end tests."""
    return run_command([
        sys.executable, "tests/e2e/test_e2e.py"
    ], "End-to-End Tests")


def run_all_tests():
    """Run all tests."""
    return run_command([
        sys.executable, "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short"
    ], "All Tests")


def run_backend_tests():
    """Run backend-specific tests."""
    return run_command([
        sys.executable, "tests/integration/test_backend.py"
    ], "Backend Integration Tests")


def run_with_coverage():
    """Run tests with coverage report."""
    return run_command([
        sys.executable, "-m", "pytest", 
        "tests/", 
        "--cov=backend", 
        "--cov-report=html", 
        "--cov-report=term-missing",
        "-v"
    ], "Tests with Coverage")


def main():
    """Main test runner."""
    print("🚀 Hacker News Analytics Dashboard - Test Runner")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("Usage: python3 run_tests.py <test_type>")
        print("\nAvailable test types:")
        print("  unit        - Run unit tests only")
        print("  integration - Run integration tests only")
        print("  e2e         - Run end-to-end tests only")
        print("  backend     - Run backend integration tests")
        print("  all         - Run all tests")
        print("  coverage    - Run all tests with coverage report")
        print("\nExamples:")
        print("  python3 run_tests.py unit")
        print("  python3 run_tests.py all")
        print("  python3 run_tests.py coverage")
        return
    
    test_type = sys.argv[1].lower()
    
    # Ensure we're in the right directory
    if not Path("tests").exists():
        print("❌ Error: tests directory not found. Please run from project root.")
        return
    
    results = []
    
    if test_type == "unit":
        results.append(run_unit_tests())
    elif test_type == "integration":
        results.append(run_integration_tests())
    elif test_type == "e2e":
        results.append(run_e2e_tests())
    elif test_type == "backend":
        results.append(run_backend_tests())
    elif test_type == "all":
        results.extend([
            run_unit_tests(),
            run_integration_tests(),
            run_e2e_tests()
        ])
    elif test_type == "coverage":
        results.append(run_with_coverage())
    else:
        print(f"❌ Unknown test type: {test_type}")
        return
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Test Summary")
    print(f"{'='*60}")
    
    passed = sum(results)
    total = len(results)
    
    if total == 1:
        status = "✅ PASSED" if results[0] else "❌ FAILED"
        print(f"Test: {status}")
    else:
        for i, result in enumerate(results):
            status = "✅ PASSED" if result else "❌ FAILED"
            test_names = ["Unit", "Integration", "E2E"]
            print(f"{test_names[i]} Tests: {status}")
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 