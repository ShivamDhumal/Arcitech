from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser, content_item, category
from django.core.validators import RegexValidator

class UserSerializer(serializers.ModelSerializer):

    PASSWORD_REGEX = RegexValidator(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',)
    
    phone_validator = RegexValidator(
        regex=r'^\d{1,10}$',
        message='Enter a valid phone number with a maximum of 10 digits.',
        code='invalid_phone'
    )
    pincode_validator = RegexValidator(
        regex=r'^\d{6}$',
        message='Enter a valid 6-digit PIN code.',
        code='invalid_pincode'
    )

    email = serializers.EmailField(
        required=True,
    )
    first_name = serializers.CharField(
        required=True,
    )
    last_name = serializers.CharField(
        required=True,
    )
    phone = serializers.IntegerField(
        required=True,
        validators=[phone_validator]
    )
    pincode = serializers.IntegerField(
        required=True,
        validators=[pincode_validator]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[PASSWORD_REGEX],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone', 'pincode', 'email', 'password', 'password2', 'state', 'city', 'country', 'address')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            pincode=validated_data.get('pincode', ''),
            state=validated_data.get('state', ''),
            city=validated_data.get('city', ''),
            country=validated_data.get('country', ''),
            address=validated_data.get('address', ''),
        )
        password = validated_data['password']

        try:
            validate_password(password, user=user)
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        user.set_password(password)
        user.username = validated_data['email']
        user.save()
        return user

class contentserializer(serializers.ModelSerializer):
    user = serializers.CharField(
        required=False,
    )
    class Meta:
        model = content_item
        fields = '__all__'
