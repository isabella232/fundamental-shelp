# SPDX-FileCopyrightText: 2014 SAP SE Srdjan Boskovic <srdjan.boskovic@sap.com>
#
# SPDX-License-Identifier: Apache-2.0

# Value Input Help

'''
SH  Search help (default)
CH  Check table
CT  Check table with text table
FV  Fixed values for domains
DV  Fixed values from flow logic
# CA  Calendar helpBAPIUPDATE
# CL  Time help
SR  Search help for data element (temporary)
MC  Matchcode
MI  MaPtchcode ID
IN  Internal Table
'''

import operator
from collections import OrderedDict
from pyrfc import RFCError

class valueInput:
    def __init__(self, connection, user_parameters=None):
        self.__conn = connection
        if user_parameters is None:
            self._SU3Params = self.__conn.call('BAPI_USER_GET_DETAIL', USERNAME='DEMO')['PARAMETER']
        else:
            self._SU3Params = user_parameters
        self._Descriptors = {}     # Collective or elementary helps in backend format (ET_SHLP)
        self._ElementaryHelp = {}  # Elementary helps in server format
        self._FieldDomainValues = {}


    def get_shelp_descriptor(self, shlpname):
        '''
        SHLP descriptors are returned in ET_SHLP table: one single row for the elementary
        help, or multiple rows, in case of collective help. The sequence of rows in this table
        determines the sequence of help tabs in SAPGUI, the table is returned sorted.
        Elementary helps are stored in a single list, to avoid redundancy, as one elementary
        help can be part of more collectives.
        '''
        try:
            helptype, helpname = shlpname.split()
        except Exception, e:
            return {'error': 'invalid help id format: %s' % shlpname}

        if helptype in ('SH', 'CT', 'CH'):
            if shlpname not in self._Descriptors:
                self._Descriptors[shlpname] = \
                    self.__conn.call('ZSHLP_METADATA_GET', IV_SHLPNAME = helpname, IV_SHLPTYPE = helptype)

                for shlp in self._Descriptors[shlpname]['ET_SHLP']:
                    elem_shlpname = '%s %s' % (shlp['SHLPTYPE'], shlp['SHLPNAME'])
                    if elem_shlpname not in self._ElementaryHelp:
                        self._ElementaryHelp[elem_shlpname] = self.__elementary(shlp)

            elementary_helps = OrderedDict()
            for shlp in self._Descriptors[shlpname]['ET_SHLP']:
                elem_shlpname = '%s %s' % (shlp['SHLPTYPE'], shlp['SHLPNAME'])
                elementary_helps[elem_shlpname] = self._ElementaryHelp[elem_shlpname]

            return {'elementary_helps': elementary_helps}
        else:
            raise Exception, 'search help type %s not supported, only SH, CH and CT' % helptype


    def get_field_values(self, shlpname):
        helptype, helpname = shlpname.split()
        if helptype != 'FV':
            return []
        if shlpname not in self._FieldDomainValues:
            # _todo: error handdling, like wrong domain name ...
            self._FieldDomainValues[shlpname] = self.__conn.call('ZDYN_DOMVALUES_GET', IV_DOMNAME=helpname)
        return self._FieldDomainValues[shlpname]


    def __del__(self):
        # _todo: not needed in production
        if self.__conn is not None:
            self.__conn.close()


    def __elementary(self, shlp):
        newhelp = {}

        newhelp['INTDESCR'] = shlp['INTDESCR']
        newhelp['SCRLENMAX'] = 0
        newhelp['SHLPOUTPUT'] = ''
        newhelp['ALLOUTPUTS'] = []

        if shlp['SHLPTYPE'] == 'SH':

            # FIELDDESCR post-processing
            for fd in shlp['FIELDDESCR']:
                # convert to integers
                for intfield in ['POSITION', 'OFFSET',  'LENG',    'INTLEN', 'OUTPUTLEN', 'DECIMALS',
                                 'HEADLEN',  'SCRLEN1', 'SCRLEN2', 'SCRLEN3']:
                    fd[intfield] = int(fd[intfield])
                # merge FIELDPROP to FIELDDESCR
                for fp in shlp['FIELDPROP']:
                    if fd['FIELDNAME'] == fp['FIELDNAME']:
                        fd['SHLPOUTPUT'] = fp['SHLPOUTPUT']
                        fd['SHLPSELPOS'] = fp['SHLPSELPOS']
                        fd['SHLPLISPOS'] = fp['SHLPLISPOS']
                        fd['DEFAULTVAL'] = fp['DEFAULTVAL'] # SU01 defaults shown in SE11
                        # Search Help output (result)
                        if fp['SHLPOUTPUT'] == 'X':
                            if not newhelp['SHLPOUTPUT']:   # _todo: multiple outputs
                                newhelp['SHLPOUTPUT'] = fp['FIELDNAME']
                            newhelp['ALLOUTPUTS'].append(fp['FIELDNAME'])
                        break;
                # merge INTERFACE to FIELDDESCR
                for fi in shlp['INTERFACE']:
                    if fd['FIELDNAME'] == fi['SHLPFIELD']:
                        fd['TOPSHLPNAM'] = fi['TOPSHLPNAM']
                        fd['TOPSHLPFLD'] = fi['TOPSHLPFLD']
                        break;
                # Max parameter caption length
                if fd['SCRLEN3'] > newhelp['SCRLENMAX']:
                    newhelp['SCRLENMAX'] = fd['SCRLEN3']
                # Takeover SU01 user parameters values
                # Both the DEFAULTVAL of the FIELDPROP and the MEMORYID of
                # the FIELDDESCR may contain the SU3 parameter ID.
                # The DEFAULTVAL does not exist in CT helps (no FIELDPROP
                # table filled) and in SH helps it appears filled with less
                # fields then MEMORYID.
                # In the next line, if MEMORYID is replaced with DEFAULTVAL,
                # only user param defaults of DEFAULTVAL will be taken over,
                # just like in SE11 help test or in applications. With MEMORYID all
                # user param defaults maintained in SU01/SU3 are taken over,
                # thus more input fields defaulted than in SAPGUI. __todo: check this ...
                if len(fd['DEFAULTVAL']) > 0:
                    for p in self._SU3Params:
                        if p['PARID'] == fd['MEMORYID']:
                            fd['PARVA'] = p['PARVA']
                            # fd['PARTXT'] = p['PARTXT']
                            break;
                # if user defaults not set
                if 'PARVA' not in fd:
                    fd['PARVA'] = ''
                    fd['PARTXT'] = ''

        elif shlp['SHLPTYPE'] in ('CH','CT'):
            fielddescr_shlpoutput = ''
            # FIELDDESCR post-processing
            for fd in shlp['FIELDDESCR']:
                # convert to integers
                for intfield in ['POSITION', 'OFFSET',  'LENG',    'INTLEN', 'OUTPUTLEN', 'DECIMALS',
                                 'HEADLEN',  'SCRLEN1', 'SCRLEN2', 'SCRLEN3']:
                    fd[intfield] = int(fd[intfield])
                # merge FIELDPROP to FIELDDESCR
                for fp in shlp['FIELDPROP']:
                    if fd['FIELDNAME'] == fp['FIELDNAME']:
                        fd['SHLPOUTPUT'] = fp['SHLPOUTPUT']
                        fd['SHLPSELPOS'] = fp['SHLPSELPOS']
                        fd['SHLPLISPOS'] = fp['SHLPLISPOS']
                        # fd['DEFAULTVAL'] = fp['DEFAULTVAL'] # no DEFAULTVAL in CT helps
                        # Search Help output (result)
                        if fp['SHLPOUTPUT'] == 'X':
                            if not newhelp['SHLPOUTPUT']:
                                newhelp['SHLPOUTPUT'] = fp['FIELDNAME']
                        break;
                # merge INTERFACE to FIELDDESCR
                for fi in shlp['INTERFACE']:
                    if fd['FIELDNAME'] == fi['SHLPFIELD']:
                        fd['TOPSHLPNAM'] = fi['TOPSHLPNAM']
                        fd['TOPSHLPFLD'] = fi['TOPSHLPFLD']
                        break;
                # Max parameter caption length
                if fd['SCRLEN3'] > newhelp['SCRLENMAX']:
                    newhelp['SCRLENMAX'] = fd['SCRLEN3']
                # Takeover SU01 user parameters values
                # Both the DEFAULTVAL of the FIELDPROP and the MEMORYID of
                # the FIELDDESCR may contain the SU3 parameter ID.
                # The DEFAULTVAL does not exist in CT helps (no FIELDPROP
                # table filled) and in SH helps it appears filled with less
                # fields then MEMORYID.
                # In the next line, if MEMORYID is replaced with DEFAULTVAL,
                # only user param defaults of DEFAULTVAL will be taken over,
                # just like in SE11 help test or in applications. With MEMORYID all
                # user param defaults maintained in SU01/SU3 are taken over,
                # thus more input fields defaulted than in SAPGUI. __todo: check this ...
                if len(fd['MEMORYID']) > 0: # this is CT help, no FIELDPROP/DEFAULTVAL
                    for p in self._SU3Params:
                        if p['PARID'] == fd['MEMORYID']:
                            fd['PARVA'] = p['PARVA']
                            # fd['PARTXT'] = p['PARTXT']
                            break;
                # if user defaults not set
                if 'PARVA' not in fd:
                    fd['PARVA'] = ''
                    fd['PARTXT'] = ''
                if fd['MAC']:
                    fielddescr_shlpoutput = fd['FIELDNAME']
            # CT help output field
            if not newhelp['SHLPOUTPUT']:
                # output not found in FIELDPROP
                if not fielddescr_shlpoutput:
                    # output not found in FIELDDESCR, take anything and
                    # echo the case
                    print 'no SHLPOUTPUT for %s %s' % (shlp['SHLPTYPE'], shlp['SHLPNAME'])
                    newhelp['SHLPOUTPUT'] = shlp['INTERFACE'][0]['SHLPFIELD']
                else:
                    newhelp['SHLPOUTPUT'] = fielddescr_shlpoutput

        # sort by position
        newhelp['FIELDDESCR'] = sorted(shlp['FIELDDESCR'], key=lambda k: k['POSITION'])

        # remove multiple outputs if not found
        if len(newhelp['ALLOUTPUTS']) == 1:
            del newhelp['ALLOUTPUTS']

        return newhelp


    def get_user_params(self):
        return self._SU3Params


    def search(self, shlpname, select_options, maxrows = 0, compact=False):
        if shlpname not in self._ElementaryHelp:
            self.get_shelp_descriptor(shlpname)
        helptype, helpname = shlpname.split()
        so = []
        for s in select_options: #  _todo: clean up
            so_record = {}
            so_record['SHLPNAME']  = shlpname
            so_record['SHLPFIELD'] = s[0]
            so_record['SIGN']      = s[1]
            so_record['OPTION']    = s[2]
            so_record['LOW']       = s[3].upper()
            so_record['HIGH']      = s[4].upper()
            so.append(so_record)
        try:
            r = self.__conn.call('ZSHLP_GET', IV_SHLPTYPE = helptype, IV_SHLPNAME = helpname, IT_SELOPT = so, IV_MAXROWS = maxrows)
        except RFCError as ex:
            # errors like dynpro sent in background in SH DEBIC for example ...
            error = {}
            ex_type_full = str(type(ex))
            error['type'] = ex_type_full[ex_type_full.rfind(".")+1:ex_type_full.rfind("'")]
            error['code'] = ex.code if hasattr(ex, 'code') else '<None>'
            error['key'] = ex.key if hasattr(ex, 'key') else '<None>'
            error['message'] = ex.message
            return {'error': error}

        # map ET_VALUE_LIST name/value array into SH result table
        result = []
        result_line = [] if compact else {} # compact: array w/o header names in search records, only values, otherwise dict
        recordpos = '0000'
        # headers sequence in Search Result may differ from FIELDDESCR[POSITION] sequence
        help_headers = {}
        for f in self._ElementaryHelp[shlpname]['FIELDDESCR']:
            help_headers[f['FIELDNAME']] = [f['REPTEXT'], f['LENG']] # _todo: check unicode here
        headers = []
        for record in r['ET_VALUE_LIST']:
            if record['RECORDPOS'] == '0001':
                # this check required because the recordpos starts from
                # 0001 but after reaching 9999 rolls down to 0000 and
                # again to 0001 etc.
                if len(headers) < len(help_headers):
                    headers += [[record['FIELDNAME']] + help_headers[record['FIELDNAME']]]
            if recordpos != record['RECORDPOS']:
                # new record, append line
                if result_line:
                    result.append(result_line)
                    result_line = [] if compact else {}
                # new record
                recordpos = record['RECORDPOS']
            if compact:
                result_line.append(record['FIELDVAL'])
            else:
                result_line[record['FIELDNAME']] = record['FIELDVAL']
        # last line
        if result_line:
            result.append(result_line)
        # sort per first column (default)
        if len(result) > 0:
            if compact:
                result = sorted(result, key=lambda k: k[0])
            else:
                result = sorted(result, key=lambda k: k[headers[0][0]])
        # maxrows exceeded
        exceeded = r['EV_MAXROWS_EXCEEDED']
        # search result output field
        shlpoutput = self._ElementaryHelp[shlpname]['SHLPOUTPUT']
        return {'search_result': result, 'shlpoutput': shlpoutput, 'maxrows_exceeded': exceeded, 'headers':headers, 'desc':r['ET_VALUE_DESC']}

    #
    # used for internal testing only, most likely not needed in the future
    #

    def print_params(self, shlpname):
        # print input parameters of a given Searh Help, with SU01 defaults
        Params = self.get_help_params(shlpname)
        scrlenmax = self._ElementaryHelp[shlpname]['SCRLENMAX']
        '''       1   2     3                     4    5   6     7     8     9'''
        format = '%2d %-10s %-'+str(scrlenmax)+'s %-5s %3d %-10s %-18s %-40s %1s'
        for p in Params:
            '''             1                   2               3               4              5               6              7           8            9'''
            print format % (int(p['POSITION']), p['FIELDNAME'], p['SCRTEXT_L'], p['DATATYPE'], int(p['LENG']), p['MEMORYID'], p['PARVA'], p['PARTXT'], p['SHLPOUTPUT'])


    def get_search_result_headers(self, shlpname):
        headers = {}
        for f in self._ElementaryHelp[shlpname]['FIELDDESCR']:
            headers[f['FIELDNAME']] = [f['REPTEXT'], f['LENG']] # _todo: check unicode here
        return headers


    def get_title(self, shlpname):
        return self._ElementaryHelp[shlpname]['INTDESCR']['DDTEXT']


    def get_help_params(self, shlpname):
        return self._ElementaryHelp[shlpname]['FIELDDESCR']


    def get_search_defaults(self, shlpname):
        # get all search defaults, relevant for a given Search Help
        defaults = []
        for fielddesc in self._ElementaryHelp[shlpname]['FIELDDESCR']:
            if len(fielddesc['DEFAULTVAL']) > 0:
                defaults.append({fielddesc['FIELDNAME'] : fielddesc['MEMORYID']})
        return defaults


    def get_input_defaults_user(self, shlpname):
        # get user SU01 params/values relevant for a given Search Help
        sel = []
        for p in self._SU3Params:
            for fielddesc in self._ElementaryHelp[shlpname]['FIELDDESCR']:
                # remove the next check if all SU01 user defaults shall be
                # applied. with this check only parameters from SE11 applied
                if len(fielddesc['DEFAULTVAL']) > 0:
                    if p['PARID'] == fielddesc['MEMORYID']: # PARID
                        sel.append([fielddesc['FIELDNAME'], 'I', 'EQ', p['PARVA'], ''])
        return sel

if __name__ == "__main__":
    from abapsystems import *
    c = get_connection(I64)
