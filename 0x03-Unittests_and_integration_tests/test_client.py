#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient  # the class we’re testing


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value."""
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
    """Unit-test GithubOrgClient._public_repos_url."""
    client = GithubOrgClient("testorg")
    mock_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}

    # Patch 'org' as a property with return value
    with patch.object(
        GithubOrgClient, "org", new_callable=property, return_value=mock_payload
    ):
        result = client._public_repos_url
        self.assertEqual(
            result, "https://api.github.com/orgs/testorg/repos"
        )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Unit-test GithubOrgClient.public_repos."""
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload
        client = GithubOrgClient("testorg")

    # Patch '_public_repos_url' property with return value
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=property, return_value="fake_url"
        ):
            result = client.public_repos
            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once()

if __name__ == "__main__":
    unittest.main()
