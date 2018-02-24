import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogunchained.settings")
django.setup()

from faker import Faker
import random
from post.models import Comments


fake = Faker()


def generate_comments(number=10):
    for _ in range(0, number):
        Comments.objects.create(
            content=fake.sentence(nb_words=100),
            created=fake.date(),
            post_id=random.choice([1, 2, 3, 6, 9, 10, 13, 14, 15, 16, 19, 20]),
            user_id=random.randint(1, 4)
        )


number_of_comments = input("How Many Comments: ")
generate_comments(int(number_of_comments))
print("Comments Inserted")

