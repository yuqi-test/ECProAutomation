# -*- coding: utf-8 -*-
'''
@author: wsy
'''
import base64
import hashlib
import hmac
import json

from utils.converter.encoding import isUnicode


def bjca_hmac(secret, jdata):
    plain = ''
    for key in sorted(jdata.keys()):
        if jdata[key] != None and isUnicode(jdata[key]) and len(jdata[key]) != 0:
            if type(jdata[key]) == type({}):
                plain = plain + key + '=' + _sort_json_obj(jdata[key]) + '&'
            elif type(jdata[key]) == type([]):
                plain = plain + key + '=' + _sort_list_obj(jdata[key]) + '&'
            else:
                if isUnicode(jdata[key]):
                    plain = plain + key + '=' + (jdata[key]) + '&'
                else:
                    plain = plain + key + '=' + str(jdata[key]) + '&'
        elif jdata[key] != None and not isUnicode(jdata[key]):
            if type(jdata[key]) == type({}):
                plain = plain + key + '=' + _sort_json_obj(jdata[key]) + '&'
            elif type(jdata[key]) == type([]):
                plain = plain + key + '=' + _sort_list_obj(jdata[key]) + '&'
            else:
                if isUnicode(jdata[key]):
                    plain = plain + key + '=' + (jdata[key]) + '&'
                else:
                    plain = plain + key + '=' + str(jdata[key]) + '&'
        else:
            del jdata[key]
    if isUnicode(plain): plain = plain[:-1].replace('True', 'true').replace('False', 'false').encode('utf-8')
    signature = hmac.new(secret.encode(), plain, digestmod=hashlib.sha256).digest()
    jdata['signature'] = base64.b64encode(signature).decode()
    return json.dumps(jdata, sort_keys=True)


def _sort_json_obj(jobj):
    strObj = '{'
    for objkey in sorted(jobj.keys()):
        if type(jobj[objkey]) == type({}):
            strObj = strObj + objkey + '=' + _sort_json_obj(jobj[objkey]) + ', '
        elif type(jobj[objkey]) == type([]):
            strObj = strObj + objkey + '=' + _sort_list_obj(jobj[objkey]) + ', '
        else:
            if not jobj[objkey]:
                strObj = strObj + objkey + '=null, '
            else:
                if isUnicode(jobj[objkey]):
                    strObj = strObj + objkey + '=' + jobj[objkey] + ', '
                else:
                    strObj = strObj + objkey + '=' + str(jobj[objkey]) + ', '
    strObj = strObj[:-2] + '}'
    return strObj


def _sort_list_obj(lobj):
    strObj = '['
    for objkey in lobj:
        if type(objkey) == type({}):
            strObj = strObj + _sort_json_obj(objkey) + ', '
        elif type(objkey) == type([]):
            strObj = strObj + _sort_list_obj(objkey) + ', '
        else:
            if not objkey:
                strObj = strObj + '=null, '
            else:
                if isUnicode(objkey):
                    strObj = strObj + objkey + ', '
                else:
                    strObj = strObj + str(objkey) + ', '
    strObj = strObj[:-2] + ']'
    return strObj


if __name__ == '__main__':
    jdata = {
        "algo": "RSA",
        "appId": "APP_59F4B704C6414344812E7EEF3BBFEE3F",
        "bussinessId": "getCert_1551071913309",
        "deviceId": "DEV_1F26075C040D43AEA58DE5B83D1E433D",
        "encPack": "{\"BJCAROOT\":{\"EncCert\":{\"EncAlg\":\"1\",\"EncCertKeyID\":\"\",\"EncCertSN\":\"0980990000019ECF6A\"},\"EncData\":\"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\",\"EncKey\":\"nFQwKaWvqUiCsHm0q64cmyweWi6B2fCrmTzGypfcQk8zXSOT4boZkpsdhXHGWYHm1v7XF3Nl+Iv6Tg/wT/7CgH72MgzgAkfabHgT/G1Ir4u9vaaRRor80U1j/faY3DBKsUb+ofpkiiFxl3z96Us760Ib/5gmlPpp/OXWH5EETpg=\",\"SignTID\":\"\",\"Version\":\"2\"}}",
        "signAlgo": "HMAC",
        "version": "1.0",
    }

    print(bjca_hmac('Y934rsAOYUEABD2mMZSZHcDNChdDbZh1', jdata))
