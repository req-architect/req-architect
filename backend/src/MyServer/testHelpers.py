import os


TEST_UID = "test_uid"
TEST_TOKEN = "test_token"
TEST_MAIL = "test_mail"
TEST_USERNAME = "test_user"
TEST_REPOS = ["test_repo_1", "test_repo_2"]
TEST_SERVER_REPOS = {
    TEST_REPOS[0]: "url_1",
    TEST_REPOS[1]: "url_2"
}


class MockedAuthInfo:
    def __init__(self, provider) -> None:
        self.provider = provider
        self.uid = TEST_UID
        self.token = TEST_TOKEN


def server_test_mode() -> bool:
    return os.environ.get("SERVER_TEST_MODE") == '1'
