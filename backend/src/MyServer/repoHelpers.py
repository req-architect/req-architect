from MyServer.authHelpers import OAuthProvider, AuthInfo
import git
import os
import csv
from decouple import config
import MyServer.error


class ConflictDetector(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if 'CONFLICT' in message:
            print("Merge resulted in conflicts")
            # Dodatkowo, możesz wydobyć informacje o konfliktach
            # z e.message, na przykład:
            # print(message)


def getReposFromFile() -> dict:
    with open("/app/serverRepos.csv", "r") as file:
        reader = csv.reader(file, delimiter=" ")
        repos = {}
        for row in reader:
            repos[row[0]] = row[1]
        return repos


def checkGitOperationStatus(operationState: git.RemoteProgress):
    pass


def stageChanges(repoFolderPath: str, message: str, userName: str, userMail) -> bool:
    try:
        repo = git.Repo(repoFolderPath)
        repo.git.config('user.name', userName)
        repo.git.config('user.email', userMail)
        repo.git.add(repoFolderPath)
        repo.index.commit(message)
        fetchInfo = repo.remote().fetch()
        for info in fetchInfo:
            if info.REJECTED:
                raise MyServer.error.FetchRejectedException()
        try:
            repo.git.merge(f'origin/{repo.active_branch.name}')
        except git.GitCommandError:
            raise MyServer.error.MergeRejectedException(f"Merge was rejected after fetching results from remote repo.")
        # pullInfo = repo.remote().pull()
        # for info in pullInfo:
        #     if info.REJECTED:
        #         raise MyServer.error.PullRejectedException("Pull was rejected.") 
        pushInfo = repo.remote().push()
        try:
            pushInfo.raise_if_error()
        except Exception:
            raise MyServer.error.PushRejectedException(f"Push operation resulted in conflicts.")
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
    if provider == OAuthProvider.GITHUB:
        url = f"https://{token}:@{repoUrl}"
    else:
        url = f"https://oauth2:{token}@{repoUrl}.git"
    os.makedirs(destination)
    try:
        repo = git.Repo.clone_from(url, destination)
    except git.GitCommandError:
        raise MyServer.error.CloneRejectedException(f"Clone was rejected.")
    return repo


def pullRepo(repoFolder: str, token):
    repo = git.Repo(repoFolder)
    repo.git.update_environment(GIT_TERMINAL_PROMPT='0', GIT_USERNAME='x-access-token', GIT_PASSWORD=token)
    origin = repo.remote()
    pullInfo = origin.pull()
    for info in pullInfo:
        if info.REJECTED:
            raise MyServer.error.PullRejectedException("Pull was rejected.")


def checkIfExists(repoFolder: str) -> bool:
    return os.path.exists(repoFolder)
