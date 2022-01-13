from typing import Union

from external_services.github import GitHubOrganizationProvider
from external_services.twitter import FollowEachOtherProvider


class ConnectedException(Exception):
    """Exceptions for fully connected algorithm"""

    pass


def check_unexpected_errors(
    providers: list[Union[GitHubOrganizationProvider, FollowEachOtherProvider]]
):
    for provider in providers:
        if provider.unexpected_error:
            raise ConnectedException(
                "An Unexpected error ocurred while trying to check if both developers are fully connected"
            )


def are_fully_connected(
    dev1OrgProvider: GitHubOrganizationProvider,
    dev1FollowProvider: FollowEachOtherProvider,
    dev2OrgProvider: GitHubOrganizationProvider,
    dev2FollowProvider: FollowEachOtherProvider,
):

    check_unexpected_errors(
        [
            dev1OrgProvider,
            dev1FollowProvider,
            dev2OrgProvider,
            dev1FollowProvider,
        ]
    )

    account_errors = []

    if not dev1OrgProvider.account_exits:
        account_errors.append("{dev1} is not a valid user in github")
    if not dev2OrgProvider.account_exits:
        account_errors.append("{dev2} is not a valid user in github")

    if not dev1FollowProvider.account_exits:
        account_errors.append("{dev1} is not a valid user in twitter")
    if not dev2FollowProvider.account_exits:
        account_errors.append("{dev2} is not a valid user in twitter")

    # if one account doesn't exist, they cannot be fully connected
    if len(account_errors) != 0:
        return {"connected": False, "errors": account_errors}

    # Github

    dev1_organizations = dev1OrgProvider.get_organizations()
    # login is name. we assume that they are in the same organization using the name
    dev1_organization_names = set(org["login"] for org in dev1_organizations)

    dev2_organizations = dev2OrgProvider.get_organizations()
    dev2_organization_names = set(org["login"] for org in dev2_organizations)

    common_organizations = dev1_organization_names.intersection(dev2_organization_names)

    # Twitter

    dev1_follows_dev2 = dev1FollowProvider.is_following()
    dev2_follows_dev1 = dev2FollowProvider.is_following()

    check_unexpected_errors(
        [
            dev1FollowProvider,
            dev1FollowProvider,
        ]
    )

    fully_connected = (
        bool(common_organizations) and dev1_follows_dev2 and dev2_follows_dev1
    )

    return {
        "connected": fully_connected,
        "errors": account_errors,
        "common_organizations": common_organizations,
    }
