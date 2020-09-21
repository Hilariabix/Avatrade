from django.contrib.auth import get_user_model
from rest_framework import serializers
from avatrade.social_network.utils import verify_email, enrich_by_email

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type':   'password'})

    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'User already exists, please log in.'})

        if not verify_email(email):
            serializers.ValidationError({'email': 'Email address verification failed.'})

        enriched_data = enrich_by_email(email)

        user = User(**enriched_data)
        user.set_password(password)
        user.save()
        return user
