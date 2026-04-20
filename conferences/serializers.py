from rest_framework import serializers
from conferences.models import Track, Conference,Session
from django.contrib.auth import get_user_model

User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id','email']


class SimpleConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ['id', 'name', 'short_name', 'location', 'start_date', 'end_date']


class TrackSerializer(serializers.ModelSerializer):
    conference = SimpleConferenceSerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Track
        fields = ['id','name','conference','user','created_at','updated_at']
        read_only_fields = ['conference', 'user']

    def validate(self, data):
        request = self.context.get('request')
        view = self.context.get('view')

        conference_id = view.kwargs.get('conference_pk')
        user = request.user

        qs = Track.objects.filter(
            conference_id=conference_id,
            user=user
        )

        # update case handle
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "You already created a track in this conference."
            )

        return data
    

class SessionSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Session
        fields = ['id','track','user','title','start_time','end_time']
        read_only_fields = ['track','user']