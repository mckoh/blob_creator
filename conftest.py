"""
Test Configuration for Blob Creator

Author: Michael Kohlegger
Date: 2021-09
"""

from anybadge import Badge
import pytest


def pytest_configure(config):
    """Pytest configuration"""
    config.addinivalue_line(
        "markers", "my_own: Marks own tests that are to be distinguished from third party tests"
    )


def pytest_sessionstart(session):
    """Pytest hook for test start"""
    session.results = {}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook for test run"""
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[item] = result


def pytest_sessionfinish(session, *_):
    """Pytest hook for test end"""

    thresholds = {
        20: 'red',
        40: 'orange',
        60: 'yellow',
        100: 'green'
    }

    passed_amount = sum(1 for result in session.results.values() if result.passed)
    failed_amount = sum(1 for result in session.results.values() if result.failed)

    if passed_amount+failed_amount == 0:
        test_score = 0.0
    else:
        test_score = passed_amount / (passed_amount + failed_amount) * 100

    badge = Badge('pytest success', test_score, thresholds=thresholds, default_color="red")
    badge.write_badge('pytest_badge.svg', overwrite=True)
