"""jiratools
"""
import re
import datetime
import dataclasses


DEFAULT_ENV_FILE = 'env.txt'    # デフォルトの環境設定ファイル


EnvData = None


@dataclasses.dataclass
class Env:
    http_proxy: str = ''
    https_proxy: str = ''
    token: str = ''
    email: str = ''
    url: str = ''
    project: str = ''
    start_field: str = ''
    due_field: str = ''

    @staticmethod
    def get_param(line):
        return re.sub('^[a-zA-Z_]+: ', '', line.rstrip())

    @staticmethod
    def open(envfile=DEFAULT_ENV_FILE):
        global EnvData
        http_proxy = ''
        https_proxy = ''
        token = ''
        email = ''
        url = ''
        project = ''
        start_field = ''
        due_field = ''
        with open(envfile, 'r') as f:
            for line in f.readlines():
                if re.match(r'^http_proxy: ', line):
                    http_proxy = Env.get_param(line)
                elif re.match(r'^https_proxy: ', line):
                    https_proxy = Env.get_param(line)
                elif re.match(r'^token: ', line):
                    token = Env.get_param(line)
                elif re.match(r'^email: ', line):
                    email = Env.get_param(line)
                elif re.match(r'^url: ', line):
                    url = Env.get_param(line)
                elif re.match(r'^project: ', line):
                    project = Env.get_param(line)
                elif re.match(r'^start_field: ', line):
                    start_field = Env.get_param(line)
                elif re.match(r'^due_field: ', line):
                    due_field = Env.get_param(line)

        # 環境設定ファイル
        EnvData = Env(https_proxy, http_proxy, token, email, url, project,
                      start_field, due_field)
        return EnvData


# issue utilities

def get_start_date(issue):
    start_date = None
    if hasattr(issue.fields, EnvData.start_field):
        date_str = getattr(issue.fields, EnvData.start_field)
        if date_str:
            start_date = datetime.date.fromisoformat(date_str)

    return start_date


def get_due_date(issue):
    due_date = None
    if hasattr(issue.fields, EnvData.due_field):
        date_str = getattr(issue.fields, EnvData.due_field)
        if date_str:
            due_date = datetime.date.fromisoformat(date_str)

    return due_date


if __name__ == '__main__':
    env = Env.open()
    print(env.http_proxy)
    print(env.https_proxy)
    print(env.token)
    print(env.email)
    print(env.url)
    print(env.project)
    print(env.start_field)
    print(env.due_field)
