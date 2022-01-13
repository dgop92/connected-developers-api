import tweepy
from django.conf import settings
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from developers.models import Dev, DevRegister, Organization
from developers.serializers import DevRegisterSerializer
from external_services.algorithms import ConnectedException, are_fully_connected
from external_services.github import BasicOrganizationProvider
from external_services.twitter import BasicFollowEachOtherProvider

TOKEN = settings.TWITER_BEARER_TOKEN
GITHUB_ORG_URL = "https://api.github.com/users/{user}/orgs"
client = tweepy.Client(TOKEN)


def register_new_devs(dev1_username, dev2_username, connected_data):

    # get or create return a tuple (instance, bool: created or not)
    dev1 = Dev.objects.get_or_create(username=dev1_username)[0]
    dev2 = Dev.objects.get_or_create(username=dev2_username)[0]

    # so far we only save common organizations
    organization_names = connected_data["common_organizations"]
    organizations = []
    for name in organization_names:
        org = Organization.objects.get_or_create(name=name)[0]
        organizations.append(org)

    # new update, new organizations, so clear relationships and add new ones
    dev1.organizations.clear()
    dev2.organizations.clear()
    dev1.organizations.add(*organizations)
    dev2.organizations.add(*organizations)

    dev_reg = DevRegister.objects.create(
        dev1=dev1, dev2=dev2, connected=connected_data["connected"]
    )
    dev_reg.organizations.add(*organizations)


@api_view(["GET"])
def realtime_view(request, dev1, dev2):

    """
    Check if two developers are connected and what GitHub organizations they have in common
    """

    if dev1 == dev2:
        return Response(
            {"detail": "both dev are the same person"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    dt1 = BasicFollowEachOtherProvider(client, dev1, dev2)
    dt2 = BasicFollowEachOtherProvider(client, dev2, dev1)
    do1 = BasicOrganizationProvider(GITHUB_ORG_URL.format(user=dev1))
    do2 = BasicOrganizationProvider(GITHUB_ORG_URL.format(user=dev2))

    try:
        connected_data = are_fully_connected(do1, dt1, do2, dt2)
        if connected_data["errors"]:
            final_errors = [
                e.format(dev1=dev1, dev2=dev2) for e in connected_data["errors"]
            ]
            return Response(
                {"errors": final_errors}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            fully_connected = connected_data["connected"]
            register_new_devs(
                dev1_username=dev1, dev2_username=dev2, connected_data=connected_data
            )
            if fully_connected:
                return Response(
                    {
                        "connected": True,
                        "organisations": connected_data["common_organizations"],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "connected": False,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
    except ConnectedException as e:
        return Response(
            {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def register_view(request, dev1, dev2):

    try:
        d1 = Dev.objects.get(username=dev1)
        d2 = Dev.objects.get(username=dev2)

        registers = DevRegister.objects.filter(
            Q(dev1=d1) & Q(dev2=d2) | Q(dev1=d2) & Q(dev2=d1)
        )

        serialized_registers = []
        for register in registers:
            devreg_serializer = DevRegisterSerializer(register)
            serialized_registers.append(devreg_serializer.data)
        return Response(serialized_registers, status=status.HTTP_200_OK)
    except Dev.DoesNotExist:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
