from pathlib import Path

import git
import requests
from git.exc import InvalidGitRepositoryError

from utils.utils import read_txt


def check_update():
    resp = requests.get("https://api.github.com/repos/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/commits")
    data = resp.json()
    if not isinstance(data, list):
        return "Version: xxxxxxx  Error | 检查失败"
    try:
        repo = git.Repo(Path().absolute())
    except InvalidGitRepositoryError:
        return "Version: xxxxxxx  Error | 检查失败"
    local_commit = repo.head.commit
    for commit in data:
        if commit["sha"] == str(local_commit):
            version = read_txt("VERSION")
            return "Version: [{}](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/commit/{})".format(
                version, str(local_commit)
            )
    return "Version: [{}](https://github.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/commit/{})  Older Version | 更新可用".format(
        str(local_commit)[:7], str(local_commit)
    )
