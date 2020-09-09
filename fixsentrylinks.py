#!/usr/bin/env python3


import contextlib, os
from github import Github # https://github.com/PyGithub/PyGithub


PROJECTS = {
    "fenix": "firefox-nightly",
    "fenix-fennec-beta": "firefox-beta",
    "fenix-fennec": "firefox",
}


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        github = Github(os.getenv("GITHUB_ACCESS_TOKEN"))
        for project in ("android-components", "fenix"):
            for issue in github.get_repo(f"mozilla-mobile/{project}").get_issues(state='all'):
                if updated_body := issue.body:
                    for old, new in PROJECTS.items():
                        updated_body = updated_body.replace(f"sentry.prod.mozaws.net/operations/{old}/", f"sentry.prod.mozaws.net/operations/{new}/")
                    if issue.body != updated_body:
                        issue.edit(body=updated_body)
                        print(f"Updated issue {issue.html_url}")
            for comment in github.get_repo(f"mozilla-mobile/{project}").get_issues_comments():
                if updated_body := comment.body:
                    for old, new in PROJECTS.items():
                        updated_body = updated_body.replace(f"sentry.prod.mozaws.net/operations/{old}/", f"sentry.prod.mozaws.net/operations/{new}/")
                    if comment.body != updated_body:
                        comment.edit(body=updated_body)
                        print(f"Updated comment {comment.html_url}")
