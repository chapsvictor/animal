from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from core import settings
from rest_framework import serializers
from userapp.models import User
from location.models import State, LocalGovernmentArea
from rest_framework.validators import UniqueValidator
from location.serializers import LocationSerializer, StateSerializer


class UserDetailSerializer(serializers.ModelSerializer):

    """ user model w/o password"""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'user_image', 'certificate_upload', 'specialization', 'address', 'mobile_no', 'state', 'local_government_area')
        read_only_fields = ('email',)


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True, write_only=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    user_image = serializers.ImageField(required=False, allow_empty_file=True)
    address = serializers.CharField(max_length=250)
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), many=False)
    local_government_area = serializers.PrimaryKeyRelatedField(queryset=LocalGovernmentArea.objects.all(), many=False)
    mobile_no = serializers.IntegerField(required=True)
    certificate_upload = serializers.FileField(required=False, allow_empty_file=True)
    specialization = serializers.CharField(max_length=50, required=False)

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("the two password fields didn't match")
        return data

    def get_cleaned_data(self):
        print('get_cleaned_data')
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'email': self.validated_data.get('email', ''),
            'password': self.validated_data.get('password', ''),
            'username': self.validated_data.get('username', ''),
            'state': self.validated_data.get('state', ''),
            'user_image': self.validated_data.get('user_image', ''),
            'address': self.validated_data.get('address', ''),
            'local_government_area': self.validated_data.get('local_government_area', ''),
            'mobile_no': self.validated_data.get('mobile_no', ''),
            'certificate_upload': self.validated_data.get['mobile_no']

        }



    def create(self, validated_data):
        user = User.objects.create(email=self.validated_data['email'],
                                   first_name=self.validated_data['first_name'],
                                   last_name=self.validated_data['last_name'],
                                   username=self.validated_data['username'],
                                   local_government_area=self.validated_data['local_government_area'],
                                   state=self.validated_data['state'],
                                   address=self.validated_data['address'],
                                   mobile_no=self.validated_data['mobile_no'],
                                   )
        try:
            user.user_image = self.validated_data['user_image']
            user.certificate_upload = self.validated_data['certificate_upload']
            user.specialization = self.validated_data['specialization']
        except KeyError:
            pass
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user
