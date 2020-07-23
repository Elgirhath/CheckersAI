from tests.tests import Tests
import argparse

parser = argparse.ArgumentParser(description='Run tests')
parser.add_argument('--debug', action="store_true", help='run tests with UI')

args = parser.parse_args()

Tests.runTests(args.debug)