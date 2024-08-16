from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import Payments, User
from .serializers import PaymentsSerializer, UserSerializer
from materials.permissions import IsStuff, IsOwner
from users.services import create_product_with_price, create_stripe_session


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('payment_way', 'paid_product', 'user',)
    ordering_fields = ('payment_date',)
    permission_classes = [AllowAny]


class PaymentsCreateAPIView(generics.CreateAPIView):
    """Контроллер создания платежа"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = f'{payment.paid_product}'
        price = create_product_with_price(name=product, unit_amount=payment.amount)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

        user_email = serializer.save['email']
        send_mail(
            "Подтверждение регистрации",
            "Добро пожаловать! Вы успешно зарегистрированы.",
            "tima.zaplavnyy@ya.ru",
            [user_email],
            fail_silently=False,
        )
        print(user_email)


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser | IsStuff]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    template_name = 'profile.html'
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser | IsStuff]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner | IsAdminUser]


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
