import math
from django.shortcuts import redirect, render ,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from . models import Hotel , hotelBooking , Amenities
from django.contrib.auth.decorators import login_required 
from django.db.models import Q 
# from .decorators




# @login_required(login_url='/login')
def home(request):
    hotels= Hotel.objects.all()
    amenities = Amenities.objects.all()
    
# search by destination and amenities Functionality
    location = request.GET.get('location')
    amenities_list = request.GET.getlist('amenities')
    if len(amenities_list):
        hotels = hotels.filter( Q(amenities__amenity__in= amenities_list) & Q(location__icontains =location))

        # following code is for removing duplicate data. / can be resolved by .distinct()
        result= []
        [result.append(i) for i in hotels if i not in result]
        hotels = result
        print("Am and lo search" , hotels)

   
       


  

# Search Functionality
    search = request.GET.get('search')
    if search:
        hotels = hotels.filter(Q(name__icontains= search) |
                               Q(amenities__amenity__icontains= search)|
                               Q(location__icontains = search)).distinct()

        # fixing  Redendency bug. / has resolved by .distinct()
        # result = list(OrderedDict.fromkeys(hotels))
        # hotels = result

      
# sort_by Functionality
    sort_by = request.GET.get('sort_by')
    if sort_by:
        if sort_by == 'ASD':
           hotels = hotels.order_by('price')

        elif sort_by == 'DSC':
           hotels = hotels.order_by('-price')

    if len(hotels) == 0:
            messages.warning(request ,'Zero Results')

       




# pagination logic 
    result_per_page = 4
    page= request.GET.get('page')
    print(f" This is Page {page}")

    if page is None :
        page = 1
    else:
        page = int(page)

   

    length = len(hotels)
    print(f'length of all posts {length}')

    hotels = hotels[(page-1)*result_per_page : page*result_per_page]

    prev , nxt = None , None

    if page >1:
        prev = page -1
        
        
    elif page < (math.ceil(length/result_per_page)):
        nxt = page +1
        
    else:
        page = None

    
# filter logic 

    checkin= request.GET.get('checkin')
    checkout= request.GET.get('checkout')
    qs = hotelBooking.objects.filter(
            start_date = checkin ,
            end_date = checkout
        ).values('hotel__name')

    hotels = Hotel.objects.exclude(name__in =qs.values_list('hotel__name', flat=True))
     

       
    print(f"{qs} filtered by dates ")
    print(f"{hotels} in new qs ")




    context= {
        'hotels' : hotels ,
        'amenities': amenities,
        'sort_by' : sort_by ,
        'search' : search ,
        'nxt'  : nxt,
        'prev': prev ,
    }
    return render(request , 'home.html', context)



@login_required(login_url='/login')
def about(request):
    return render(request , 'about.html')



def logout_user(request):
    try:
        logout(request)
        return redirect('/login/')
    except Exception as e:
        print(e)


def register_page(request):
    if request.method == "POST":
        username= request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user_obj = User.objects.filter(username=username)
        if user_obj.exists():
            messages.warning(request ,'User already exists.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user= User.objects.create(username= username , email= email)
        user.set_password(password)
        user.save()
        messages.success(request ,'Account created successfully.')
        return redirect('login') 

        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



    return render(request , 'register.html')



def check_booking(start_date , end_date , room_count , uid):
    querySet = hotelBooking.objects.filter(
        start_date = start_date,
        end_date = end_date ,
        hotel__uid = uid
    )
    if len(querySet) >= room_count:
        return False

    return True



def details(request, uid):
    hotel = Hotel.objects.get(uid = uid)
    context = {
        'hotel' : hotel ,
    }
    try:
        if request.method == 'POST':
            checkin = request.POST.get('checkin')
            checkout = request.POST.get('checkout')
            room_count = hotel.room_count

           
            if checkin and checkout :
                if check_booking(checkin ,checkout, room_count ,uid ) :
                
                    hotelBooking.objects.create(hotel=hotel , user=request.user, start_date=checkin,
                    end_date=checkout, booking_type= 'pre_paid')

                    messages.success(request ,'Booking has been done!')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                messages.warning(request ,'All rooms are reserved !')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else :
                messages.debug(request ,'Dates are missing')


    except Exception as e :
        messages.debug(request ,'Dates are missing')

        print(e)

    return render(request, 'detail.html', context)




def login_page(request):
    if request.method == "POST":
        username= request.POST['username']
        password = request.POST['password']

        user_obj = User.objects.filter(username=username)

        if not user_obj.exists():
            messages.warning(request ,'User does not exist.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return redirect(request, '/login_page')

        user_obj = authenticate(username= username, password=password)
        if not user_obj:
            messages.warning(request ,'Invalid password or username')
            # return redirect(request, '/login_page')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        login(request ,user_obj)
        return redirect('home') 

    return render(request , 'login.html')