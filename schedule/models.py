from django.db import models


FACULTY_ACRONYMS = {
    'факультет "Международная школа бизнеса и мировой экономики"':'МШБиМЭ',
    'факультет "Экономики и права"':'ФЭП',
    'факультет гостинично-ресторанной, туристической и спортивной индустрии':'ГРТСИ',
    'факультет маркетинга':'ФМа',
    'факультет математической экономики, статистики и информатики':'ФМЭСИ',
    'факультет менеджмента':'ФМе',
    'факультет экономики торговли и товароведения':'ФЭТТ',
    'финансовый факультет':'ФФ',
    'факультет дистанционного обучения':'Дистанционного обучения',
    'факультет "Плехановская школа бизнеса Integral"':'школа бизнеса Integral',
    'факультет бизнеса "Капитаны"':'Капитаны',
    'факультет бизнеса "КАПИТАНЫ"':'КАПИТАНЫ',
    'институт цифровой экономики и информационных технологий': 'ИЦЭИТ (ФМЭСИ)',
    'факультет бизнеса и дополнительного образования': 'ФБиДО'
}


LESSON_TIMES = (
    "08:30 - 10:00", "10:10 - 11:40", "11:50 - 13:20", "14:00 - 15:30",
    "15:40 - 17:10", "17:20 - 18:50", "18:55 - 20:25", "20:30 - 22:00",
)


class Faculty(models.Model):
    title = models.CharField(max_length=150)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.acronym)

    @property
    def acronym(self):
        if self.title in FACULTY_ACRONYMS.keys():
            return FACULTY_ACRONYMS[self.title] 
        else:
            return [word[0] for word in self.title.upper().split()]


class Course(models.Model):
    title = models.CharField(max_length=30)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


# class EducationForm(models.Model):
#     title = models.CharField(max_length=30)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.title)

#     @property
#     def faculty(self):
#         return self.course.faculty


class Group(models.Model):
    title = models.CharField(max_length=50)
    # education_form = models.ForeignKey(EducationForm, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    @property
    def faculty(self):
        return self.course.faculty
    

    # @property
    # def faculty(self):
    #     return self.education_form.course.faculty

    # @property
    # def course(self):
    #     return self.education_form.course

    def __str__(self):
        return str(self.title)


class Teacher(models.Model):
    name = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Сlassroom(models.Model):
    room_num = models.CharField(max_length=50)
    campus = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.room_num}"


class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)
    week = models.IntegerField()
    subgroup = models.CharField(max_length=50, null=True, blank=True)
    classroom = models.ForeignKey(Сlassroom, on_delete=models.CASCADE)
    date = models.DateField(max_length=50)
    lesson_num = models.IntegerField()
    title = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True)

    @property
    def date_formatted(self):
        return self.date.strftime("%d.%m.%Y")

    @property
    def time(self):
        return LESSON_TIMES[self.lesson_num]