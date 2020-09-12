from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import *
import requests
import json
headers = { "X-Api-Key": "381612a94bc714916aee910d2bf5c363",
            "X-Auth-Token": "f50c72ccd3ea8f36b0b15a7675a850dc"}

def Home(request):
     return render(request,"index.html")






def Contact(request):
     return render(request,"contact.html")

def About(request):
     return render(request,"about.html")



def All_Movies(request):
    cat = Movie_Category.objects.all()
    movies = Movies.objects.all().order_by("-id")[:9]
    d = {
        "cats":cat, "movies":movies
    }
    return render(request, "movie_category.html", d)


def Movie_Details_Page(request, m_id):
    movie = Movies.objects.filter(id = m_id).first()
    casts = Cast.objects.filter(movie = movie)
    d = {
        "movie":movie, "casts":casts
    }
    return render(request, "movie_single.html", d)





from datetime import date, timedelta
def Movie_Confirmation(request, m_id):
    movie = Movies.objects.filter(id = m_id).first()
    st = ShowTime.objects.filter(movie = movie)
    Dates = []
    ShowTime1 = []

    today = date.today()
    for i in range(4):
        Dates.append(today + timedelta(days=i))


    for d in Dates:
        # 29
        temp = []
        TempSt = []
        talkies = ""
        for i in st:
            if d == i.date:
                if i.talkies.name != talkies:
                    if len(talkies) > 2:
                        TempSt.append((talkies, temp))
                    talkies = i.talkies.name
                    temp = []
                    temp.append(i)
                else:
                    temp.append(i)
        TempSt.append((talkies, temp))
        ShowTime1.append(TempSt)


    data = zip(Dates, ShowTime1)
    data2 = zip(Dates, ShowTime1)
    return render(request, "movie_booking.html", {"data":data, "data2":data2})





"""def SeatBookingPage(request,m_id):
    movie = Movies.objects.filter(id=m_id).first()
    d={
        "moviee": movie
    }
    return render(request,"seat_booking.html",d)"""

def Login(request):
    error = False
    if request.method == "POST":
        un = request.POST["un"]
        ps = request.POST["ps"]
        usr = authenticate(username = un, password = ps)
        if usr:
            login(request, usr)
            return redirect("home")
        error = True
    return render(request, "login.html", {"error": error})


def Logout(request):
    logout(request)
    return redirect("login")



def SignUP(request):
    error = False
    if request.method == "POST":
        d = request.POST
        name = d["name"]
        un = d["un"]
        ps = d["ps"]
        email = d["email"]
        add = d["add"]
        number = d["number"]
        usr = User.objects.filter(username = un)

        if not usr:
            user = User.objects.create_user(un, email, ps)
            UserDetails.objects.create(usr=user, name=name,
                                       number=number, email=email, address=add)
            return redirect("login")
        error = True
    return render(request, "signup.html", {"error":error})



def Delete_Album(request,m_id):
    movie = Movies.objects.filter(id = m_id)
    movie.delete()
    return redirect('home')


################ Admin Functions ........###
def Admin_Add_Cat(request):
    error = False
    if request.method == "POST":
        cat = request.POST["cat"].strip().capitalize()
        cats = Movie_Category.objects.filter(name=cat)
        if not cats:
            Movie_Category.objects.create(name=cat)
            return redirect("home")
        error = True

    return render(request, "add_cat.html",{'error':error})

def Admin_Add_Movie(request):
    form = Add_Movie_Form()
    categories = Movie_Category.objects.all()
    if request.method == "POST":
        form = Add_Movie_Form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            cat = request.POST["cat"]
            cat = Movie_Category.objects.filter(id = cat).first()
            data.cat = cat
            data.save()
            return redirect("all_movies")
    d = {"form":form, "cats":categories}
    return render(request, "add_movie.html",d)




def SeatBookingPage(request, m_id):
    st = ShowTime.objects.filter(id = m_id).first()
    sheets = Sheets.objects.filter(st=st)
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        data = request.POST
        St = data.getlist("cb")
        usr = request.user
        St1 = Sheets.objects.filter(usr=usr, status="Pending")
        for i in St1:
            i.status = "Blank"
            i.save()

        for i in St:
            st = Sheets.objects.filter(id = i).first()
            st.usr = request.user
            st.status = "Pending"
            st.save()


        return redirect("payment")
        #return redirect("SeatBookingPage", m_id)


    d = {
        "s1":sheets[:22],
        "s2":sheets[22:44],
        "s3":sheets[44:66],
        "s4":sheets[66:],
        "st":st
    }

    return render(request, "seat_booking.html", d)



def Admin_Add_ShowTime(request):
    talk  = Talkies.objects.all()
    movies = Movies.objects.all()
    if request.method == "POST":
        d = request.POST
        tk = d["talkies"]
        mv = d["movie"]
        dt = d["date"]
        tm = d["time"]
        rs = d["rs"]
        talkies = Talkies.objects.filter(id = tk).first()
        movie = Movies.objects.filter(id = mv).first()
        St = ShowTime.objects.create(talkies=talkies, movie=movie, time=tm,
                                     Rs= rs, date=dt)
        for i in range(1,89):
            Sheets.objects.create(talkies=talkies, st=St, sn = i)
        return redirect("home")

    d = {
        "talk":talk, "movies":movies
    }
    return render(request, "add_st.html", d)


def Create_Sheets(request):
    for i in range(1,89):
        Sheets.objects.create(sn = i)
    return redirect("home")



def MakePayment(request):
    usr = request.user
    St = Sheets.objects.filter(usr=usr, status="Pending")
    Rs = 0
    for i in St:
        Rs = Rs + i.st.Rs
    payload = {
        'purpose': 'Movie Booking',
        'amount': str(Rs),
        'buyer_name': request.user.username,
        'email': request.user.email,
        'phone': request.user.userdetails_set.first().number,
        'redirect_url': 'http://127.0.0.1:8000/PayCheck/{}/'.format(request.user.username),
        'send_email': 'True',
        'send_sms': 'True',
        'allow_repeated_payments': 'False',
    }
    response = requests.post("https://www.instamojo.com/api/1.1/payment-requests/", data=payload, headers=headers)
    obj = json.loads(response.text)
    print(obj)
    Url= obj["payment_request"]["longurl"]
    Idd = obj["payment_request"]["id"]
    Di = Payment_Id.objects.filter(Usr = usr)
    Di.delete()
    Payment_Id.objects.create(Usr=usr, PayId=Idd)
    return redirect(Url)


from django.http import HttpResponse
def PayChack(request, Usr):
    usr = User.objects.filter(username = Usr).first()
    Di = Payment_Id.objects.filter(Usr=usr).first()
    response = requests.get("https://www.instamojo.com/api/1.1/payment-requests/{}/".format(Di.PayId),headers=headers)
    obj = json.loads(response.text)
    Status = obj["payment_request"]["payments"][0]["status"]
    if Status == "Failed":
        return HttpResponse("<h1>Payment Failed</h1>")
    else:
        return HttpResponse("<h1>Payment Done... @@</h1>")