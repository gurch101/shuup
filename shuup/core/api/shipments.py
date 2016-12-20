# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

import django_filters
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import serializers, viewsets

from shuup.core.models import Product, Shipment, ShipmentProduct, Shop


class ShipmentProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentProduct
        exclude = ("shipment", "id")


class ShipmentSerializar(serializers.ModelSerializer):
    products = ShipmentProductSerializer(many=True, read_only=True)

    class Meta:
        fields = "__all__"
        model = Shipment


class ShipmentFilter(FilterSet):
    product = django_filters.ModelChoiceFilter(name="products__product",
                                               queryset=Product.objects.all(),
                                               lookup_expr="exact")
    shop = django_filters.ModelChoiceFilter(name="order__shop",
                                            queryset=Shop.objects.all(),
                                            lookup_expr="exact")

    class Meta:
        model = Shipment
        fields = ["id", "order", "product", "shop"]


class ShipmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for shuup.core.models.Shipment
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializar
    filter_backends = (DjangoFilterBackend,)
    filter_class = ShipmentFilter

    def get_view_name(self):
        return _("Shipments")

    def get_view_description(self, html=False):
        return _("Shipments can be listed and fetched.")