from MyServer.authHelpers import OAuthProvider
import git


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
    

def removeFromRepo(userFolder: str, targetPath: str) -> bool:
    """Probably unnessesery for later"""
    try:
        repo = git.Repo(userFolder)
        repo.index.remove([targetPath])
        return True
    except git.InvalidGitRepositoryError:
        return False
    except git.NoSuchPathError:
        return False
    

def commitAndPush(userFolder: str, message: str) -> bool:
    try:
        repo = git.Repo(userFolder)
        repo.index.commit(message)
        repo.remote().push()
        return True
    except git.InvalidGitRepositoryError:
        return False
    except git.NoSuchPathError:
        return False


def getUserFolderName(uid: str, provider: OAuthProvider) -> str:
    prefix = "github" if provider == OAuthProvider.GITHUB else "gitlab"
    return f"{prefix}-{uid}"
