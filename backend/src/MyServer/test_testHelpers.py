import unittest
import MyServer.testHelpers as testHelpers
from MyServer.authHelpers import OAuthProvider

class TestTestHelpers(unittest.TestCase):
    def test_init_MockedAuthInfo(self):
        auth_info = testHelpers.MockedAuthInfo(OAuthProvider.GITHUB)
        self.assertEqual(auth_info.provider, OAuthProvider.GITHUB)
        self.assertEqual(auth_info.uid, testHelpers.TEST_UID)
        self.assertEqual(auth_info.token, testHelpers.TEST_TOKEN)
    
    def test_serwer_mode(self):
        result = testHelpers.server_test_mode()
        self.assertFalse(result)
    