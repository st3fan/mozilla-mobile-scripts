#!/usr/bin/env python3

import os, re
from github import Github # https://github.com/PyGithub/PyGithub

if __name__ == "__main__":
    pattern = re.compile(r"^FNX\d-\d+ ⁃ (.*)$")
    github = Github(os.getenv("GITHUB_ACCESS_TOKEN"))
    repo = github.get_repo("mozilla-mobile/android-components")
    for issue in repo.get_issues(state='open'):
        if match := pattern.search(issue.title):
            issue.edit(title=match[1])