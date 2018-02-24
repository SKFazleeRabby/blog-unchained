import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogunchained.settings")
django.setup()


import random
from django.utils import timezone
from faker import Faker
from post.models import Post


fake = Faker()


def generate_post(number=10):
    for _ in range(0, number):
        Post.objects.create(
            title=fake.sentence(),
            body=fake.paragraphs(nb=7),
            images='images/default.png',
            created_at=timezone.now(),
            category_id=random.randint(1, 2),
            user_id=random.randint(1, 4),
            draft=random.randint(0, 1),
            featured=0,
            published=timezone.now().date()
        )


number_of_post = input("How Many Post: ")
generate_post(int(number_of_post))
print("Data Inserted")

