import sys
import requests
import json
import jiratools as jt


ENV_FILE = 'env.txt'


Env = jt.Env.open(ENV_FILE)


def main(issue_key):
    url = Env.url + '/rest/api/3/issue/' + issue_key
    response = requests.get(url,
                            auth=(Env.email, Env.token))
    print(json.dumps(json.loads(response.text),
                     sort_keys=True, indent=4,
                     separators=(',', ': '),
                     ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(f'Usage: python {sys.argv[0]} <ISSUE_KEY>')
        exit()

    main(sys.argv[1])
