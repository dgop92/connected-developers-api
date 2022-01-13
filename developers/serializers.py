from rest_framework import serializers

from developers.models import DevRegister


class DevRegisterSerializer(serializers.ModelSerializer):

    organizations = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = DevRegister
        fields = (
            "registered_at",
            "connected",
            "organizations",
        )
