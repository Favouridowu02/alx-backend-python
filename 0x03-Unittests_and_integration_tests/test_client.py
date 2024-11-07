#!/usr/bin/env python3
"""
    This Module contains the testcases for the test client
"""
from client import GithubOrgClient
from unittest import TestCase, mock
from parameterized import parameterized, param, parameterized_class
from fixtures import TEST_PAYLOAD

class TestGithubOrgClient(TestCase):
    """
        This class contains the test cases for the GithibOrgClient claass
    """
    @parameterized.expand([
        ('google'),
        ('abc'),
    ])
    @mock.patch('client.get_json')
    def test_org(self, org, mocked_org):
        """This is a test Method
        """
        test_object = GithubOrgClient(org)
        test_object.org()
        test_object.public_repos()

        mocked_org.called_once_with(f"https://api.github.com/orgs/{org}")

    def test_public_repos_url(self):
        """
            Test that the result of _public_repos_url
            return the correct value based on the given payload
        """
        with mock.patch('client.GithubOrgClient.org',
                        new_callable=mock.PropertyMock) as MockPublic:
            expected = {'hi': 'testing'}
            MockPublic.return_value = expected
            test_instance = MockPublic()
            self.assertEqual(test_instance, expected)

    @mock.patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
            Test to unit-test GithubOrgClient.public_repos
            Test that the list of repos is what you expect from
            the chosen payload.
            Test that the mocked property and the mocked get_json
            was called once.
        """
        expected = [{'name': 'testing'}]
        mock_get_json.return_value = expected
        with mock.patch('client.GithubOrgClient._public_repos_url',
                        new_callable=mock.PropertyMock) as MockPublic:
            MockPublic.return_value = "hi"
            test_instance = GithubOrgClient('test')
            result = test_instance.public_repos()

            self.assertEqual(result, [expected[0]["name"]])
            MockPublic.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """
            Thus test is to test the GithubOrgClient.has_license
       """
        test_instance = GithubOrgClient('test')
        result = test_instance.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(TestCase):
    """
        This module contains the Integration test cases for the fixtures
    """
    @classmethod
    def setUpClass(cls):
        """
            This is the setupClass method.
            This is the method that would be run before any tests in
            this class would be ran
        """
        config = {'return_value.json.side_effect':
                [
                    cls.org_payload, cls.repos_payload,
                    cls.org_payload, cls.repos_payload
                ]
                }
        cls.get_patcher = mock.patch('requests.get', **config)
        cls.mock = self.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """This is the teardown method for the class"""
        cls.get_patcher.stop()
