import os


class MockedAuthInfo:
    def __init__(self, provider) -> None:
        self.provider = provider
        self.uid = "fake_user"
        self.token = "fake_token"


def server_test_mode() -> bool:
    return os.environ.get("SERVER_TEST_MODE") == 1
