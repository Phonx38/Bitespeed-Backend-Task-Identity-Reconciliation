from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "phoneNumber",
            "email",
            "linkedId",
            "linkPrecedence",
            "createdAt",
            "updatedAt",
            "deletedAt",
        ]

    def validate(self, data):
        phone = data.get("phoneNumber")
        email = data.get("email")
        if not phone and not email:
            raise serializers.ValidationError("Phone number or Email is required.")
        if phone and not phone.isnumeric():
            raise serializers.ValidationError("Phone number is not valid")
        return data
