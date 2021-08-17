import os
from git import Repo
from pathlib import Path
import re

PWD = os.path.abspath(os.path.dirname(__file__))
MAIN_REPO = "origin/dev"
CLASSIFIERS = {"phishing_common", "domain_classifier", "filename_classifier", "path_classifier",
               "tls_certificate_classifier"}  # TODO does need to be in config file?


def increment_version(version):
    pattern = re.compile("""(\\d\\.\\d\\.)(\\d)(.*)""")
    matches = pattern.match(version)
    return matches.group(1) + str(int(matches.group(2)) + 1) + matches.group(3)


# update dependency version or update _version.py
def update_version_deps(file_name, version, new_version):
    with open(file_name) as f:
        new_text = f.read().replace(version, new_version)
    with open(file_name, "w") as f:
        f.write(new_text)


# pattern matching similar to scala is only available in 3.10
def update_version_classifiers(file_name, version, new_version, update_classifier):
    update_version_deps(file_name, version, new_version)

    if update_classifier == "phishing_common":
        for classifier_setup in CLASSIFIERS.pop():
            setup_file = PWD + f'/{classifier_setup}/setup.py'
            update_version_deps(setup_file, version, new_version)
    elif update_classifier == "domain_classifier":
        setup_file = PWD + f'/tls_certificate_classifier/setup.py'
        update_version_deps(setup_file, version, new_version)


repo = Repo("/Users/arnold.dajao/Documents/OldTask/Temp/piSandBox")  # TODO get from variables

commit_dev = repo.commit("test1")  # TODO get from variables
commit_origin_dev = repo.commit(MAIN_REPO)
diff_index = commit_origin_dev.diff(commit_dev)

classifiers_updates = set()

for diff_item in diff_index:
    path = Path(diff_item.a_path).parent
    if str(path).lower() in CLASSIFIERS:
        classifiers_updates.add(path)

for classifier in classifiers_updates:
    print(classifier)

    version_file = PWD + f'/{classifier}/{classifier}/_version.py'
    # Read Version file
    exec(open(version_file).read())

    current_version = __version__
    # update version
    new_version_incr = increment_version(current_version)

    update_version_classifiers(version_file, current_version, new_version_incr, classifier)
