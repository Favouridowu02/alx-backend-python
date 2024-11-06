#!/usr/bin/env python3
"""
    This Module contains the testcases for the test client
"""
from client import GithubOrgClient
from unittest import TestCase, mock
from parameterized import parameterized, param


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
        """
        expected = {'hi': 'testing'}
        mock_get_json.return_value = expected
        with mock.patch('client.GithubOrgClient._public_repos_url',
                new_callable=mock.PropertyMock) as MockPublic:
            MockPublic.return_value = expected
            mock_get_json()
            test_instance = MockPublic()
            self.assertEqual(test_instance, expected)
            mock_get_json.assert_called_once()
            MockPublic.assert_called_once()
