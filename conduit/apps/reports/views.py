from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import (Report, DeviceReport)
from .serializers import (ReportSerializer,)
from .renderers import (ReportJSONRenderer,)

class ReportViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    lookup_field = 'id'
    queryset = Report.objects.all()

    permission_classes = (IsAuthenticatedOrReadOnly,)
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

        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)


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

        return Response(serializer.data, status=status.HTTP_200_OK)


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