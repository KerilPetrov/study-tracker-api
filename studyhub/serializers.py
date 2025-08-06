from rest_framework import serializers

from studyhub.models import Plan, Topic


class TitleValidationMixin:
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название не может быть пустым.")
        return value


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "topic",
            "title",
            "is_done",
            "estimated_minutes",
            "actual_minutes",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class TaskReadSerializer(TaskSerializer):
    pass


class TaskCreateSerializer(TaskSerializer, TitleValidationMixin):
    def validate_estimated_minutes(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Количество времени не может быть отрицательным."
            )

    def validate_actual_minutes(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Количество времени не может быть отрицательным."
            )


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [
            "id",
            "plan",
            "title",
            "description",
            "order",
            "estimated_days",
            "is_optional",
        ]

        read_only_fields = [
            "id",
        ]


class TopicReadSerializer(TopicSerializer):
    tasks = TaskReadSerializer(many=True, read_only=True)


class TopicCreateSerializer(TopicSerializer, TitleValidationMixin):

    def validate_order(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Порядок темы не может быть отрицательным."
            )

    def validate_estimated_days(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Количество дней не может быть отрицательным."
            )

    def validate_plan(self, plan):
        request = self.context.get("request")
        if plan.owner != request.user:
            raise serializers.ValidationError("Недопустимый доступ к плану.")
        return plan


class PlanSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Plan.

    Включает поля:
    - id
    - title
    - description
    - created_at
    - updated_at
    """

    class Meta:
        model = Plan
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PlanReadSerializer(PlanSerializer):
    topics = TopicReadSerializer(many=True, read_only=True)


class PlanCreateSerializer(serializers.ModelSerializer):
    pass
