from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import (Report, )
from conduit.apps.units.models import (Unit,)
from .serializers import (ReportSerializer,)
from .renderers import (ReportJSONRenderer,)

from datetime import datetime
from django.db.models import Q

class ReportViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    lookup_field = 'id'
    queryset = Report.objects.all()

    permission_classes = (IsAuthenticated,)
    serializer_class = ReportSerializer

    renderer_classes = (ReportJSONRenderer, )

    def create(self, request):

        serializer_data = request.data.get('report', {})

        serializer_context = {
            'request': request,
            'unit_id': serializer_data['unit_id']
        }
        serializer = self.serializer_class(data=serializer_data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = self.queryset
        unit_queryset = Unit.objects.all()
        if self.request.user.is_superuser is not True:
            ownerQ = Q(unit__owner=self.request.user)
            operatorQ = Q(unit__operators__id__contains=self.request.user.id)
            queryset = queryset.filter(ownerQ | operatorQ)

        lasttime_string = self.request.query_params.get('lasttime', None)

        id = self.request.query_params.get('id', None)
        unit_id = self.request.query_params.get('unit_id', None)

        if id is not None:
            queryset = queryset.filter(id=id)
        elif lasttime_string is not None:
            lasttime = datetime.strptime(lasttime_string, '%Y-%m-%d-%H:%M:%S')
            queryset = queryset.filter(updated_at__gt=lasttime)
        elif unit_id is not None:
            try:
                unit = unit_queryset.get(id=unit_id)
            except Unit.DoesNotExist:
                raise NotFound('unit with id not found')
            unit_selected = unit_queryset.filter(id=unit_id)
            if unit.type == 1:      #line
                unit_selected = unit_queryset.filter(parent=unit)
            elif unit.type == 0:    #city
                unit_selected = unit_queryset.filter(parent__parent=unit)
            queryset = queryset.filter(unit__in=unit_selected)
        return queryset

    def list(self, request):
        serializer_context = {'request': request}
        page = self.paginate_queryset(self.get_queryset())

        serializer = self.serializer_class(page,
                                           context=serializer_context,
                                           many=True)

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, id):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(id=id)
        except Report.DoesNotExist:
            raise NotFound('An report with this id does not exists.')

        serializer = self.serializer_class(serializer_instance,
                                           context=serializer_context)

        return Response(serializer.data, status = status.HTTP_200_OK)


class ReportUpdateAPIView(generics.UpdateAPIView):
    lookup_url_kwarg = 'report_id'
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def post(self, request, report_id=None):

        serializer_data = request.data.get('report', {})
        unit_id = serializer_data.get('unit_id', None)
        ackoperator_id = serializer_data.get('ackoperator_id', None)
        serializer_context = {'request': request,
                              'unit_id': unit_id,
                              'ackoperator_id': ackoperator_id }

        try:
            serializer_instance = self.queryset.get(id=report_id)
        except Report.DoesNotExist:
            raise NotFound("report with id not found")

        serializer = self.serializer_class(serializer_instance,
                                            context=serializer_context,
                                            data=serializer_data,
                                            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        result = {
            "success": True,
            "report": serializer.data}
        return Response(result, status=status.HTTP_200_OK)


class ReportDeleteAPIView(generics.DestroyAPIView):
    lookup_url_kwarg = 'report_id'
    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def post(self, request, report_id=None):
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            raise NotFound('Report with this ID does not exists.')

        report.delete()

        return Response(None,  status=status.HTTP_204_NO_CONTENT)

