from rest_framework import serializers
from .models_tender import TenderContent


class TenderContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenderContent
        fields = "__all__"
