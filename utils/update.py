from pathlib import Path

import git
import requests
from git.exc import InvalidGitRepositoryError

from utils.env import env
from utils.prepare import VERSION
from utils.utils import proxies


def check_update():
    if env.skip_update_check:
        return ""
    data = requests.get(
        "https://api.github.com/repos/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/commits", proxies=proxies
    ).json()
    if not isinstance(data, list):
        return "Version: xxxxxxx  Error | 检查失败"
    try:
        repo = git.Repo(Path().absolute())
    except InvalidGitRepositoryError:
        return "Version: xxxxxxx  Error | 检查失败"
    local_commit = repo.head.commit
    remote_commit = []
    for commit in data:
        if str(local_commit) == commit["sha"]:
            break
        remote_commit.append(commit)
    if not remote_commit:
        return "Version: [{}](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/commit/{})".format(
            VERSION, str(local_commit)
        )
    return "Version: [{}](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/commit/{})  Older Version | 更新可用".format(
        str(local_commit)[:7], str(local_commit)
    )


def update(path):
    repo = git.Repo(path)
    repo.git.pull()
    return "更新完成! 重启后生效"
