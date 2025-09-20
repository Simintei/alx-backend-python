#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient  # the class we're testing


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
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"}

        # Patch 'org' property using PropertyMock
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
                mock_org.return_value = mock_payload
                result = client._public_repos_url
                self.assertEqual(result, 
                    "https://api.github.com/orgs/testorg/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Unit-test GithubOrgClient.public_repos."""
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        client = GithubOrgClient("testorg")

        # Patch _public_repos_url property using PropertyMock
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_repos_url:
                mock_repos_url.return_value = "fake_url"
                repos = client.public_repos()

            # Assert the list of repo names matches expected
                self.assertEqual(
                    [repo["name"] for repo in mock_get_json.return_value],
                    ["repo1", "repo2"]
                )

            # Ensure mocks called once
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once()


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient."""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the correct boolean."""
        client = GithubOrgClient("testorg")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
