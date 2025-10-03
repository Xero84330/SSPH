from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    isauthor = models.BooleanField(default=False)
    country = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    
    BOOK_TYPES = [
        ('novel', 'Novel'),
        ('comic', 'Comic'),
        ('shortstory', 'Short Story'),
    ]

    AGE_RATINGS = [
        ('All Ages', 'All Ages'),
        ('13+', '13+'),
        ('16+', '16+'),
        ('18+', '18+'),
    ]

    bname = models.CharField("Book Name", max_length=100)
    btype = models.CharField("Type", choices=BOOK_TYPES, max_length=20)
    genre = models.CharField("Genre", max_length=50)
    agerating = models.CharField("Age Rating", choices=AGE_RATINGS, max_length=10)
    description = models.TextField("Description", max_length=1000)
    coverimage = models.ImageField("Cover Image", upload_to='images/')

    def __str__(self):
        return self.bname




class Chapter(models.Model):
    Book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapters")
    title = models.CharField(max_length=100)
    content = models.TextField()
    order = models.PositiveIntegerField()  

    def __str__(self):
        return f"{self.order}. {self.title}"

