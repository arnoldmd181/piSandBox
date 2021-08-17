import os
from git import Repo
import re

# import logging
# from phishing_common.logger import LOGGER_NAME, initialize_logging

# logger = logging.getLogger(LOGGER_NAME)

PWD = os.path.abspath(os.path.dirname(__file__))
MAIN_REPO = "origin/dev"
CLASSIFIERS = {"phishing_common", "domain_classifier", "filename_classifier", "path_classifier",
               "tls_certificate_classifier"}  # TODO does need to be in config file?
EXCLUSIONS = {"readme.md"}  # needs to be in lower case TODO does need to be in config file?


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
        CLASSIFIERS.remove("phishing_common")
        for classifier_setup in CLASSIFIERS:
            setup_file = PWD + f'/{classifier_setup}/setup.py'
            update_version_deps(setup_file, version, new_version)
    elif update_classifier == "domain_classifier":
        setup_file = PWD + f'/tls_certificate_classifier/setup.py'
        update_version_deps(setup_file, version, new_version)


if __name__ == "__main__":
    # initialize_logging()

    repo = Repo("/Users/arnold.dajao/Documents/OldTask/Temp/piSandBox")  # TODO get from variables
    o = repo.remotes.origin
    o.pull()

    commit_dev = repo.commit("test1")  # TODO get from variables
    commit_origin_dev = repo.commit(MAIN_REPO)
    diff_index = commit_origin_dev.diff(commit_dev)

    classifiers_updates = set()

    for diff_item in diff_index:
        # path = Path(diff_item.a_path).parent
        full_filename = diff_item.a_path
        path_changed = re.split(r'\/', full_filename)[0].lower()
        file_changed = re.split(r'\/', full_filename)[-1].lower()
        print(f"file updated: {full_filename}")
        # if str(file_changed) == "_version.py":
        #     # logger.fatal("_version.py was changed")
        #     print("_version.py was changed")
        #     exit(1)
        if str(path_changed) in CLASSIFIERS and str(file_changed) not in EXCLUSIONS:
            print(f"file added: {full_filename}")
            classifiers_updates.add(path_changed)

    if classifiers_updates:

        for classifier in classifiers_updates:
            print(classifier)  # TODO Remove

            version_file = PWD + f'/{classifier}/{classifier}/_version.py'
            # Read Version file
            exec(open(version_file).read())

            current_version = __version__
            # update version
            new_version_incr = increment_version(current_version)

            update_version_classifiers(version_file, current_version, new_version_incr, classifier)
    else:
        # logger.warning("No version update needed")
        print("No version update needed")
