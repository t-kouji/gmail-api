#coding: utf-8
import httplib2, os
from googleapiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage
import pprint

# Gmail権限のスコープを指定
SCOPES = 'https://mail.google.com/'
# 認証ファイル
CLIENT_SECRET_FILE = 'credentials.json'
USER_SECRET_FILE = 'credentials-gmail.json'
# ------------------------------------
# ユーザ認証データの取得
def gmail_user_auth():
    store = Storage(USER_SECRET_FILE)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = 'Python Gmail API'
        credentials = tools.run_flow(flow, store, None)
        print('認証結果を保存しました:' + USER_SECRET_FILE)
    return credentials
# Gmailのサービスを取得
def gmail_get_service():
    credentials = gmail_user_auth()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    return service
# ------------------------------------
# GmailのAPIが使えるようにする
service = gmail_get_service()

# メッセージを扱うAPI
messages = service.users().messages()
# 自分のメッセージ一覧を10件得る
msg_list = messages.list(userId='me', maxResults=10).execute()


import sys
print(sys.version)
# print(msg_list)

# メッセージ一覧の最新の一つを得る
msg = msg_list['messages'][0]
id = msg['id']
threadId = msg['threadId']
print(f'id:{id} threadId:{threadId}')

# メッセージの本体を取得する
data = messages.get(userId='me', id=id).execute()

# メッセージの本体の要約（snippet）を取得し出力する
print(data['snippet'])
pprint.pprint(data)
attachment_str = data['payload']['parts'][1]['body']['attachmentId']

"""Retrieve an attachment from a Message."""

import base64
from googleapiclient import errors


def GetAttachments(service, user_id, msg_id):
# -------
# #   Get and store attachment from Message with given id.
# #   Args:
# #     service: Authorized Gmail API service instance.
# #     user_id: User's email address. The special value "me"
# #     can be used to indicate the authenticated user.
# #     msg_id: ID of Message containing attachment.
# #     store_dir: The directory used to store attachments.
# -------
    try:

        attachment = messages.attachments().get(userId='me',messageId = id, id=attachment_str).execute()
        file_data = base64.urlsafe_b64decode(attachment['data'])
        print(file_data)

        # for part in message['payload']['parts']:
        #     if part['filename']:
        #         print(part['filename'])
        #         file_data = base64.urlsafe_b64decode(part['parts'][0]['body']['data'].encode('UTF-8'))
        #         path = ''.join([store_dir, part['filename']])

        #         f = open(path, 'w')
        #         f.write(file_data)
        #         f.close()

    except errors.HttpError as error:
        print ('An error occurred: %s' % error)



GetAttachments(gmail_get_service,'me',id)
