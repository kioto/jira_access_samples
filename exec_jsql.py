"""実行中のエピックを取り出す

Example:
$ python exec_jquery.py 'status!="Done" and issuetype="エピック" order by key'

"""
import sys
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


Jira = JIRA({'server': URL}, basic_auth=(EMAIL, TOKEN))


def get_children_issues(parent_issue):
    """子チケットの取得
    """
    query = f'project={PROJ} and parent={parent_issue.id} order by key'
    children = Jira.search_issues(query)
    if children is None:
        children = []

    return children


def get_issue_short_info(issue):
    """チケットの短い情報を出力
    """
    buf = f'{issue.key}: {issue.fields.issuetype}'
    """
    if hasattr(issue, 'customfield_10052'):  # 開始日
        buf += issue.fields.customfield_10052
    if issue.fields.duedate:  # 終了日
        buf += f' ~{issue.fields.duedate}'
    """
    return buf


def print_children(issue, level=1):
    for child in get_children_issues(issue):
        print('  '*level, get_issue_short_info(child))
        print_children(child, level+1)


def main(query):
    issues = Jira.search_issues(f'project={PROJ} and ' + query)

    for issue in issues:
        # チケット情報
        print('key:', issue.key)
        fields = issue.fields
        print('summary:', fields.summary)
        print('status:', fields.status)             # 進行中、完了など
        print('issue type:', fields.issuetype.name)  # エピック、タスクなど
        print('labels:', fields.labels)
        # print('start date: ', fields.customfield_10052)
        # print('due date  : ', fields.duedate)

        # 子チケット（３レベルまで）
        print('children:')
        print_children(issue)

        print()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: python exec_jsql.py <JSQL STRING>')
        exit()

    main(sys.argv[1])
