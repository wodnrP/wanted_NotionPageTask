from rest_framework import generics, status
from rest_framework.response import Response
from .models import Board
from .serializers import BoardSerializer
from django.db import connection

class BoardMainView(generics.GenericAPIView):
    serializer_class = BoardSerializer
    
    def get(self, request, PageId):
        try:
            board = Board.objects.get(pageId=PageId)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM boards_board WHERE pageId = %s", [PageId])
            row = cursor.fetchone()
        if row is None:
            return Response (status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(row, status=status.HTTP_200_OK)
            