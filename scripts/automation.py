import self as self

print("test from echo file")

import os
import git

# def gitDiff(branch1, branch2):
#     format = '--name-only'
#     commits = []
#     g = git.Git('https://github.com/arnoldmd181/piSandBox')
#     differ = g.diff('%s..%s' % (branch1, branch2), format).split("\n")
#     for line in differ:
#         if len(line):
#             commits.append(line)
#
#     #for commit in commits:
#     #    print '*%s' % (commit)
#     return commits
#
# # repo = versions("/Users/arnold.dajao/Documents/OldTask/Temp/Iron-predict-models-test")
# repo = gitDiff("test", "dev")
#
# print(repo)

# repo = git.Repo("/Users/arnold.dajao/Documents/OldTask/Temp/Iron-predict-models-test")
# # logger.info("repo": repo)
# print("repo" + repo)
# subprocess.check_output(['git', 'diff', '--name-only', currentBranch + '..' + compBranch])

# branch1  = "dev"
# branch2 = "test1"
# g = git.Git('https://github.com/arnoldmd181/piSandBox')
#
# print(g)
#
# format = '--name-only'
# commits = []
# g = git.Git('https://github.com/arnoldmd181/piSandBox')
# # differ = g.diff('%s..%s' % (branch1, branch2), format).split("\n")
# different = g.diff("git diff dev…test1")
# print(different)
# # for line in differ:
# #     if len(line):
# #         print(line)

from git import Repo
from pathlib import Path
import re

# rorepo is a Repo instance pointing to the git-python repository.
# For all you know, the first argument to Repo is a path to the repository
# you want to work with
repo = Repo("/Users/arnold.dajao/Documents/OldTask/Temp/piSandBox")

commit_dev = repo.commit("test1")
commit_origin_dev = repo.commit("origin/dev")
diff_index = commit_origin_dev.diff(commit_dev)

classifiers_updates = set()
classifiers = {"phishing_common", "domain_classifier", "filename_classifier", "path_classifier",
               "tls_certificate_classifier"}

for diff_item in diff_index:
    path = Path(diff_item.a_path).parent
    print("A blob: {} \n".format(path))
    if str(path).lower() in classifiers:
        classifiers_updates.add(path)

FileName = '/Users/arnold.dajao/Documents/OldTask/Temp/piSandBox/domain_classifier/domain_classifier/_version.py'
print(classifiers_updates)

here = os.path.abspath(os.path.dirname("../domain_classifier"))
# exec(open(os.path('../domain_classifier/domain_classifier/_version.py')).read())
# exec(open(os.path.join(here, '/domain_classifier/domain_classifier/_version.py')).read())
exec(
    open('/Users/arnold.dajao/Documents/OldTask/Temp/piSandBox/domain_classifier/domain_classifier/_version.py').read())
version = __version__


def increment_version(version):
    pattern = re.compile("""(\\d\\.\\d\\.)(\\d)(.*)""")
    matches = pattern.match(version)
    new_version = matches.group(1) + str(int(matches.group(2)) + 1) + matches.group(3)
    return new_version


# update dependency version or update _version.py
def update_version_deps(FileName, version, new_version):
    with open(FileName) as f:
        newText = f.read().replace(version, new_version)
    with open(FileName, "w") as f:
        f.write(newText)


new_version = increment_version(FileName)

update_version_deps(FileName, version, new_version)
