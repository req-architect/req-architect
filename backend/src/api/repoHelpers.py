"""This module provides functions responsible for integration with git."""

from api.authHelpers import OAuthProvider, AuthInfo
from api.testHelpers import server_test_mode, TEST_SERVER_REPOS
import git
import os
import csv
from decouple import config
import api.error


def getReposFromFile() -> dict:
    """Load server repositories from conig file.\n
    Returns: dict[repo_name: repo_url]"""
    if server_test_mode():
        return TEST_SERVER_REPOS

    with open("/app/serverRepos.csv", "r") as file:
        reader = csv.reader(file, delimiter=" ")
        repos = {}
        for row in reader:
            repos[row[0]] = row[1]
        return repos


def stageChanges(repoFolderPath: str, message: str, userName: str, userMail) -> bool:
    """Commit changes in given repo whith given message and push it to remote.\n"""
    if server_test_mode():
        return True

    try:
        repo = git.Repo(repoFolderPath)
        repo.git.config('user.name', userName)
        repo.git.config('user.email', userMail)
        repo.git.add(repoFolderPath)
        repo.index.commit(message)
        fetchInfo = repo.remote().fetch()
        for info in fetchInfo:
            if info.flags == info.REJECTED:
                raise api.error.FetchRejectedException()
        try:
            repo.git.merge(f'origin/{repo.active_branch.name}')
        except git.GitCommandError:
            raise api.error.MergeRejectedException(f"Merge was rejected after fetching results from remote repo.")
        pushInfo = repo.remote().push()
        try:
            pushInfo.raise_if_error()
        except Exception:
            raise api.error.PushRejectedException(f"Push operation resulted in conflicts.")
        return True
    except git.InvalidGitRepositoryError:
        return False
    except git.NoSuchPathError:
        return False
    except OSError:
        return False


def repoName2DirName(repoName: str) -> str:
    """Get name of repository direcory on server from repo's name."""
    return repoName.replace('/', '-')


def getRepoInfo(request) -> tuple[str, str]:
    """Get repo's directory and name.\n
    Returns: tuple[repo directory name, repo name]"""
    authInfo: AuthInfo = request.auth
    repoName = request.GET.get('repositoryName')
    userId = authInfo.uid
    repoFolder = repoName2DirName(repoName)
    provider_prefix = authInfo.provider.name.lower()
    return f"{config('REPOS_FOLDER')}/{provider_prefix}/{userId}/{repoFolder}", repoName


def cloneRepo(repoFolder: str, repoUrl, token, provider: OAuthProvider):
    """Clone repo from given url"""
    destination = f"{repoFolder}"
    os.makedirs(destination)

    if server_test_mode():
        repo = git.Repo.init(destination + "/req")
        return repo

    if provider == OAuthProvider.GITHUB:
        url = f"https://{token}:@{repoUrl}"
    else:
        url = f"https://oauth2:{token}@{repoUrl}.git"
    try:
        repo = git.Repo.clone_from(url, destination)
    except git.GitCommandError:
        raise api.error.CloneRejectedException(f"Clone was rejected.")
    # ensure /req exists
    os.makedirs(f"{destination}/req", exist_ok=True)
    return repo


def pullRepo(repoFolder: str, token):
    """Pull repo from give url"""
    if server_test_mode():
        return

    repo = git.Repo(repoFolder)
    repo.git.update_environment(GIT_TERMINAL_PROMPT='0', GIT_USERNAME='x-access-token', GIT_PASSWORD=token)
    origin = repo.remote()
    pullInfo = origin.pull()
    for info in pullInfo:
        if info.flags == info.REJECTED:
            raise api.error.PullRejectedException("Pull was rejected.")


def checkIfExists(repoFolder: str) -> bool:
    """Check if repo folder exists on server."""
    return os.path.exists(repoFolder)


def getUserServerRepos(userRepos: list, serverRepos: dict):
    """Get user's repos list and return list of those which are also in server's config file."""
    if not userRepos:
        return []
    return [repoName for repoName in userRepos if repoName in serverRepos.keys()]
