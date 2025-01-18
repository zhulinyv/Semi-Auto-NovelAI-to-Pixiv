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
from utils.utils import logger, proxies


def check_update(repo="zhulinyv/Semi-Auto-NovelAI-to-Pixiv", path=Path().absolute()):
    logger.info("正在检查 {} 版本更新...".format(repo.split("/")[-1]))
    if env.skip_update_check:
        return ""
    try:
        data = requests.get(f"https://api.github.com/repos/{repo}/commits", proxies=proxies).json()
    except Exception:
        logger.error("更新检查失败! 请检查网络连接")
        return "Version: Error  网络连接失败"
    try:
        local_repo = git.Repo(path)
    except InvalidGitRepositoryError:
        logger.warning("更新检查失败! 非 GIT 安装")
        return "Version: Error  不是GIT仓库"
    local_commit = local_repo.head.commit
    remote_commit = []
    try:
        for commit in data:
            if str(local_commit) == commit["sha"]:
                break
            remote_commit.append(commit)
    except Exception:
        logger.warning("更新检查失败! 请检查网络连接")
        return "Version: Error  更新检查失败"
    if not remote_commit:
        logger.success("{} 已是最新!".format(repo.split("/")[-1]))
        return "Version: [{}](https://github.com/{}/commit/{})".format(VERSION, repo, str(local_commit))
    logger.warning("{} 更新可用".format(repo.split("/")[-1]))
    return "Version: [{}](https://github.com/{}/commit/{})  Older Version | 更新可用".format(
        str(local_commit)[:7], repo, str(local_commit)
    )


def update(path):
    repo = git.Repo(path)
    repo.git.pull()
    return "更新完成! 重启后生效"
