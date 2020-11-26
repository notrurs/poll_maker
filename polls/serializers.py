from rest_framework import serializers
from .models import Poll, Question, Choice, Answer


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class PollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'poll_date_start' in validated_data:
            raise serializers.ValidationError({'poll_date_start': 'Cant change poll_date_start'})
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def create(self, validated_data):
        if validated_data['poll_date_start'] >= validated_data['poll_date_end']:
            raise serializers.ValidationError({'poll_date_start': 'poll_date_start is bigger or equal then poll_date_end'})
        return Poll.objects.create(**validated_data)


class ChoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class AnswerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
