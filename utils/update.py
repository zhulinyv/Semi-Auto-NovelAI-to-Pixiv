import os
from pathlib import Path

try:
    import git
except Exception:
    os.environ["PATH"] = os.path.abspath("./Git23921/bin")
    import git

import requests
from git.exc import InvalidGitRepositoryError

from utils.env import env
from utils.prepare import VERSION
from utils.utils import proxies


def check_update():
    if env.skip_update_check:
        return ""
    try:
        data = requests.get(
            "https://api.github.com/repos/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/commits", proxies=proxies
        ).json()
    except Exception:
        return "Version: Error  网络连接失败"
    try:
        repo = git.Repo(Path().absolute())
    except InvalidGitRepositoryError:
        return "Version: Error  不是GIT仓库"
    local_commit = repo.head.commit
    remote_commit = []
    try:
        for commit in data:
            if str(local_commit) == commit["sha"]:
                break
            remote_commit.append(commit)
    except Exception:
        return "Version: Error  更新检查失败"
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
