from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import Subject_A, Subject_B, Subject_C, Subject_D, Page
from .serializers import PageSerializer
from django.db import connection
from django.http import Http404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# ORM Version
class PageViewSet(viewsets.ViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    @action(detail=False, url_path=r'(?P<page_id>\d+)', url_name='page')
    def get_page(self, request, page_id=None):
        obj = get_object_or_404(Page, pk=page_id)
        breadcrumbs = []

        if obj.parent_object:
            if isinstance(obj.parent_object, Subject_A):
                name = obj.parent_object.name
                breadcrumbs.append(name)

            elif isinstance(obj.parent_object, Subject_B):
                subject_a_name = obj.parent_object.parent.name
                breadcrumbs.append(subject_a_name)
                name = obj.parent_object.name
                breadcrumbs.append(name)

            elif isinstance(obj.parent_object, Subject_C):
                subject_b_name = obj.parent_object.parent.parent.name
                breadcrumbs.append(subject_b_name)
                subject_a_name = obj.parent_object.parent.name
                breadcrumbs.append(subject_a_name)
                name = obj.parent_object.name
                breadcrumbs.append(name)

            elif isinstance(obj.parent_object, Subject_D):
                subject_c_name = obj.parent_object.parent.parent.parent.name
                breadcrumbs.append(subject_c_name)
                subject_b_name = obj.parent_object.parent.parent.name
                breadcrumbs.append(subject_b_name)
                subject_a_name = obj.parent_object.parent.name
                breadcrumbs.append(subject_a_name)
                name = obj.parent_object.name
                breadcrumbs.append(name)

        serializer_context = {'breadcrumbs': breadcrumbs}
        serializer = self.serializer_class(obj, context=serializer_context)

        return Response(serializer.data)



