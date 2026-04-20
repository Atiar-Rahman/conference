from rest_framework import serializers
from papers.models import Paper,CoAuthor,ReviewAssignment,Review
from conferences.serializers import TrackSerializer
from conferences.serializers import SimpleUserSerializer
from conferences.models import Track


class PaperSerializer(serializers.ModelSerializer):

    author = SimpleUserSerializer(read_only=True)
    track = TrackSerializer(read_only=True)

    class Meta:
        model = Paper
        fields = [
            'id', 'author', 'track',
            'title', 'abstract', 'keywords',
            'pdf', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'author', 'track',
            'created_at', 'updated_at',
            'status'
        ]

    def validate(self, data):
        request = self.context["request"]

        # get track from view kwargs
        view = self.context["view"]
        track_id = view.kwargs.get("track_pk")

        track = Track.objects.get(pk=track_id)
        config = track.conference.submission_config

        #  1. paper limit check
        paper_count = Paper.objects.filter(
            track=track,
            author=request.user,
            is_deleted=False
        ).count()

        if paper_count >= config.paper_limit:
            raise serializers.ValidationError(
                "Paper submission limit reached for this conference."
            )

        # 2. abstract length check (optional logic example)
        abstract = data.get("abstract", "")
        if len(abstract) > config.abstract_limit:
            raise serializers.ValidationError(
                f"Abstract exceeds limit of {config.abstract_limit} characters."
            )

        return data


class PaperStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ["id","status"]

    def validate_status(self, value):
        user = self.context["request"].user

        # reviewer restriction
        if user.role == "reviewer" and value not in [user.role.ACCEPTED, user.role.REJECTED]:
            raise serializers.ValidationError(
                "Reviewer can only accept or reject"
            )

        return value
    




class CoAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoAuthor
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        user = data.get("user")
        email = data.get("email")
        paper = data.get("paper")

        # 1. Must have identity
        if not user and not email:
            raise serializers.ValidationError(
                "Either user or email must be provided."
            )

        # 2. Prevent duplicate user per paper
        if user and CoAuthor.objects.filter(paper=paper, user=user).exists():
            raise serializers.ValidationError(
                "This user is already a co-author of this paper."
            )

        # 3. Prevent duplicate email per paper (external authors)
        if email and CoAuthor.objects.filter(paper=paper, email=email).exists():
            raise serializers.ValidationError(
                "This email is already added as co-author."
            )

        return data
    





class ReviewAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewAssignment
        fields = ['id','paper','reviewer','assigned_at','updated_at']
        read_only_fields = ['id', 'assigned_at','updated_at']

    def validate(self, data):
        if data['reviewer'].role != 'reviewer':
            raise serializers.ValidationError(
                "Assigned user must have reviewer role."
            )
        return data
    




class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','assignment','comment','plagiarism_score','ai_score','recommendation']
        read_only_fields = ['id','assignment']

    def validate(self, data):
        request = self.context["request"]
        assignment = self.context.get("assignment")  # FIXED

        if not assignment:
            raise serializers.ValidationError("Assignment not found.")

        if assignment.reviewer != request.user:
            raise serializers.ValidationError(
                "You are not assigned to this paper."
            )

        return data