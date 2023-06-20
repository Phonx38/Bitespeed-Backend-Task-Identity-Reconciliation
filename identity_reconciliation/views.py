from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact, LinkPrecedenceTypes
from .serializers import ContactSerializer


class IdentifyContact(APIView):
    def post(self, request):
        data_serializer = ContactSerializer(data=request.data)
        data_serializer.is_valid(raise_exception=True)
        validated_info = data_serializer.validated_data

        contact_email = validated_info.get("email")
        contact_phone = validated_info.get("phoneNumber")

        exact_match = Contact.objects.filter(
            email=contact_email, phoneNumber=contact_phone
        ).first()

        if exact_match:
            return self.generate_response(contact_email, contact_phone)

        partial_match = Contact.objects.filter(
            Q(email=contact_email) | Q(phoneNumber=contact_phone)
        ).order_by("createdAt")

        if not partial_match.exists():
            new_entry = Contact.objects.create(
                email=contact_email,
                phoneNumber=contact_phone,
                linkPrecedence=LinkPrecedenceTypes.PRIMARY.value,
            )
            return self.generate_response(contact_email, contact_phone)

        if not contact_email or not contact_phone:
            return self.generate_response(contact_email, contact_phone)

        matched_records = partial_match.values(
            "id", "phoneNumber", "email", "linkedId", "linkPrecedence"
        )

        email_found = False
        phone_found = False

        linked_id = matched_records[0].get("id")

        if matched_records[0].get("email") == contact_email:
            email_found = True
        if matched_records[0].get("phoneNumber") == contact_phone:
            phone_found = True

        for record in matched_records[1:]:
            if record.get("linkPrecedence") != LinkPrecedenceTypes.SECONDARY.value:
                linked_contact = Contact.objects.get(id=linked_id)
                Contact.objects.filter(id=record["id"]).update(
                    linkedId=linked_contact,
                    linkPrecedence=LinkPrecedenceTypes.SECONDARY.value,
                )

            if not email_found and record.get("email") == contact_email:
                email_found = True
            if not phone_found and record.get("phoneNumber") == contact_phone:
                phone_found = True

        if not email_found or not phone_found:
            linked_contact = Contact.objects.get(
                id=linked_id
            )  # Fetch the Contact instance
            Contact.objects.create(
                phoneNumber=contact_phone,
                email=contact_email,
                linkedId=linked_contact,  # Use the fetched instance
                linkPrecedence=LinkPrecedenceTypes.SECONDARY.value,
            )

        return self.generate_response(contact_email, contact_phone)

    def generate_response(self, contact_email, contact_phone):
        unique_ids = set()
        retrieved_ids = Contact.objects.filter(
            Q(email=contact_email) | Q(phoneNumber=contact_phone)
        ).values("id", "linkedId")

        for entry in retrieved_ids:
            unique_ids.add(entry["id"])
            if entry["linkedId"]:
                unique_ids.add(entry["linkedId"])

        while True:
            previous_count = len(unique_ids)
            retrieved_ids = Contact.objects.filter(
                Q(id__in=unique_ids) | Q(linkedId__in=unique_ids)
            ).values("id", "linkedId")

            for entry in retrieved_ids:
                unique_ids.add(entry["id"])
                if entry["linkedId"]:
                    unique_ids.add(entry["linkedId"])

            if previous_count == len(unique_ids):
                break

        matched_entries = Contact.objects.filter(id__in=unique_ids).order_by(
            "createdAt"
        )

        unique_phoneNumbers = []
        for contact in matched_entries:
            if contact.phoneNumber and contact.phoneNumber not in unique_phoneNumbers:
                unique_phoneNumbers.append(contact.phoneNumber)

        payload = {
            "contact": {
                "primaryContactId": matched_entries[0].id,
                "emails": list(
                    matched_entries.values_list("email", flat=True).distinct()
                ),
                "phoneNumbers": unique_phoneNumbers,
                "secondaryContactIds": list(
                    matched_entries.values_list("id", flat=True)
                )[1:],
            }
        }

        return Response(payload, status=status.HTTP_200_OK)
