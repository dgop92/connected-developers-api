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

        dev_reg = DevRegister.objects.create(dev1=dev1, dev2=dev2, connected=False)
        dev_reg.organizations.add(*organizations)
        self.assert_instance_exists(DevRegister, dev1=dev1, dev2=dev2)
