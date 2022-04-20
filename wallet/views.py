# Create your views here.
from rest_framework import viewsets, permissions

from wallet.models import Wallet
from wallet.serializers import WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all().order_by('-created_at')
    serializer_class = WalletSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user, deleted=False).order_by('-created_at')

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
