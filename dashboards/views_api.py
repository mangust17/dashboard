from .models import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import viewsets
from .serializers import *
from urllib.parse import unquote


@api_view(["GET"])
def get_models(request):
    models_qs = (
        PricesClean.objects.values_list("model", flat=True).distinct().order_by("model")
    )
    data = [{"label": model, "value": model} for model in models_qs]
    return JsonResponse(data, safe=False)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models_tender import TenderContent, PartnerOffers, OfferWinners


@api_view(["GET"])
def get_colors(request, model):
    model_name = unquote(model)
    models_qs = (
        PricesClean.objects.filter(model=model_name)
        .values_list("color", flat=True)
        .order_by("color")
        .distinct()
    )
    data = [{"label": color, "value": color} for color in models_qs]
    return JsonResponse(data, safe=False)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models_tender import TenderContent, PartnerOffers, OfferWinners


@api_view(["GET"])
def get_full_table(request):
    result = []

    tenders = TenderContent.objects.prefetch_related("offers", "winners__offer")

    for tender in tenders:
        row = {
            "id": tender.id,
            "model": tender.model,
            "buyer_name": tender.buyer_name,
            "sim_spec": tender.sim_spec,
            "order_qty": tender.order_qty,
            "partner_min_price": float(tender.partner_min_price or 0),
            "partner_max_price": float(tender.partner_max_price or 0),
            "stat_min_price": float(tender.stat_min_price or 0),
            "stat_max_price": float(tender.stat_max_price or 0),
        }

        # Добавляем колонки с ценами всех офферов
        offers = tender.offers.all()
        for offer in offers:
            row[f"offer_price_{offer.seller_name}"] = float(offer.price or 0)

        # Добавляем колонки с количеством победителей
        winners = tender.winners.all()
        for winner in winners:
            row[f"winner_{winner.offer.seller_name}_qty"] = winner.qty

        # Авто-выбор победителя по минимальной цене
        if offers.exists():
            min_offer = min(offers, key=lambda o: o.price or 0)
            row["winner"] = min_offer.seller_name
            row["winner_price"] = float(min_offer.price or 0)

        # Добавляем список офферов
        row["offers"] = [
            {"seller_name": offer.seller_name, "price": float(offer.price or 0)}
            for offer in offers
        ]

        # Добавляем сумму qty победителей
        row["winners_sum"] = sum(winner.qty or 0 for winner in winners)

        result.append(row)

    return Response(result)


class TenderContentViewSet(viewsets.ModelViewSet):
    queryset = TenderContent.objects.all()
    serializer_class = TenderContentSerializer


class OffersViewSet(viewsets.ModelViewSet):
    queryset = PartnerOffers.objects.all()
    serializer_class = OffersSerializer


class WinnersViewSet(viewsets.ModelViewSet):
    queryset = OfferWinners.objects.all()
    serializer_class = OfferWinnersSerializer


class ActionsViewSet(viewsets.ModelViewSet):
    queryset = PartnerOffersActions.objects.all()
    serializer_class = PartnerActionsSerializer
