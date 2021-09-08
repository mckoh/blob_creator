
from anybadge import Badge
import pytest


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[item] = result


def pytest_sessionfinish(session, exitstatus):
    
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