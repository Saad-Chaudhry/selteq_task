import factory
from faker import Faker
from django.contrib.auth import get_user_model
from core.models import Task

fake = Faker()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: fake.email())
    username = factory.LazyAttribute(lambda _: fake.user_name())
    password = factory.PostGenerationMethodCall("set_password", "Test@1234")


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    user = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence")
    duration = factory.Faker("random_int", min=1, max=120)
