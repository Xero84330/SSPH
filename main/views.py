from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserCreationForm
from .models import User, Book, Chapter
from django.db.models import Max


# Create your views here.

# readers function
def home(request):
    book = Book.objects.all()
    return render(request, 'reader/rhome.html', {'books': book})

def browse(request):
    return render(request, 'reader/rbrowse.html')

def ranking(request):
    return render(request, 'reader/rranking.html')

def contest(request):
    return render(request, 'reader/rcontest.html')

def about(request):
    return render(request, 'reader/rabout.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")   # email instead of username
        password = request.POST.get("password")

        user_obj = authenticate(request, email=email, password=password)

        if user_obj is not None:
            login(request, user_obj)
            messages.success(request, f"Welcome {user_obj.username}")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "reader/login.html")

def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")

        new_user = User.objects.create_user(email=email, username=username, password=password)
        new_user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "reader/signup.html")

def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logged out successfully!")
    return redirect('home')

def rbook(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    chapters = book.chapters.order_by('order')

    return render(request, 'reader/rbook.html', {
        'book': book,
        'chapters': chapters,
    })

def rread(request, book_id, chapter_id):
    book = get_object_or_404(Book, id=book_id)
    chapter = get_object_or_404(Chapter, id=chapter_id, Book=book)  
    prev_chapter = Chapter.objects.filter(Book=book, order__lt=chapter.order).order_by('-order').first()
    next_chapter = Chapter.objects.filter(Book=book, order__gt=chapter.order).order_by('order').first()


    return render(request, "reader/rread.html", {
        "book": book,
        "chapter": chapter,
        "chapters": book.chapters.all().order_by("order"),
        "prev_chapter": prev_chapter,
        "next_chapter": next_chapter,
    })


# author functions

def create(request):
    user_books = Book.objects.filter(user=request.user)
    return render(request, 'author/adashboard.html', {'books': user_books})

def statistics(request):
    return render(request, 'author/astats.html')

def payment(request):
    return render(request, 'author/apayment.html')

def abookpage(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    chapters = book.chapters.order_by('order')

    return render(request, 'author/abookpage.html', {
        'book': book,
        'chapters':chapters,
    })

def addbook(request): 
    if request.method == 'POST':
        bname = request.POST.get('bname')
        btype = request.POST.get('btype')
        genre = request.POST.get('genre')
        agerating = request.POST.get('agerating')
        description = request.POST.get('description')
        coverimage = request.FILES.get('coverimage')

        # Tie the book to the logged-in user
        Book.objects.create(
            user=request.user,
            bname=bname,
            btype=btype,
            genre=genre,
            agerating=agerating,
            description=description,
            coverimage=coverimage
        )
        messages.success(request, f'Book "{bname}" has been created successfully!')
        return redirect('create')

    # Show books belonging to logged-in user
    user_books = Book.objects.filter(user=request.user)
    return render(request, 'author/addbook.html', {'books': user_books})


def addchapter(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            # Auto-increment order
            last_order = book.chapters.aggregate(max_order=Max('order'))['max_order'] or 0
            Chapter.objects.create(
                Book=book,
                title=title,
                content=content,
                order=last_order + 1
            )
            messages.success(request, f'Chapter "{title}"added sucessfully')
            return redirect('abookpage', book_id=book.id)

    return render(request, "author/addchapter.html", {"book": book})

def delete_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    book_id = chapter.Book_id  # so we know where to redirect back
    chapter.delete()
    messages.success(request, "Chapter deleted successfully.")
    return redirect("abookpage", book_id=book_id)

def edit_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    book = chapter.Book  # get the related book

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            chapter.title = title
            chapter.content = content
            chapter.save()
            messages.success(request, "Chapter updated successfully.")
            return redirect("abookpage", book_id=book.id)

    return render(request, "author/addchapter.html", {"chapter": chapter, "book": book})

def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)

    if request.method == 'GET':
        book.delete()
        messages.success(request, f'Book "{book.bname}" deleted successfully!')
        return redirect('create')