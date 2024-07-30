"""実行中のエピックを取り出す

Example:
$ python exec_jquery.py 'status!="Done" and issuetype="エピック" order by key'

"""
import sys
from jira import JIRA
import jiratools as jt


ENV_FILE = 'env.txt'


Env = jt.Env.open(ENV_FILE)
Jira = JIRA({'server': Env.url}, basic_auth=(Env.email, Env.token))


def get_children_issues(parent_issue):
    """子チケットの取得
    """
    query = f'project={Env.project} and parent={parent_issue.id} order by key'
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
    issues = Jira.search_issues(f'project={Env.project} and ' + query)

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
