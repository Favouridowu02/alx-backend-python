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
