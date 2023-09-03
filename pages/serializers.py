from rest_framework import serializers
from .models import Page


class PageSerializer(serializers.ModelSerializer):
    page_id = serializers.IntegerField(source='id', read_only=True)
    breadcrumbs = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = Page
        exclude = ('id', 'object_id', 'content_type')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['breadcrumbs'] = self.context['breadcrumbs']
        return data
