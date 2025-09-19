#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient  # the class we’re testing


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org property"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value
        and get_json is called once with the expected URL.
        """
        # mock return value of get_json
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        # instantiate client with org_name
        client = GithubOrgClient(org_name)

        # call the property/method under test
        result = client.org

        # check get_json called with expected URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # check the return value matches mocked payload
        self.assertEqual(result, expected_payload)


if __name__ == "__main__":
    unittest.main()

