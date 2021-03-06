from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from firstapp.forms import Userregistrtion,UserExtendedForm,Productform
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from firstapp.models import Product,AuthUser,cart,order,User_extends
from django.core.paginator import Paginator
from django.db.models import Q,Sum

# Create your views here.

catogory=None
cart_option='Cart'

def indexview(request):
    user_count = User_extends.objects.all().count()
    return render(request,'index.html',{"userCount":user_count})

def registerview(request):
    form1 = Userregistrtion()
    form2 = UserExtendedForm()

    if request.method == "POST":
        form1 = Userregistrtion(request.POST)
        form2 = UserExtendedForm(request.POST,request.FILES)
        
        if form1.is_valid():
            form1.save()
            form1=Userregistrtion()
            if form2.is_valid():
                myfile = request.FILES['profile']
                fs = FileSystemStorage(location='static/profile_pic')
                filename = fs.save(myfile.name, myfile)
                form2.save(Filename=myfile.name or None)
                form2 = UserExtendedForm()
                return HttpResponseRedirect(reverse("login"))
            else:
                form2 = UserExtendedForm(request.POST,request.FILES)
        else:
            form1=Userregistrtion(request.POST)
    
    return render(request,'register.html',{'form1':form1,'form2':form2})


@login_required
def login_homeview(request):
    global catogory
    obj = Product.objects.all().filter(~Q(username__username=request.user.username) & ~Q(status='sold'))
    if catogory:
        obj = obj.filter(catogory=catogory)
    if request.GET.get('q'):
        querry = request.GET.get('q')
        obj = obj.filter(
                Q(username__first_name__icontains=querry)|
                Q(price__icontains=querry)|
                Q(Productname__icontains=querry)|
                Q(Description__icontains=querry)|
                Q(status__icontains=querry)|
                Q(Upload_date__icontains=querry)
            ).distinct()
    paginator = Paginator(obj, 12) 
    page = request.GET.get('page')
    obj = paginator.get_page(page)
    return render(request,'login_home.html',{'objects':obj,'pagenumber':obj})




@login_required
def product_detail_view(request,id=None):
    obj = Product.objects.get(Id=id)
    authobj = User_extends.objects.get(username=obj.username.username)
    userobj = AuthUser.objects.get(username=authobj.username)
    form = Productform(instance=obj)
    form1 = UserExtendedForm(instance=authobj)
    return render(request,'product_details.html',{'form':form,'form1':form1,'profile_picture':"/static/profile_pic/"+authobj.myfile,'userobj':userobj})


@login_required
def user_detail_view(request,id=None):
    obj = AuthUser.objects.get(id=id)
    authobj = User_extends.objects.get(username=obj.username)
    form = Userregistrtion(instance=obj)
    form1 = UserExtendedForm(instance=authobj)
    return render(request,'user_details.html',{'form':form,'form1':form1,'profile_picture':"/static/profile_pic/"+authobj.myfile})


@login_required
def cart_view(request):
    global cart_option
    total_item = 0
    total_amount= 0
    form,objects,obj,bill_context = None,None,None,None
    if request.method =="POST":
        form = Productform(request.POST,request.FILES)
        try:
            if form.is_valid():
                instance = Product.objects.create(Productname=(form.cleaned_data['Productname']),
                price=int(form.cleaned_data['price']),
                Description=str(form.cleaned_data['Description']),
                Upload_date=str(form.cleaned_data['Upload_date']),
                product_mage=request.FILES['product_mage'],
                username=AuthUser.objects.get(username=request.user.username),
                status=str(form.cleaned_data['status']),
                payment_mode=str(form.cleaned_data['payment_mode']),
                payment_qr=request.FILES['payment_qr'] or None,
                catogory=str(form.cleaned_data['catogory']))
                form = Productform()
                cart_option='Product-Post'
            else:
                form = Productform(request.POST,request.FILES)
                return render(request,'cart_view.html',{'form':form,'option':'post'})

        except Exception as P:
            print(P)

    if cart_option == "Cart":
        obj = cart.objects.filter(request_id__username=request.user.username)
        total_item = len(obj)
        total_amount = float((obj.aggregate(Sum('product_id__price')))['product_id__price__sum'] or 0 ) 
        if request.GET.get('q'):
            querry = request.GET.get('q')
            obj = obj.filter(
                    Q(request_id__first_name__icontains=querry)|
                    Q(product_id__price__icontains=querry)|
                    Q(product_id__Productname__icontains=querry)|
                    Q(product_id__Description__icontains=querry)|
                    Q(product_id__Upload_date__icontains=querry)
                ).distinct()
            total_item = len(obj)
            total_amount = (obj.aggregate(Sum("product_id__price")))['product_id__price__sum'] or 0

    elif cart_option =="Posted-Product":
        obj = Product.objects.filter(username__username=request.user.username)
        total_item = len(obj)
        total_amount = float(Product.objects.filter(Q(username__username=request.user.username)).aggregate(Sum('price'))['price__sum'] or 0)
        if request.GET.get('q'):
            querry = request.GET.get('q')
            obj = obj.filter(
                    Q(username__first_name__icontains=querry)|
                    Q(price__icontains=querry)|
                    Q(Productname__icontains=querry)|
                    Q(Description__icontains=querry)|
                    Q(status__icontains=querry)|
                    Q(Upload_date__icontains=querry)
                ).distinct()
            total_item = len(obj)
            total_amount = (obj.aggregate(Sum("price")))['price__sum'] or 0
            
        
    elif cart_option =="Requested-Product":
        obj = order.objects.filter(Q(product_id__username__username=request.user.username) &
        ~Q(product_id__status="sold"))
        total_item = order.objects.filter(Q(product_id__username__username=request.user.username) & ~Q(product_id__status="sold")).count()
        total_amount = float(order.objects.filter(Q(product_id__username__username=request.user.username) & ~Q(product_id__status="sold")).aggregate(Sum('product_id__price'))['product_id__price__sum'] or 0)
        if request.GET.get('q'):
            querry = request.GET.get('q')
            obj = obj.filter(
                    Q(user_id__first_name__icontains=querry)|
                    Q(product_id__price__icontains=querry)|
                    Q(product_id__Productname__icontains=querry)|
                    Q(product_id__Description__icontains=querry)|
                    Q(product_id__Upload_date__icontains=querry)
                ).distinct()
            total_item = len(obj)
            total_amount = (obj.aggregate(Sum("product_id__price")))['product_id__price__sum'] or 0

    elif cart_option == "My-Orders":
        obj = order.objects.filter(Q(user_id__username=request.user.username))
        total_item = len(obj)
        total_amount = float(order.objects.filter(Q(user_id__username=request.user.username)).aggregate(Sum('product_id__price'))['product_id__price__sum'] or 0)
       
        if request.GET.get('q'):
            querry = request.GET.get('q')
            obj = obj.filter(
                    Q(user_id__first_name__icontains=querry)|
                    Q(product_id__price__icontains=querry)|
                    Q(product_id__Productname__icontains=querry)|
                    Q(product_id__Description__icontains=querry)|
                    Q(product_id__Upload_date__icontains=querry)
                ).distinct()
            total_item = len(obj)
            total_amount = (obj.aggregate(Sum("product_id__price")))['product_id__price__sum'] or 0

    else:
        form = Productform()

    if cart_option == "Posted-Product" or cart_option =="Cart" or cart_option =="Requested-Product" or cart_option == "My-Orders" :
        paginator = Paginator(obj, 12) 
        page = request.GET.get('page')
        obj = paginator.get_page(page)
        bill_context = {'total_amount':total_amount,'total_item':total_item}
    return render(request,'cart_view.html',{'objects':obj,'pagenumber':obj,'form':form,'option':cart_option,'bill':bill_context})

def cart_add(request):
    if request.method=="POST" and request.is_ajax():
        try:
            cartinstance = cart.objects.create(product_id=Product.objects.get(Id=request.POST.get('productid')),request_id=AuthUser.objects.get(username=request.user.username))
            product_instance  = Product.objects.all().filter(Id=request.POST.get('productid')).update(status='cart')
        except Exception as p:
            print(p)

    return HttpResponse(None)

def cart_remove(request):
    if request.method=="POST" and request.is_ajax():
        try:
            product_instance  = Product.objects.all().filter(Id=request.POST.get('productid')).update(status='sell')
            cartinstance = cart.objects.get(cart_id=request.POST.get('cart_id')).delete()
        except Exception as p:
            print(p)
    return HttpResponse(None)

def create_order(request):
    if request.method=="POST" and request.is_ajax():
        try:
            orderinstance = order.objects.create(product_id=Product.objects.get(Id=request.POST.get('product_id')),user_id=AuthUser.objects.get(username=request.user.username))
            product_instance  = Product.objects.filter(Id=request.POST.get('product_id')).update(status='order')
            cartinstance = cart.objects.get(cart_id=request.POST.get('cart_id')).delete()
            # print(orderinstance,product_instance,cartinstance)
        except Exception as p:
            print(p)

    return HttpResponse(None)

def cancell_order(request):
    if request.method=="POST" and request.is_ajax():
        try:
            product_instance  = Product.objects.all().filter(Id=request.POST.get('product_id')).update(status='sell')
            orderinstance = order.objects.get(order_id=request.POST.get('order_id')).delete()
            cartinstance = cart.objects.create(product_id=Product.objects.get(Id=request.POST.get('product_id')),request_id=AuthUser.objects.get(username=request.user.username))
        except Exception as p:
            print(p)
    return HttpResponse(None)

def sell_product(request):
    if request.method=="POST" and request.is_ajax():
        try:
            product_instance  = Product.objects.all().filter(Id=request.POST.get('product_id')).update(status='sold')
            orderinstance = order.objects.filter(order_id=request.POST.get('order_id')).update(status='sold')
            cartinstance = cart.objects.filter(product_id__Id=request.POST.get('product_id')).delete()
        except Exception as p:
            print(p)
    return HttpResponse(None)


def remove_product(request):
    if request.method=="POST" and request.is_ajax():
        try:
            product_instance  = Product.objects.get(Id=request.POST.get('product_id')).delete()
        except Exception as p:
            print(p)
    return HttpResponse(None)

def catogories(request):
    global catogory
    if request.method=="POST" and request.is_ajax():
        try:
           catogory = request.POST.get('catogory')
           if catogory =='All':
               catogory=None
        except Exception as p:
            print(p)
    return HttpResponse(None)

def cart_options(request):
    global cart_option
    if request.method=="POST" and request.is_ajax():
        try:
           cart_option = request.POST.get('cart_option')
        except Exception as p:
            print(p)
    return HttpResponse(None)

@login_required
def logoutviews(request):
    logout(request)
    return HttpResponseRedirect(reverse('appstartpoint'))

