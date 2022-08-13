from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserDetailSerializer
from django.contrib.auth import get_user_model
from location.models import LocalGovernmentArea, State

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        qs = User.objects.all()
        return qs

    def retrieve(self, request):
        qs = User.objects.get(id=request.user.id)
        serializer = UserDetailSerializer(qs)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.error)

    def destroy(self, request, *args, **kwargs):
        # if request.user.is_staff:
            # if request.user == 'admin'
        qs = self.get_object()
        qs.delete()
        return Response('User was successfully deleted')

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        
        local_government_area = LocalGovernmentArea.objects.get(name=request.data['local_government_area'])
        user.local_government_area = local_government_area
        state = State.objects.get(name=request.data['state'])
        user.state = state
        user.email = request.data['email']
        user.username = request.data['username']
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.user_image = request.data['user_image']
        user.address = request.data['address']
        user.mobile_no = request.data['address']
        user.certificate_upload = request.data['certificate_upload']
        user.specialization = request.data['specialization']
        user.save()

        serializer = UserDetailSerializer(data=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data

        try:
            local_government_area = LocalGovernmentArea.objects.get(name=request.data['local_government_area'])
            user.local_government_area = local_government_area
            state = State.objects.get(name=request.data['state'])
            user.state = state
        except KeyError:
            pass
        user.email = request.data.get('email', user.email)
        user.username = request.data.get('username', user.email)
        user.first_name = request.data.get('first_name', user.email)
        user.last_name = request.data.get('last_name', user.email)
        user.user_image = request.data.get('user_image', user.email)
        user.address = request.data.get('address', user.address)
        user.mobile_no = request.data.get('address', user.mobile_no)
        user.certificate_upload = request.data.get('certificate_upload', user.certificate_upload)
        user.specialization = request.data.get('specialization', user.specialization)
        user.save()

        serializer = UserDetailSerializer(data=user, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer
    def get_queryset(self):
        qs = User.objects.all()
        return qs




