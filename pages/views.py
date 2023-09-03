from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import Subject_A, Subject_B, Subject_C, Subject_D, Page
from .serializers import PageSerializer
from django.db import connection
from django.http import Http404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# # ORM Version
# class PageViewSet(viewsets.ViewSet):
#     queryset = Page.objects.all()
#     serializer_class = PageSerializer

#     @action(detail=False, url_path=r'(?P<page_id>\d+)', url_name='page')
#     def get_page(self, request, page_id=None):
#         obj = get_object_or_404(Page, pk=page_id)
#         breadcrumbs = []

#         if obj.parent_object:
#             if isinstance(obj.parent_object, Subject_A):
#                 name = obj.parent_object.name
#                 breadcrumbs.append(name)

#             elif isinstance(obj.parent_object, Subject_B):
#                 subject_a_name = obj.parent_object.parent.name
#                 breadcrumbs.append(subject_a_name)
#                 name = obj.parent_object.name
#                 breadcrumbs.append(name)

#             elif isinstance(obj.parent_object, Subject_C):
#                 subject_b_name = obj.parent_object.parent.parent.name
#                 breadcrumbs.append(subject_b_name)
#                 subject_a_name = obj.parent_object.parent.name
#                 breadcrumbs.append(subject_a_name)
#                 name = obj.parent_object.name
#                 breadcrumbs.append(name)

#             elif isinstance(obj.parent_object, Subject_D):
#                 subject_c_name = obj.parent_object.parent.parent.parent.name
#                 breadcrumbs.append(subject_c_name)
#                 subject_b_name = obj.parent_object.parent.parent.name
#                 breadcrumbs.append(subject_b_name)
#                 subject_a_name = obj.parent_object.parent.name
#                 breadcrumbs.append(subject_a_name)
#                 name = obj.parent_object.name
#                 breadcrumbs.append(name)

#         serializer_context = {'breadcrumbs': breadcrumbs}
#         serializer = self.serializer_class(obj, context=serializer_context)

#         return Response(serializer.data)



# SQL Version
class IsAuthenticatedOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.user.is_staff


class PageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrAdmin]

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Page, pk=pk)
        object_id = obj.object_id
        content_type_id = obj.content_type_id

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        p.title AS page_title,
                        p.content AS page_content,
                        sa.name AS subject_a_name,
                        sb.name AS subject_b_name,
                        sc.name AS subject_c_name,
                        sd.name AS subject_d_name,
                        COALESCE(sa.name, sb.name, sc.name, sd.name) AS breadcrumbs
                    FROM pages_page p
                    LEFT JOIN pages_subject_a sa ON p.object_id = sa.id
                    LEFT JOIN pages_subject_b sb ON sa.id = sb.parent_id
                    LEFT JOIN pages_subject_c sc ON sb.id = sc.parent_id
                    LEFT JOIN pages_subject_d sd ON sc.id = sd.parent_id
                    WHERE p.content_type_id = %s AND p.object_id = %s;
                    """,
                    [content_type_id, object_id],
                )

                row = cursor.fetchone()
                print(row)
                if row is None:
                    raise Http404("Page does not exist")

                (
                    page_title,
                    page_content,
                    subject_a_name,
                    subject_b_name,
                    subject_c_name,
                    subject_d_name,
                    breadcrumbs
                 ) = row

                breadcrumbs = [
                    name for name in [
                        subject_a_name,
                        subject_b_name,
                        subject_c_name,
                        subject_d_name,
                    ] if name
                ]

                response_data = {
                    'title': page_title,
                    'content': page_content,
                    'breadcrumbs': breadcrumbs
                }

                return Response(response_data)

        except Page.DoesNotExist:
            raise Http404("Page does not exist")
