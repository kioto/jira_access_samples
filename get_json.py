import sys
import requests
import json


ENV_FILE = 'env.txt'

TOKEN = ''  # あらかじめ発行したトークン
URL = ''    # https://xxxx.atlassian.net
EMAIL = ''  # トークンを発行したユーザのメールアドレス
PROJ = ''   # プロジェクト名
with open(ENV_FILE, 'r') as f:
    [TOKEN, URL, EMAIL, PROJ] = [param.rstrip() for param in f.readlines()]

if '' in [TOKEN, URL, EMAIL, PROJ]:
    # １つでも空文字が残っていればエラー
    print('ERROR: env.txt')
    exit()

API = URL + '/rest/api/3/issue/'
HEADERS = {
  'Accept': 'application/json',
  'Authorization': TOKEN
}


def main(issue_key):
    url = API + issue_key
    response = requests.get(url, auth=(EMAIL, TOKEN))
    print(json.dumps(json.loads(response.text),
                     sort_keys=True, indent=4,
                     separators=(',', ': '),
                     ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(f'Usage: python {sys.argv[0]} <ISSUE_KEY>')
        exit()

    main(sys.argv[1])
