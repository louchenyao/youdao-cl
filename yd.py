#! /usr/bin/env python
# -*- coidng: utf-8 -*-

from __future__ import print_function

import os
import sys

if sys.version_info[0] == 2:
    PY2 = True
else:
    PY2 = False

if PY2:
    import httplib as hc
    from urllib import urlencode
else:
    import http.client as hc
    from urllib.parse import urlencode

import argparse
import json

def query(words):
    params = {
        "keyfrom": "wordstash",
        "key": "908579755",
        "type": "data",
        "doctype": "json",
        "version": "1.1",
        "q": words,
    }
    
    url = "/openapi.do?" + urlencode(params)
    conn = hc.HTTPConnection("fanyi.youdao.com")
    conn.request("GET", url)
    rep = conn.getresponse()
    data = rep.read()
    conn.close()

    data = data.decode("utf-8")
    data = json.loads(data)
    return data

def pretty_print(res):
    if res["errorCode"]:
        print("erroCode = %d\n" % res["errorcode"])
        return

    if "basic" in res:
        print("Basic:")
        basic = res["basic"]
        if "uk-phonetic" in basic: print(u"    uk-phonetic: %s" % basic["uk-phonetic"]);
        if "us-phonetic" in basic: print(u"    us-phonetic: %s" % basic["us-phonetic"]);
        if "phonetic" in basic:    print(u"    phonetic: %s" % basic["phonetic"]);
        if "explains" in basic:
            cnt = 1;
            for explain in basic["explains"]:
                print(u"    %s. " % cnt + explain)
                cnt += 1

    if "translation" in res:
        print("Translation:")
        for line in res["translation"]:
            print(u"    " + line);

    if "web" in res:
        print("Web:")
        for item in res["web"]:
            print(u"    %s:" % item["key"])
            print(u"        ", end=u"")
            for trans in item["value"]:
                print("%s; " % trans, end=u"")
            print()

def main(word):
    res = query(word)
    pretty_print(res)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("words")
    args = parser.parse_args()
    words = args.words

    base_dir = os.path.dirname(os.path.abspath(__file__))
    history_path = os.path.join(base_dir, "history.log")
    with open(history_path, "a") as f:
        f.write("%s\n" % words)

    main(args.words)
