"""This module provides functions responsible for integration with git."""

from api.authHelpers import OAuthProvider, AuthInfo
from api.testHelpers import server_test_mode, TEST_SERVER_REPOS
import git
import os
import csv
from decouple import config
import api.error


def get_repos_from_file() -> dict:
    """Load server repositories from config file.\n
    Returns: dict[repo_name: repo_url]"""
    if server_test_mode():
        return TEST_SERVER_REPOS

    with open("/app/serverRepos.csv", "r") as file:
        reader = csv.reader(file, delimiter=" ")
        repos = {}
        for row in reader:
            repos[row[0]] = row[1]
        return repos


def stage_changes(repo_folder_path: str, message: str, user_name: str, user_mail) -> bool:
    """Commit changes in given repo whith given message and push it to remote.\n"""
    if server_test_mode():
        return True

    try:
        repo = git.Repo(repo_folder_path)
        repo.git.config('user.name', user_name)
        repo.git.config('user.email', user_mail)
        repo.git.add(repo_folder_path)
        repo.index.commit(message)
        fetch_info = repo.remote().fetch()
        for info in fetch_info:
            if info.flags == info.REJECTED:
                raise api.error.FetchRejectedException()
        try:
            repo.git.merge(f'origin/{repo.active_branch.name}')
        except git.GitCommandError:
            raise api.error.MergeRejectedException(f"Merge was rejected after fetching results from remote repo.")
        push_info = repo.remote().push()
        try:
            push_info.raise_if_error()
        except Exception:
            raise api.error.PushRejectedException(f"Push operation resulted in conflicts.")
        return True
    except git.InvalidGitRepositoryError:
        return False
    except git.NoSuchPathError:
        return False
    except OSError:
        return False


def repo_name_to_dir_name(repo_name: str) -> str:
    """Get name of repository directory on server from repo's name."""
    return repo_name.replace('/', '-')


def get_repo_info(request) -> tuple[str, str]:
    """Get repo's directory and name.\n
    Returns: tuple[repo directory name, repo name]"""
    auth_info: AuthInfo = request.auth
    repo_name = request.GET.get('repositoryName')
    user_id = auth_info.uid
    repo_folder = repo_name_to_dir_name(repo_name)
    provider_prefix = auth_info.provider.name.lower()
    return f"{config('REPOS_FOLDER')}/{provider_prefix}/{user_id}/{repo_folder}", repo_name


def clone_repo(repo_folder: str, repo_url, token, provider: OAuthProvider):
    """Clone repo from given url"""
    destination = f"{repo_folder}"
    os.makedirs(destination)

    if server_test_mode():
        repo = git.Repo.init(destination + "/req")
        return repo

    if provider == OAuthProvider.GITHUB:
        url = f"https://{token}:@{repo_url}"
    else:
        url = f"https://oauth2:{token}@{repo_url}.git"
    try:
        repo = git.Repo.clone_from(url, destination)
    except git.GitCommandError:
        raise api.error.CloneRejectedException(f"Clone was rejected.")
    # ensure /req exists
    os.makedirs(f"{destination}/req", exist_ok=True)
    return repo


def pull_repo(repo_folder: str, token):
    """Pull repo from give url"""
    if server_test_mode():
        return

    repo = git.Repo(repo_folder)
    repo.git.update_environment(GIT_TERMINAL_PROMPT='0', GIT_USERNAME='x-access-token', GIT_PASSWORD=token)
    origin = repo.remote()
    pull_info = origin.pull()
    for info in pull_info:
        if info.flags == info.REJECTED:
            raise api.error.PullRejectedException("Pull was rejected.")


def check_if_exists(repo_folder: str) -> bool:
    """Check if repo folder exists on server."""
    return os.path.exists(repo_folder)


def get_user_server_repos(user_repos: list, server_repos: dict):
    """Get user's repos list and return list of those which are also in server's config file."""
    if not user_repos:
        return []
    return [repoName for repoName in user_repos if repoName in server_repos.keys()]
