#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import mailbox
import json


def message2mailobj(msg):
    mail_obj = {}

    # 最初に現れたヘッダを辞書に追加
    for key in msg.keys():
        # ヘッダはすべて小文字に正規化
        field = key.lower()
        # 複数現れるのを保存したいヘッダはリストに保持
        if field == 'received':
            if field not in mail_obj:
                mail_obj['received'] = []
            mail_obj[field].append(msg.get(field))
        elif field in mail_obj:
            next
        else:
            mail_obj[field] = str(msg.get(field))

    # body 部分の処理
    payloads = []
    if msg.is_multipart():
        # multipart の場合、ヘッダが含まれているので同じように取り込む
        for part in msg.get_payload():
            payloads.append(message2mailobj(part))
    else:
        payloads.append(msg.get_payload())
    mail_obj['payloads'] = payloads

    return mail_obj


def main():
    # 第一パラメータがメールボックスファイル
    if not os.path.exists(sys.argv[1]):
        exit(1)

    mbox = mailbox.mbox(sys.argv[1])

    mbox_obj = []
    mbox_itr = mbox.itervalues()
    mail = next(mbox_itr)
    while mail:
        mail_obj = message2mailobj(mail)
        mail_obj['mailbox_header'] = mail.get_from()
        #print(mail_obj)
        mbox_obj.append(mail_obj)

        try:
            mail = next(mbox_itr)
        except StopIteration:
            break

    print(json.dumps(mbox_obj))


if __name__ == '__main__':
    main()
