import os
from os.path import isfile, join

import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.db import transaction

from core.settings import XML_PATH
from shedule import models


class Command(BaseCommand):
    help = 'Parses XML files provided by rea'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    @transaction.non_atomic_requests
    def handle(self, *args, **options):
        dump_path = options['path'] if 'path' in options.keys() else XML_PATH
        print(dump_path)
        if dump_path and os.path.exists(dump_path):
            filenames = [join(dump_path, f) for f in os.listdir(dump_path) if isfile(join(dump_path, f))]
        else:
            self.stdout.write("Not able to find path to parse. Please, Specify it in settings.py or pass it as argument --path.")

        # clear db?

        for index, filename in enumerate(filenames):
            _parse_xml_shedule(filename)
            self.stdout.write(self.style.SUCCESS(f'Successfully parsed {index}/{len(filenames)}, {filename}'))

    def _parse_xml_shedule(self, path):
        xml_root = ET.parse(filename).getroot()
        header = xml_root.attrib
        faculty_title = header.get('Фак')
        course_title = header.get('Курс')
        group_title = header.get('Название')
        faculty = models.Faculty.objects.get_or_create(title=faculty_title)
        courses = faculty