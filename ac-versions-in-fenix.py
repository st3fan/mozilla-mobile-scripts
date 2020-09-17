#!/usr/bin/env python3


import os, re
from github import Github # https://github.com/PyGithub/PyGithub


def parse_ac_version(src):
    """Parse the Android-Components version out of the AndroidComponents.kt file."""
    if match := re.compile(r'VERSION = "([^"]*)"', re.MULTILINE).search(src):
        return match[1]


if __name__ == "__main__":
    repo = Github(os.getenv("GITHUB_ACCESS_TOKEN")).get_repo("mozilla-mobile/fenix")
    for release in repo.get_releases():
        try:
            content_file = repo.get_contents("buildSrc/src/main/java/AndroidComponents.kt", ref=release.tag_name)
            if version := parse_ac_version(content_file.decoded_content.decode('utf8')):
                print(release.tag_name, "=>", version)
        except Exception as e:
            print(release.tag_name, "=>", "FAILED:", str(e))


