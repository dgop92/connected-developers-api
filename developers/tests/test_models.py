from django.db.models import Q
from django.test import TestCase
from test_utils import InstanceAssertionsMixin

from developers.models import Dev, DevRegister, Organization


class TestModels(TestCase, InstanceAssertionsMixin):
    def test_basic_creation(self):

        dev1_username = "juan"
        dev2_username = "mike"
        dev1 = Dev.objects.create(username=dev1_username)
        dev2 = Dev.objects.create(username=dev2_username)
        self.assert_instance_exists(Dev, username=dev1_username)
        self.assert_instance_exists(Dev, username=dev2_username)

        organization_names = ["org1", "org2"]
        organizations = []
        for name in organization_names:
            organizations.append(Organization.objects.create(name=name))
            self.assert_instance_exists(Organization, name=name)

        dev1.organizations.add(*organizations)
        dev2.organizations.add(*organizations)

        DevRegister.objects.create(dev1=dev1, dev2=dev2, connected=False)
        self.assert_instance_exists(DevRegister, dev1=dev1, dev2=dev2)

    def test_registers_of_devs(self):

        dev1 = Dev.objects.create(username="d1")
        dev2 = Dev.objects.create(username="d2")
        org1 = Organization.objects.create(name="git")
        org2 = Organization.objects.create(name="lab")
        dev1.organizations.add(org1)
        dev1.organizations.add(org1)

        DevRegister.objects.create(dev1=dev1, dev2=dev2, connected=True)

        dev1.organizations.remove(org1)
        dev2.organizations.add(org2)

        DevRegister.objects.create(dev1=dev2, dev2=dev1, connected=False)

        registers = DevRegister.objects.filter(
            Q(dev1=dev1) & Q(dev2=dev2) | Q(dev1=dev2) & Q(dev2=dev1)
        )

        # last events are fisrt
        self.assertFalse(registers[0].connected)
        self.assertTrue(registers[1].connected)
