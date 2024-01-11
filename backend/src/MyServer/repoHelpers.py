from MyServer.authHelpers import OAuthProvider


def getUserFolderName(uid: str, provider: OAuthProvider) -> str:
    prefix = "github" if provider == OAuthProvider.GITHUB else "gitlab"
    return f"{prefix}-{uid}"