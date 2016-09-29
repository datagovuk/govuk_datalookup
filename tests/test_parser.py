# -*- coding: utf-8 -*-
from govuk_datalookup.fetch import parse_html

def test_valid():
    html = open("tests/data/sample.html", "r").read()
    results = parse_html(u'test', html)

    assert len(results) > 0

    assert results[u'name'] == u'test'
    assert results[u'title'] == u'Ofqual spend data over £25k'
    assert results[u'notes'] != u''
    assert results[u'owner_org'] == 'ofqual'
    assert len(results[u'resources']) == 53

def test_invalid():
    html = ""
    results = parse_html(u'test', html)

    assert len(results) == 0

def test_bad_input():
    assert parse_html('', None) == {}
    assert parse_html(None, None) == {}

