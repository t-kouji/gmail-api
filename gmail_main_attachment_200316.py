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
pprint.pprint(msg_list)

# メッセージ一覧の最新の一つを得る
msg = msg_list['messages'][0]
id = msg['id']
threadId = msg['threadId']
# print(f'id:{id} threadId:{threadId}')

#取得したメッセージ一覧の中に添付ファイルが存在するメッセージのIDをリストとして取得。
def list_of_attachments_ID(msg_list):
    list_of_attachments_ID= []
    for msg in msg_list:
        id = msg['id']
        # メッセージの本体を取得する
        data = messages.get(userId='me', id=id).execute()
        try:
            if data['payload']['parts'][1]['body']['attachmentId']:
                list_of_attachments_ID.append(id)
        except KeyError:
            continue
    return list_of_attachments_ID

print(list_of_attachments_ID(msg_list['messages']))


import base64
from googleapiclient import errors

def GetAttachments(id,attachment_id):
    # 添付ファイルのidを取得
    # attachment_id = data['payload']['parts'][1]['body']['attachmentId']
    for d in attachment_id:
        # 添付ファイルの本体を取得
        # attachment = messages.attachments().get(userId='me',messageId = id, id=d).execute()
        # # 添付ファイルのコードを変換
        # file_data = base64.urlsafe_b64decode(attachment['data'])
        # print(file_data)
        print(d)
        print(id)

GetAttachments(id,list_of_attachments_ID(msg_list['messages']))



