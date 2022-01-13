from django.db.models import Q
from django.test import TestCase

from developers.models import Dev, DevRegister, Organization
from developers.serializers import DevRegisterSerializer


class TestSerializers(TestCase):
    def test_serialization_of_registers(self):

        # realtime 1
        dev1 = Dev.objects.create(username="d1")
        dev2 = Dev.objects.create(username="d2")
        org1 = Organization.objects.create(name="git")
        org2 = Organization.objects.create(name="lab")
        dev1.organizations.add(org1, org2)
        dev2.organizations.add(org1, org2)
        dev_reg = DevRegister.objects.create(dev1=dev1, dev2=dev2, connected=True)
        dev_reg.organizations.add(org1, org2)

        # realtime 2
        dev1.organizations.clear()
        dev2.organizations.clear()
        dev_reg = DevRegister.objects.create(dev1=dev2, dev2=dev1, connected=False)

        registers = DevRegister.objects.filter(
            Q(dev1=dev1) & Q(dev2=dev2) | Q(dev1=dev2) & Q(dev2=dev1)
        )

        serialized_registers = []
        for register in registers:
            devreg_serializer = DevRegisterSerializer(register)
            serialized_registers.append(devreg_serializer.data)

        print(serialized_registers)
