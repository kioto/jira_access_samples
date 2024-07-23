from jira import JIRA

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


def main():
    options = {
        'server': URL
    }

    jira = JIRA(options, basic_auth=(EMAIL, TOKEN))

    # ステータスは以下の３種
    # status = 'Done'  # 完了
    # status = 'To Do'  # To Do
    # status = 'In Progress'  # 進行中
    # issues = jira.search_issues(f'project = {PROJ} and status = "{status}"')
    issues = jira.search_issues(f'project = {PROJ} and status != "Done" ' \
                                'order by key')

    for issue in issues:
        print('key:', issue.key)
        print('summary:', issue.fields.summary)
        print('status:', issue.fields.status)
        print('issue type:', issue.fields.issuetype.name)
        print('labels:', issue.fields.labels)
        print()
    # issue = jira.issue('GTMS-16')
    # issue = jira.issue('SAN-5')
    # print(issue.fields.summary)


if __name__ == '__main__':
    main()
