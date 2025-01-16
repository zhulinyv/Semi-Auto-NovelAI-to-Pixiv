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


def check_update(repo="zhulinyv/Semi-Auto-NovelAI-to-Pixiv", path=Path().absolute()):
    if env.skip_update_check:
        return ""
    try:
        data = requests.get(f"https://api.github.com/repos/{repo}/commits", proxies=proxies).json()
    except Exception:
        return "Version: Error  网络连接失败"
    try:
        local_repo = git.Repo(path)
    except InvalidGitRepositoryError:
        return "Version: Error  不是GIT仓库"
    local_commit = local_repo.head.commit
    remote_commit = []
    try:
        for commit in data:
            if str(local_commit) == commit["sha"]:
                break
            remote_commit.append(commit)
    except Exception:
        return "Version: Error  更新检查失败"
    if not remote_commit:
        return "Version: [{}](https://github.com/{}/commit/{})".format(VERSION, repo, str(local_commit))
    return "Version: [{}](https://github.com/{}/commit/{})  Older Version | 更新可用".format(
        str(local_commit)[:7], repo, str(local_commit)
    )


def update(path):
    repo = git.Repo(path)
    repo.git.pull()
    return "更新完成! 重启后生效"
