import requests
from bs4 import BeautifulSoup
import datetime


HEADERS = {
    'Accept': 'text/html, */*; q=0.01',
    'Referer': 'https://rasp.rea.ru/',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36',
}

LESSON_TIMES = (
    "08:30 - 10:00", "10:10 - 11:40", "11:50 - 13:20", "14:00 - 15:30",
    "15:40 - 17:10", "17:20 - 18:50", "18:55 - 20:25", "20:30 - 22:00",
)


def fetch_schedule(group_name):
    params = (
        ('selection', group_name),
        ('weekNum', '-1'),
        ('catfilter', '0'),
    )
    shedule_url = 'https://rasp.rea.ru/Schedule/ScheduleCard'
    response = requests.get(shedule_url, headers=HEADERS, params=params)
    content = response.content.decode('utf-8')
    soup = BeautifulSoup(content, 'lxml')
    selector = ".task"
    lessons = soup.select(selector)
    all_lessons_serialized = []
    for lesson in lessons:
        lesson_title, lesson_type, lesson_place = str(lesson).split("<br/>")
        date = lesson_title.split('\'')[1]
        time_slot = lesson_title.split('\'')[3]
        lesson_serialized = fetch_lesson(group_name, date, time_slot)
        all_lessons_serialized.append(lesson_serialized)
    return all_lessons_serialized


def fetch_lesson(group_name, date, time_slot):
    params = (
        ('selection', group_name),
        ('date', date),
        ('timeSlot', time_slot),
    )

    response = requests.get('https://rasp.rea.ru/Schedule/GetDetails', headers=HEADERS, params=params)
    content = response.content.decode('utf-8')
    soup = BeautifulSoup(content, 'lxml')
    selector = "div"
    lessons = soup.select(selector)
    for index, lesson in enumerate(lessons, 1):
        title = lesson.select_one("h5").text
        if len(lessons) > 1:
            subgroup = index
        else: subgroup = "Вся группа"
        lesson_type = lesson.select_one("strong").text
        campus = str(lesson).split("Аудитория: ")[1].split(" корпус")[0]
        room = str(lesson).split("корпус - ")[1].split("<br/>")[0]
        teacher = lesson.select_one("a").text.split("school ")[1]
        lesson_as_dict = {
            'week': Номер недели (7),
            'day': add_weekday_to_date(date),
            'time': LESSON_TIMES[time_slot - 1],
            'title': title,
            'subgroup': subgroup,
            'campus': campus,
            'room': room,
            'lesson_number': time_slot,
            'lesson_type': lesson_type,
        }
        return lesson_as_dict # 1 словарь


def add_weekday_to_date(date_str):
    DATE_FORMAT = "%d.%m.%Y"
    WEEKDAYS = [
        'понедельник', 'вторник', 'среда',
        'четверг', 'пятница', 'суббота', 'воскресение'
    ]
    date = datetime.datetime.strptime(date_str, DATE_FORMAT)
    weekday = WEEKDAYS[date.weekday()]
    return f"{weekday}, {date}"


if __name__ == "__main__":
    group_name = "291д-07иб/18"
    mat = fetch_schedule(group_name)
    






