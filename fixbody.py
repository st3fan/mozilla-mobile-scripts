#!/usr/bin/env python3

import os, re
from github import Github # https://github.com/PyGithub/PyGithub

PATTERN = re.compile(r"^┆Issue is synchronized with this \[Jira Task\]\(https://jira.mozilla.com/browse/FNX\d-\d+\)$", re.MULTILINE)

if __name__ == "__main__":
    github = Github(os.getenv("GITHUB_ACCESS_TOKEN"))
    for issue in github.get_repo("mozilla-mobile/android-components").get_issues(state='open'):
        if match := PATTERN.search(issue.body):
            print(f"{issue.number} - {issue.title}")
            updated_body = PATTERN.sub("", issue.body)
            issue.edit(body=updated_body)