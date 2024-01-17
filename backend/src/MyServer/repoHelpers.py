from MyServer.authHelpers import OAuthProvider, AuthInfo
from MyServer.testHelpers import server_test_mode, TEST_REPOS, TEST_SERVER_REPOS
import git
import os
import csv
from decouple import config


def getReposFromFile() -> dict:
    if server_test_mode():
        return TEST_SERVER_REPOS

    with open("/app/serverRepos.csv", "r") as file:
        reader = csv.reader(file, delimiter=" ")
        repos = {}
        for row in reader:
            repos[row[0]] = row[1]
        return repos


def stageChanges(repoFolderPath: str, message: str, userName: str, userMail) -> bool:
    if server_test_mode():
        return True

    try:
        repo = git.Repo(repoFolderPath)
        repo.git.config('user.name', userName)
        repo.git.config('user.email', userMail)
        repo.git.add(repoFolderPath)
        repo.index.commit(message)
        repo.remote().fetch()
        repo.git.merge(f'origin/{repo.active_branch.name}')
        repo.remote().push()
        return True
    except git.InvalidGitRepositoryError:
        return False
    except git.NoSuchPathError:
        return False
    except OSError:
        return False


def repoName2DirName(repoName: str) -> str:
    return repoName.replace('/', '-')


def getRepoInfo(request) -> tuple[str, str]:
    authInfo: AuthInfo = request.auth
    repoName = request.GET.get('repositoryName')
    userId = authInfo.uid
    repoFolder = repoName2DirName(repoName)
    provider_prefix = authInfo.provider.name.lower()
    return f"{config('REPOS_FOLDER')}/{provider_prefix}/{userId}/{repoFolder}", repoName


def cloneRepo(repoFolder: str, repoUrl, token, provider: OAuthProvider):
    destination = f"{repoFolder}"
    os.makedirs(destination)

    if server_test_mode():
        repo = git.Repo.init(destination)
        return repo

    if provider == OAuthProvider.GITHUB:
        url = f"https://{token}:@{repoUrl}"
    else:
        url = f"https://oauth2:{token}@{repoUrl}.git"
    repo = git.Repo.clone_from(url, destination)
    return repo


def pullRepo(repoFolder: str, token):
    if server_test_mode():
        return

    repo = git.Repo(repoFolder)
    repo.git.update_environment(GIT_TERMINAL_PROMPT='0', GIT_USERNAME='x-access-token', GIT_PASSWORD=token)
    origin = repo.remote()
    origin.pull()


def checkIfExists(repoFolder: str) -> bool:
    return os.path.exists(repoFolder)


def getUserServerRepos(userRepos: list, serverRepos: dict):
    if not userRepos:
        return []
    return [repoName for repoName in userRepos if repoName in serverRepos.keys()]