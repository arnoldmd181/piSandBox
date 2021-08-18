import os
from git import Repo
import re
import argparse

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
    print("Running Automation Deployment")
    # initialize_logging()

    #initialized github creds
    os.system("git config --global user.name \"Arnold Dajao\"")
    os.system("git config --global user.email \"arnold.dajao@ironnetcybersecurity.com\"")

    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', type=str, required=True)
    parser.add_argument('--branch', type=str, required=True)
    # parser.add_argument('-w', '--workspace', dest="config_file")
    args = parser.parse_args()

    branch = args.branch  # TODO get from variables
    origin_branch = f'origin/{branch}'
    repo = Repo(args.workspace)  # TODO get from variables
    o = repo.remotes.origin
    # pull all origin
    o.pull()

    commit_origin_dev = repo.commit(MAIN_REPO)
    # repo_branches = repo.heads #r.heads  # or it's alias: r.branches
    # repo_heads_names = [h.name for h in repo_branches]
    print("remote branches")
    remote_refs = repo.remote().refs

    for refs in remote_refs:
        print(refs.name)

    print(f'getting commit_dev')
    commit_dev = repo.commit(origin_branch)

    diff_index = commit_origin_dev.diff(commit_dev)

    classifiers_updates = set()

    # repo.git.checkout(origin_branch)
    print("checkout branch:")
    repo.git.branch('"dc-test"')
    for diff_item in diff_index:
        # path = Path(diff_item.a_path).parent
        full_filename = diff_item.a_path
        path_changed = re.split(r'\/', full_filename)[0].lower()
        file_changed = re.split(r'\/', full_filename)[-1].lower()
        print(f"file updated: {full_filename}")
        if str(file_changed) == "_version.py":
            # logger.fatal("_version.py was changed")
            print("_version.py was changed")
            exit(-1)
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

        ver_changes_changes = ', '.join(classifiers_updates)
        repo_commit_message = f'automation updated versions for {ver_changes_changes}'

        try:

            repo.git.add(update=True)
            repo.git.commit(m=repo_commit_message)
            repo.git.push("origin", "Head:dc-test")
            # origin = repo.remote(name='origin/dc-test')
            # origin.push()
            # repo.git.checkout(origin_branch)
            # repo.remotes.origin.push()

        except Exception as e:
            # logger.warning(f'Failed to read ETDR password so pymysql will not be set up correctly\n{e}')
            print(f'Failed to read push to remote \n{e}')
            exit(-1)
    else:
        # logger.warning("No version update needed")
        print("No version update needed")
