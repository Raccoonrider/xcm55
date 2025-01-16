import logging
from django.core.management.base import BaseCommand

from common.models import batch_qs
import events.models
import users.models

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        logging.info("Merging user profiles...")

        for start, end, total, qs in batch_qs(users.models.UserProfile.objects.filter(active=True).order_by('id')):
            logging.info(f"   {start} - {end} / {total}...")
            for target in qs:
                duplicates = users.models.UserProfile.objects.filter(
                    first_name=target.first_name, 
                    last_name=target.last_name,
                    birthday=target.birthday, 
                    active=True,
                ).order_by('id')[1:]

                if duplicates:
                    logging.info(f"Duplicates found: {len(duplicates)} - {target}")

                for duplicate in duplicates:
                    for Model in (events.models.Application, events.models.Result):
                        objects = Model.objects.filter(user_profile=duplicate)
                        for instance in objects:
                            instance.user_profile=target
                            instance.save()

                    objects = users.models.User.objects.filter(profile=duplicate)
                    for instance in objects:
                        instance.profile=target
                        instance.save()

                    duplicate.active = False
                    duplicate.save()