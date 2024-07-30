from jira import JIRA
import jiratools as jt

ENV_FILE = 'env.txt'


Env = jt.Env.open(ENV_FILE)


def main():
    jira = JIRA({'server': Env.url},
                basic_auth=(Env.email, Env.token))

    # ステータスは以下の３種
    # status = 'Done'  # 完了
    # status = 'To Do'  # To Do
    # status = 'In Progress'  # 進行中
    # issues = jira.search_issues(f'project = {PROJ} and status = "{status}"')
    issues = jira.search_issues(f'project = {Env.project} and '
                                'status != "Done" order by key')

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
