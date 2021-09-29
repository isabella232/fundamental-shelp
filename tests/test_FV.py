# SPDX-FileCopyrightText: 2014 SAP SE Srdjan Boskovic <srdjan.boskovic@sap.com>
#
# SPDX-License-Identifier: Apache-2.0

import pytest
from pyshlp import *
from abapsystems import *

c = get_connection(I64)

vih = valueInput(c)

#
# Field Values Test
#


def test_FV_RET_TYPE():

    r = vih.get_field_values("FV RET_TYPE")

    assert r == {
        u"ET_VALUES": [
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Not Applicable",
                u"DOMNAME": u"RET_TYPE",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0001",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Applicable (Header Level)",
                u"DOMNAME": u"RET_TYPE",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"H",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0002",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Applicable (Item Level)",
                u"DOMNAME": u"RET_TYPE",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"I",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0003",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Secured by Bond",
                u"DOMNAME": u"RET_TYPE",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"B",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0004",
            },
        ]
    }


def test_FV_ESTAK():

    r = vih.get_field_values("FV ESTAK")

    assert r == {
        u"ET_VALUES": [
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"RFQ with Quotation",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"A",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0001",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order from Automatic Conversion of Requisitions",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"B",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0002",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order from Goods Receipt",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"C",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0003",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order from Data Transfer",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"D",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0004",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order from Allocation Table",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"E",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0005",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order from Kanban",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"F",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0006",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order from Store Order",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"G",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0007",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order from DRP",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"H",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0008",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order from BAPI",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"I",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0009",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order from ALE Scenario",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"J",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0010",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Scheduling Agreement from CRM",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"L",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0011",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Collective Purchase Order",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"S",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0012",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order Created via Function Module",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"X",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0013",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order from APO",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"1",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0014",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Enjoy Purchase Order",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"9",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0015",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order from BBP",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"K",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0016",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Third-Party Order from CRM",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"2",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0017",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Returns Order from Incorrect Delivery",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"3",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0018",
            },
            {
                u"APPVAL": u"X",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Purchase Order Ignored for Collective Delivery Run",
                u"DOMNAME": u"ESTAK",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"W",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0019",
            },
        ]
    }


def test_FV_MM_MEMORYTYPE():

    r = vih.get_field_values("FV MM_MEMORYTYPE")

    assert r == {
        u"ET_VALUES": [
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Document Saved as Complete",
                u"DOMNAME": u"MM_MEMORYTYPE",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0001",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Document Parked",
                u"DOMNAME": u"MM_MEMORYTYPE",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"P",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0002",
            },
            {
                u"APPVAL": u"",
                u"DDLANGUAGE": u"E",
                u"DDTEXT": u"Document on Hold",
                u"DOMNAME": u"MM_MEMORYTYPE",
                u"DOMVALUE_H": u"",
                u"DOMVALUE_L": u"H",
                u"DOMVAL_HD": u"",
                u"DOMVAL_LD": u"",
                u"VALPOS": u"0003",
            },
        ]
    }


#
# tear down
#

#
