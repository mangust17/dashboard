from rest_framework import serializers
from .models_tender import *


class OfferWinnersSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferWinners
        fields = "__all__"


class OffersSerializer(serializers.ModelSerializer):
    winners = OfferWinnersSerializer(many=True, read_only=True)

    class Meta:
        model = PartnerOffers
        fields = "__all__"


class PartnerActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerOffersActions
        fields = "__all__"


class TenderContentSerializer(serializers.ModelSerializer):
    partner_min_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )
    partner_max_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )

    offers = OffersSerializer(many=True, read_only=True)

    winners = OfferWinnersSerializer(many=True, read_only=True)

    class Meta:
        model = TenderContent
        fields = "__all__"
