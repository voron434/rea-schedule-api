from django.db import models


class Faculty(models.Model):
    title = models.CharField(max_length=150)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class Course(models.Model):
    title = models.CharField(max_length=30)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class EducationForm(models.Model):
    title = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    @property
    def faculty(self):
        return self.course.faculty


class Group(models.Model):
    title = models.CharField(max_length=50)
    education_form = models.ForeignKey(EducationForm, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    @property
    def faculty(self):
        return self.education_form.course.faculty

    @property
    def course(self):
        return self.education_form.course

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


class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)
    week = models.IntegerField()
    subgroup = models.CharField(max_length=50, null=True, blank=True)
    classroom = models.ForeignKey(Сlassroom, on_delete=models.CASCADE)
    date = models.DateField(max_length=50)
    time = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True)

    @property
    def date_formatted(self):
        return self.date.strftime("%d.%m.%Y")
    