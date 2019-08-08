from rest_framework import serializers

from game.models import Score


class GroupSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField()

    class Meta:
        model = Score
        fields = '__all__'