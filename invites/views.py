from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Invite, MenuType
from .serializers import InviteDetailSerializer, ResponseCreateSerializer, MenuTypeSerializer


class InviteDetailView(generics.RetrieveAPIView):
    queryset = Invite.objects.all()
    serializer_class = InviteDetailSerializer
    lookup_field = "code"

    def get(self, request, *args, **kwargs):
        code = self.kwargs.get("code")
        try:
            invite = Invite.objects.prefetch_related(
                "people", "confirmed_people", "confirmed_people__menu_type"
            ).select_related("response").get(code=code)
        except Invite.DoesNotExist:
            return Response(
                {"error": "Codul de invitație nu există."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(invite)
        return Response(serializer.data)


class InviteAccessUpdateView(generics.UpdateAPIView):
    queryset = Invite.objects.all()
    lookup_field = "code"
    http_method_names = ["patch"]

    def patch(self, request, *args, **kwargs):
        code_value = self.kwargs.get("code")

        try:
            invite = Invite.objects.get(code=code_value)
        except Invite.DoesNotExist:
            return Response({"error": "Codul nu există."}, status=status.HTTP_404_NOT_FOUND)

        invite.date_last_access = timezone.now()
        invite.save(update_fields=["date_last_access"])

        return Response({
            "message": "DateLastAccess actualizat cu succes.",
            "code": invite.code,
            "date_last_access": invite.date_last_access
        }, status=status.HTTP_200_OK)


class ResponseCreateView(generics.CreateAPIView):
    serializer_class = ResponseCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(
            {
                "message": "Răspuns salvat cu succes.",
                **result
            },
            status=status.HTTP_200_OK,
        )


class MenuTypeListView(generics.ListAPIView):
    queryset = MenuType.objects.all()
    serializer_class = MenuTypeSerializer
