from MyServer.authHelpers import OAuthProvider
import git
import os
import csv


def getReposFromFile() -> dict:
    with open("/app/serverRepos.csv", "r") as file:
        reader = csv.reader(file, delimiter=" ")
        repos = {}
        for row in reader:
            repos[row[0]] = row[1]
        return repos


def stageChanges(repoFolderPath: str, message: str, userName: str) -> bool:
    try:
        repo = git.Repo(repoFolderPath)
        repo.git.config('user.name', userName)
        repo.git.add(repoFolderPath)
        repo.index.commit(message)
        repo.remote().push()
        return True
    except git.InvalidGitRepositoryError:
        return False
    except git.NoSuchPathError:
        return False
    except OSError:
        return False


def getUserFolderName(uid: str, provider: OAuthProvider) -> str:
    prefix = "github" if provider == OAuthProvider.GITHUB else "gitlab"
    return f"{prefix}-{uid}"


def repoName2DirName(userFolder: str, repoName: str) -> str:
    return f"{userFolder}/{repoName.replace('/', '-')}"


def getRepoInfo(usersFolder: str, request) -> tuple[str, str]:
    repoName = request.GET.get('repositoryName')
    userFolder = getUserFolderName(request.auth.uid, request.auth.provider)
    repoFolder = repoName2DirName(userFolder, repoName)
    return f"{usersFolder}/{repoFolder}", repoName


def cloneRepo(repoFolder: str, repoUrl, token):
    destination = f"{repoFolder}"
    url = f"https://{token}:@{repoUrl}"
    os.makedirs(destination)
    repo = git.Repo.clone_from(url, destination)
    return repo


def pullRepo(repoFolder: str, token):
    repo = git.Repo(repoFolder)
    repo.git.update_environment(GIT_TERMINAL_PROMPT='0', GIT_USERNAME='x-access-token', GIT_PASSWORD=token)
    origin = repo.remote()
    origin.pull()


def checkIfExists(repoFolder: str) -> bool:
    if os.path.exists(repoFolder):
        return True
    return False