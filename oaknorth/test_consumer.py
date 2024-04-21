from csv import DictReader

import pytest

from consumer import consume_invoices


@pytest.fixture
def invoices():
    with open("invoices.csv") as f:
        yield list(DictReader(f))


def test_total_invoices_per_organisation(invoices):
    assert consume_invoices(invoices)['total']['1000'] == 5
    
def test_unpaid_invoices_per_organisation(invoices):
    assert consume_invoices(invoices)['unpaid']['1000'] == 2

def test_overdue_invoices_per_organisation(invoices):
    assert consume_invoices(invoices)['overdue']['1000'] == 2
    
def test_monthly_paid_invoices_per_organisation(invoices):
    assert consume_invoices(invoices)['paid_per_month']['11']['1000'] == 2