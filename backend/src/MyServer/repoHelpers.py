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


def getRepoFolder(usersFolder: str, request) -> str:
    repoName = request.GET.get('repositoryName')
    userFolder = getUserFolderName(request.auth.uid, request.auth.provider)
    repoFolder = repoName2DirName(userFolder, repoName)
    return f"{usersFolder}/{repoFolder}"


def cloneRepo(usersFolder: str, request):
    repoFolder = getRepoFolder(usersFolder, request)
    os.makedirs(repoFolder)
    url = f"https://{request.auth.token}:@github.com/XarakBendardo/pzsp2-test.git"
    repo = git.Repo.clone_from(url, repoFolder)
    return repo