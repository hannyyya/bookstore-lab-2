import datetime
from passlib.hash import pbkdf2_sha256
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, request
from .models import Book, User, Orders
from django.core.paginator import Paginator

# получение данных из бд
def index(request):
    global cart
    try:
        cart = request.session['cart']
        name = request.session['userName']
        role = request.session['userRole']
    except:
        request.session['cart'] = []
        role = 0
        name = 'Гость'
    book = Book.objects.all()
    paginator = Paginator(book, 5)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)
    return render(request, "index.html", {"book": book, "pageObj": pageObj, "userRole": role, "userName": name})

def orderList(request):
    try:
        cart = request.session['cart']
        name = request.session['userName']
        role = request.session['userRole']
    except:
        request.session['cart'] = []
        role = 0
        name = 'Гость'
    orders = Orders.objects.all()
    return render(request, "orderList.html", {"orders": orders, "userRole": role, "userName": name, "cart": cart})

def cart(request):
    try:
        cart = request.session['cart']
        name = request.session['userName']
        role = request.session['userRole']
    except:
        request.session['cart'] = []
        role = 0
        name = 'Гость'
    bookForCart = []
    totalSum = 0
    for id in cart:
        book = Book.objects.get(id = id)
        bookForCart.append(book)
    for book in bookForCart:
        totalSum = totalSum + book.price
    print(totalSum)
    return render(request, "cart.html", {"bookForCart": bookForCart, "totalSum": totalSum, "userRole": role, "userName": name, "cart": cart})

def order(request):
    try:
        cart = request.session['cart']
        name = request.session['userName']
        role = request.session['userRole']
    except:
        request.session['cart'] = []
        role = 0
        name = 'Гость'
    bookForCart = []
    booksList = []
    booksListForOrder = ''
    totalSum = 0
    for id in cart:
        book = Book.objects.get(id = id)
        bookForCart.append(book)
        booksList.append(book.bookname)
    for book in bookForCart:
        totalSum = totalSum + book.price
    order = Orders()
    if request.method == "POST":
        order.userName = request.session['userName']
        order.date = datetime.datetime.now()
        order.totalSum = totalSum
        num = 1
        for i in booksList:
            booksListForOrder = booksListForOrder+str(num)+')'+str(i)+'\n'
            num = num+1
        order.booksList = booksListForOrder
        request.session['cart'] = []
        order.save()
        return HttpResponseRedirect("/")
    else:
        return render(request, "order.html", {"bookForCart": bookForCart, "totalSum": totalSum, "userRole": role, "userName": name, "cart": cart, "order": order})

def logout(request):
    try:
        del request.session['userRole']
    except KeyError:
        pass
    return HttpResponseRedirect("/")

# сохранение данных в бд
def create(request):
    book = Book()
    if request.method == "POST":
        book.bookname = request.POST.get("bookname")
        book.author = request.POST.get("author")
        book.price = request.POST.get("price")
        if (book.bookname != '' and book.author != '' and book.price != ''):
            book.save()
        return HttpResponseRedirect("/")
    else:
        return render(request, "edit.html", {"book": book})

def addInCart(request, id):
    cart = request.session['cart']
    cart.append(id)
    request.session['cart'] = cart
    return HttpResponseRedirect("/")

def registration(request):
    user = User()
    if request.method == "POST":
        user.userName = request.POST.get("userName")
        user.userPassword = pbkdf2_sha256.encrypt(request.POST.get("userPassword"), rounds=12000, salt_size=30)
        user.userRole = 2;
        if (user.userName != '' and user.userPassword != ''):
            user.save()
        return HttpResponseRedirect("/")
    else:
        return render(request, "registration.html", {"user": user})

def login(request):
    userForSession = User()
    if request.method == "POST":
        userName = request.POST.get("userName")
        userPassword = request.POST.get("userPassword")
        userForSession = User.objects.get(userName = userName)
        if (pbkdf2_sha256.verify(userPassword, userForSession.userPassword)):
            request.session['userName'] = userForSession.userName
            request.session['userRole'] = userForSession.userRole
        return HttpResponseRedirect("/")
    else:
        return render(request, "login.html")

# изменение данных в бд
def edit(request, id):
    try:
        book = Book.objects.get(id=id)

        if request.method == "POST":
            book.bookname = request.POST.get("bookname")
            book.author = request.POST.get("author")
            book.price = request.POST.get("price")
            if (book.bookname != '' and book.author != '' and book.price != ''):
                book.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"book": book})
    except Book.DoesNotExist:
        return HttpResponseNotFound("<h2>Book not found</h2>")

def editUser(request):
    try:
        user = User.objects.get(userName=request.session['userName'])

        if request.method == "POST":
            user.userName = request.POST.get("userName")
            password = request.POST.get("userPassword")
            user.userPassword = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=30)
            if (user.userName != '' and user.userPassword != ''):
                user.save()
                request.session['userName'] = user.userName
            return HttpResponseRedirect("/")
        else:
            return render(request, "personalArea.html", {"user": user})
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")

# удаление данных из бд
def delete(request, id):
    try:
        book = Book.objects.get(id=id)
        book.delete()
        return HttpResponseRedirect("/")
    except Book.DoesNotExist:
        return HttpResponseNotFound("<h2>Book not found</h2>")



'''
def homePage(request):
    book = Book.objects.all()
    asyncio.run(acreate_person())
    #book1 = Book.objects.create(bookname="Tom", author='sdad', price=123)
    book2 = Book.objects.get(id=3)
    return HttpResponse(book2.bookname)
async def acreate_person():
    person = await Book.objects.acreate(bookname="Tom", author='sdad', price=123)

'''