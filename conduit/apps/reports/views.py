from rest_framework import generics, mixins, status, viewsets, views
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from .models import (Report, )
from conduit.apps.units.models import (Unit,)
from .serializers import (ReportSerializer,)
from .renderers import (ReportJSONRenderer,)

import os,uuid
from datetime import datetime, timedelta
from django.db.models import Q
import oss2

class ReportViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    lookup_field = 'id'
    queryset = Report.objects.all()

    permission_classes = (AllowAny,)
    serializer_class = ReportSerializer

    renderer_classes = (ReportJSONRenderer, )

    def create(self, request):

        serializer_data = request.data.get('report', {})

        serializer_context = {
            'request': request,
            'unitId': serializer_data.get('unitId', None),
            'unit_imei': serializer_data.get('gsm_imei', None)
        }
        serializer = self.serializer_class(data=serializer_data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"reports": serializer.data}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = self.queryset
        unit_queryset = Unit.objects.all()
        if self.request.user.is_superuser is not True:
            ownerQ = Q(unit__owner=self.request.user)
            operatorQ = Q(unit__operators__id__contains=self.request.user.id)
            queryset = queryset.filter(ownerQ | operatorQ)

        lasttime_string = self.request.query_params.get('lasttime', None)

        id = self.request.query_params.get('id', None)
        unitId = self.request.query_params.get('unitId', None)

        if id is not None:
            queryset = queryset.filter(id=id)
        elif lasttime_string is not None:
            lasttime = datetime.strptime(lasttime_string, '%Y-%m-%d-%H:%M:%S')
            queryset = queryset.filter(updated_at__gt=lasttime)
        elif unitId is not None:
            try:
                unit = unit_queryset.get(id=unitId)
            except Unit.DoesNotExist:
                raise NotFound('unit with id not found')
            unit_selected = unit_queryset.filter(id=unitId)
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
        unitId = serializer_data.get('unitId', None)
        ackoperatorId = serializer_data.get('ackOperatorId', None)
        serializer_context = {'request': request,
                              'unitId': unitId,
                              'ackOperatorId': ackoperatorId}

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


class ImageUploadView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    parser_classes = (FileUploadParser,)

    reportMediaBindingThresholdMin = 1000
    accessKeyId = "LTAIxuJzCN49WyOx"
    accessKeySecret = "YzU2GrECDsYFlePmGeqHAhFYejW5Q8 "
    endpoint = "oss-cn-shanghai.aliyuncs.com"
    defaultBucketName = "beacon-media"

    def upload_to_oss(self, file_obj, mediaGuid, cameraid, frameid):
        try:
            filename = str.format("%s_%s_%s.jpg" % (mediaGuid, cameraid, frameid))

            # aliyun oss service
            auth = oss2.Auth(self.accessKeyId, self.accessKeySecret)
            bucket = oss2.Bucket(auth, self.endpoint, self.defaultBucketName)
            bucket.put_object(filename, file_obj)
            print("picture uploaded to oss, filename=%s" % filename)
        except Exception as e:
            raise ValidationError('upload image failed ', e)

    def post(self, request, imei, statusid, mode, cameraid, frameid, format='jpg'):

        report = None

        #update report
        time_low = datetime.now() - timedelta(minutes=self.reportMediaBindingThresholdMin)
        report = Report.objects.filter(Q(unit__identity=imei), Q(infoId=statusid), Q(time__gt=time_low)).first()
        if report is None:
            raise Report.DoesNotExist
        if cameraid == '1':
            report.mediaTypeCamera1 = mode
        if cameraid == '2':
            report.mediaTypeCamera2 = mode
        if cameraid == '3':
            report.mediaTypeCamera3 = mode
        report.hasMedia = True
        if report.mediaGuid is None or report.mediaGuid == '':
            report.mediaGuid = uuid.uuid4().hex

        report.save()

        file_obj = request.data['file']

        self.upload_to_oss(file_obj, report.mediaGuid, cameraid, frameid)

        # #picture handling logic
        # saving_path = '/tmp/'
        # full_path = os.path.join(saving_path, file_obj.name)
        # with open(full_path, 'wb+') as destination:
        #     for chunk in file_obj.chunks():
        #         destination.write(chunk)
        #         destination.close()

        result = {
            "success": True
        }
        return Response(result, status=status.HTTP_200_OK)
