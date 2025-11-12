from rest_framework import serializers
from django.utils import timezone
from .models import Invite, InvitedPerson, Response, ConfirmedPerson, MenuType


class InvitedPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitedPerson
        fields = ["family_name", "given_name"]


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ["is_coming", "date_of_response"]


class ConfirmedPersonSerializer(serializers.ModelSerializer):
    menu_type = serializers.CharField(source="menu_type.menu_name")

    class Meta:
        model = ConfirmedPerson
        fields = ["full_name", "menu_type"]


class InviteDetailSerializer(serializers.ModelSerializer):
    people = InvitedPersonSerializer(many=True, read_only=True)
    response = ResponseSerializer(read_only=True)
    confirmed_people = ConfirmedPersonSerializer(many=True, read_only=True)

    class Meta:
        model = Invite
        fields = [
            "code",
            "sent_invite",
            "date_last_access",
            "people",
            "response",
            "confirmed_people",
        ]


class ConfirmedPersonInputSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    menu_type_id = serializers.IntegerField()


class ResponseCreateSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10)
    is_coming = serializers.BooleanField()
    message = serializers.CharField(max_length=500, allow_blank=True)
    confirmed_people = ConfirmedPersonInputSerializer(many=True, required=False)

    def create(self, validated_data):
        code = validated_data.get("code")
        is_coming = validated_data.get("is_coming")
        message = validated_data.get("message")
        confirmed_people_data = validated_data.get("confirmed_people", [])

        try:
            invite = Invite.objects.get(code=code)
        except Invite.DoesNotExist:
            raise serializers.ValidationError({"code": "Codul nu există."})

        response, created = Response.objects.update_or_create(
            invite=invite,
            defaults={
                "is_coming": is_coming,
                "message": message,
                "date_of_response": timezone.now(),
            },
        )

        ConfirmedPerson.objects.filter(invite=invite).delete()

        if is_coming and confirmed_people_data:
            for person_data in confirmed_people_data:
                menu_type = MenuType.objects.get(id=person_data["menu_type_id"])
                ConfirmedPerson.objects.create(
                    invite=invite,
                    full_name=person_data["full_name"],
                    menu_type=menu_type,
                )

        return {
            "code": code,
            "is_coming": is_coming,
            "message": message,
            "confirmed_count": len(confirmed_people_data) if is_coming else 0,
        }


class MenuTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuType
        fields = ["id", "menu_name"]