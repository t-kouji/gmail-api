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
# pprint.pprint(msg_list)
#上記のメッセージID一覧を取得（idとthreadId）
msg_ID_list = msg_list['messages']
pprint.pprint(msg_ID_list)

#取得したメッセージ一覧の中に添付ファイルが存在するメッセージのID及びattachmentIdをリストとして取得。
def dict_of_attachment_ID(msg_ID_list):
    dict_of_attachment_ID= {}
    for msg in msg_ID_list:
        #メッセージIDを取得
        id = msg['id']
        # メッセージの本体を取得する
        data = messages.get(userId='me', id=id).execute()
        
        try:
            if data['payload']['parts'][1]['body']['attachmentId']:
                #attachmentIDを取得
                attachment_ID = data['payload']['parts'][1]['body']['attachmentId']
                dict_of_attachment_ID[id] = attachment_ID
        except KeyError:
            continue
    return dict_of_attachment_ID

pprint.pprint(dict_of_attachment_ID(msg_ID_list))


import base64
from googleapiclient import errors

def GetAttachments(dict_of_attachment_ID):
    for k,v in dict_of_attachment_ID.items():
        # 添付ファイルの本体を取得
        attachment = messages.attachments().get(userId='me',messageId = k, id=v).execute()
        # 添付ファイルのコードを変換
        file_data = base64.urlsafe_b64decode(attachment['data'])
        print(file_data)


GetAttachments(dict_of_attachment_ID(msg_ID_list))