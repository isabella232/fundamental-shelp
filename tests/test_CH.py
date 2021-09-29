# SPDX-FileCopyrightText: 2014 SAP SE Srdjan Boskovic <srdjan.boskovic@sap.com>
#
# SPDX-License-Identifier: Apache-2.0

import pytest
from abapsystems import *
from pyshlp import *


#
# I64 CH Helps
#

c = get_connection(I64)

vih = valueInput(c)

def test_not_supported():

    try:
        r = vih.get_shelp_descriptor("CL XXXX")
    except Exception as e:
        assert e.message == "search help type CL not supported, only SH, CH and CT"


def test_CH_EKKO():
    shlpname = "CH EKPO"
    sel = [["EBELN", "I", "CP", "414-01*", ""]]

    r = vih.search(shlpname, sel)

    assert r["headers"] == [[u"EBELN", u"Purch.Doc.", 10], [u"EBELP", u"Item", 5]]
    expected_search_result = [
        {u"EBELP": u"00010", u"EBELN": u"414-0100"},
        {u"EBELP": u"00020", u"EBELN": u"414-0100"},
        {u"EBELP": u"00030", u"EBELN": u"414-0100"},
        {u"EBELP": u"00040", u"EBELN": u"414-0100"},
        {u"EBELP": u"00050", u"EBELN": u"414-0100"},
        {u"EBELP": u"00060", u"EBELN": u"414-0100"},
        {u"EBELP": u"00070", u"EBELN": u"414-0100"},
        {u"EBELP": u"00080", u"EBELN": u"414-0100"},
        {u"EBELP": u"00090", u"EBELN": u"414-0100"},
        {u"EBELP": u"00100", u"EBELN": u"414-0100"},
        {u"EBELP": u"00110", u"EBELN": u"414-0100"},
        {u"EBELP": u"00010", u"EBELN": u"414-0101"},
        {u"EBELP": u"00020", u"EBELN": u"414-0101"},
        {u"EBELP": u"00030", u"EBELN": u"414-0101"},
        {u"EBELP": u"00040", u"EBELN": u"414-0101"},
        {u"EBELP": u"00050", u"EBELN": u"414-0101"},
        {u"EBELP": u"00060", u"EBELN": u"414-0101"},
        {u"EBELP": u"00070", u"EBELN": u"414-0101"},
        {u"EBELP": u"00080", u"EBELN": u"414-0101"},
        {u"EBELP": u"00090", u"EBELN": u"414-0101"},
        {u"EBELP": u"00100", u"EBELN": u"414-0101"},
        {u"EBELP": u"00110", u"EBELN": u"414-0101"},
        {u"EBELP": u"00010", u"EBELN": u"414-0102"},
        {u"EBELP": u"00020", u"EBELN": u"414-0102"},
        {u"EBELP": u"00030", u"EBELN": u"414-0102"},
        {u"EBELP": u"00040", u"EBELN": u"414-0102"},
        {u"EBELP": u"00050", u"EBELN": u"414-0102"},
        {u"EBELP": u"00060", u"EBELN": u"414-0102"},
        {u"EBELP": u"00070", u"EBELN": u"414-0102"},
        {u"EBELP": u"00080", u"EBELN": u"414-0102"},
        {u"EBELP": u"00090", u"EBELN": u"414-0102"},
        {u"EBELP": u"00100", u"EBELN": u"414-0102"},
        {u"EBELP": u"00110", u"EBELN": u"414-0102"},
    ]

    assert len(expected_search_result) == len(r["search_result"])

    for i, result_line in enumerate(r["search_result"]):
        assert result_line == expected_search_result[i]
