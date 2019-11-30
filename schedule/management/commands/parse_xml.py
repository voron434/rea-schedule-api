import os
import datetime
from os.path import isfile, join

import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.db import transaction

from core.settings import XML_PATH
from schedule import models


DATE_FORMAT = "%d.%m.%Y"


class Command(BaseCommand):
    help = 'Parses XML files provided by rea'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    @transaction.non_atomic_requests
    def handle(self, *args, **options):
        dump_path = options['path'] if 'path' in options.keys() else XML_PATH
        if dump_path and os.path.exists(dump_path):
            filenames = [join(dump_path, f) for f in os.listdir(dump_path) if isfile(join(dump_path, f))]
        else:
            self.stdout.write("Not able to find path to parse. Please, Specify it in settings.py or pass it as argument --path.")
            return
        # clear db?

        for index, filename in enumerate(filenames):
            self._parse_xml_schedule(filename)
            self.stdout.write(self.style.SUCCESS(f'Successfully parsed {index}/{len(filenames)}, {filename}'))

    def _parse_xml_schedule(self, path):
        xml_root = ET.parse(path).getroot()
        header = xml_root.attrib
        faculty_title = header.get('Фак')
        course_title = header.get('Курс')
        group_title = header.get('Название')
        faculty, is_created = models.Faculty.objects.get_or_create(title=faculty_title)
        course, is_created = models.Course.objects.get_or_create(faculty=faculty, title=course_title)
        group, is_created = models.Group.objects.get_or_create(course=course, title=group_title)
        for week in xml_root:
            week_num = week.attrib['Ном']
            for lesson in week:
                date_str = lesson[0].text
                date = datetime.datetime.strptime(date_str, DATE_FORMAT)
                lesson_num = lesson[1].text

                subgroup_num = lesson[2].text or None
                lesson_title = lesson[3].text
                lesson_type = lesson[4].text
                
                room_num = lesson[5].text
                room_campus = lesson[7].text
                classroom, is_created = models.Сlassroom.objects.get_or_create(campus=room_campus, room_num=room_num)

                teacher_name = lesson[6].text
                teacher, is_created = models.Teacher.objects.get_or_create(name=teacher_name)
                
                lesson, is_created = models.Lesson.objects.get_or_create(
                    teacher=teacher,
                    group=group,
                    week=week_num,
                    subgroup=subgroup_num,
                    classroom=classroom,
                    date=date,
                    lesson_num=lesson_num,
                    title=lesson_title,
                    lesson_type=lesson_type,
                )
