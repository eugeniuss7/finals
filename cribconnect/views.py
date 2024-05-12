from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.   
def index(request):
    if request.user.is_authenticated:
        if request.user.email == "":
            return HttpResponseRedirect(reverse("accountform"))
        elif request.GET.get("searchval"):
            searchval = request.GET.get("searchval")
            return render(request, searchval, "resultpage.html")
        context = {
            'listings': listing.objects.all(), 'account': account.objects.filter(user=request.user).first()
        }
        
        return render(request, "cribconnect/index.html", context)
    return HttpResponseRedirect(reverse("guest"))

def cribshare_view(request):
    if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
    return render(request, "cribconnect/cribshare_view.html", {"cribshare": cribshare.objects.all()})

def module2(request):
    pic_form = profileForm()
    id_form = idForm()
    cur_user = request.user.account
    property = listing.objects.filter(landowner = cur_user)
    tenants_count = tenant.objects.filter(listingID = property.last()).all().count()
    account.objects.filter()
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("guest"))
    elif request.method == "POST" or request.FILES:
        delete_listing = request.POST.get("delete-listing")
        urate = request.POST.get("user-rating")
        ureview = request.POST.get("user-review")
        lrate = request.POST.get("property-rating")
        lreview = request.POST.get("property-rating")
        response = request.POST.get("response")
        inquiry_id = request.POST.get("inquiryid")
        edit_phone = request.POST.get("editPhone")
        edit_email = request.POST.get("editEmail")
        dp = request.POST.get("dp")
        if response == "Accepted":
            inquiry = inquiryRequest.objects.filter(pk=inquiry_id).last()
            inquiryRequest.objects.filter(pk=inquiry.id).update(requestStatus=response)
            if inquiry.requestType == "Standard":
                tenant.objects.create(userID=inquiry.from_userID, listingID=inquiry.listingID, status="Settled")
            elif inquiry.requestType == "Cribshare":
                cribshare.objects.create(userID=inquiry.from_userID, listingID=inquiry.listingID)
        elif response == "Rejected":
            inquiry = inquiryRequest.objects.filter(from_userID=cur_user).last()
            inquiryRequest.objects.filter(pk=inquiry.id).update(requestStatus=response)
        elif delete_listing:
            listing.objects.filter(pk=delete_listing).delete()
        elif urate:
            rateReviews.objects.create(rating=urate, review=ureview)
            account.objects.filter(pk=tenant.objects.filter(listingID=property.first()).first().userID.id).update(rating=rateReviews.objects.last())
        elif lrate:
            rateReviews.objects.create(rating=lrate, review=lreview)
            listing.objects.filter(pk=tenant.objects.filter(userID=cur_user).first().listingID.id).update(rating=rateReviews.objects.last())
        elif edit_phone:
            account.objects.filter(pk=cur_user.id).update(phoneNumber=edit_phone)
        elif edit_email:
            User.objects.filter(pk=request.user.id).update(email=edit_email)
        elif dp:
            pic_form = profileForm(request.POST, request.FILES, instance=account.objects.filter(pk=cur_user.id).first())
            if pic_form.is_valid():
                pic_form.save()
        else:
            forVerification.objects.create(userID=cur_user)
            id_form = idForm(request.POST, request.FILES, instance=forVerification.objects.filter(userID=cur_user.id).last())
            if id_form.is_valid():
                id_form.save()
    context = {
               "listings": property.all(),
               "account": account.objects.filter(user = request.user).first(),
               'requests': inquiryRequest.objects.all(),
               'tenants': tenant.objects.filter(listingID=property.first()).all(),
               'tenants_count': tenants_count,
               'rating': rateReviews.objects.all(),
               'id_form': id_form,
               'pic_form': pic_form
               }
    return render(request, "cribconnect/module2.html", context)

def listingpage(request, pk):
    listingdetails = listing.objects.get(id=pk)
    if request.user.is_authenticated:
        if request.method == "POST":
            from_userID = request.user.account
            to_userID = account.objects.filter(listing=listingdetails).last()
            requestType = request.POST.get('requestType')
            inquiryRequest.objects.create(from_userID=from_userID, to_userID=to_userID, listingID=listingdetails, requestType=requestType)
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
    context={
        'listing': listingdetails, 'address': listingAddress.objects.all(),
        'terms': paymentTerms.objects.all(), 'images': imageGallery.objects.all(),
        'rating': rateReviews.objects.all(), 'cribshare': cribshare.objects.filter(listingID=listingdetails).all(),
        'account': account.objects.filter(pk=listingdetails.landowner.first().id).first()
    }
    
    return render(request, "cribconnect/viewproperty.html", context)

def propertylisting(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("guest"))
    elif request.user.account.is_landowner == 0:
        return HttpResponseRedirect(reverse("index"))
    elif request.method == "POST":
        description = request.POST.get("description")
        houseNumber = request.POST.get("houseNumber")
        street = request.POST.get("street")
        barangay = request.POST.get("barangay")
        municipality = request.POST.get("municipality")
        province = request.POST.get("province")
        postalCode = request.POST.get("postalCode")
        price = request.POST.get("price")
        capacity = request.POST.get("capacity")
        dimension = request.POST.get("dimension")
        type = request.POST.get("type")
        advancePayment = request.POST.get("advancePayment")
        securityDeposit = request.POST.get("securityDeposit")
        minimumStay = request.POST.get("minimumStay")
        utilityPayment = request.POST.get("utilityPayment")
        
        gform = galleryForm(request.POST, request.FILES)
        if gform.is_valid():
            gform.save()
        listingAddress.objects.create(houseNumber=houseNumber, street=street, barangay=barangay, municipality=municipality, province=province, postalCode=postalCode,)
        paymentTerms.objects.create(advancePayment=advancePayment, securityDeposit=securityDeposit, minimumStay=minimumStay, utilityPayment=utilityPayment)
        user = account.objects.filter(id = request.user.account.id)
        instance = listing.objects.create(description=description, price=price, capacity=capacity, dimension=dimension, type=type, 
                                          address=listingAddress.objects.filter(houseNumber=houseNumber).last(), 
                                          terms=paymentTerms.objects.filter(advancePayment=advancePayment).last(), 
                                          images = imageGallery.objects.last(), 
                                          features=listingFeatures.objects.last())
        instance.landowner.set(user)
        listingID = listing.objects.filter(landowner=request.user.account).last()
        form = imageForm(request.POST, request.FILES, instance = listingID)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Property successfully listed.')
            return redirect('index')
            
    else:
        form=imageForm()
        gform=galleryForm()
    context = {'form': form, 'gform': gform}
    return render(request, "cribconnect/listproperty.html", context)
    

def createaccount(request):
    form = createUser()

    if request.method == "POST":
        form = createUser(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Account successfully created.')
            return redirect('index')
        
    context = {'registerform': form}
    return render(request, "cribconnect/createaccount.html", context=context)

def guest_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, f'Invalid credentials, please try again.')
        
    return render(request, "cribconnect/guest.html", {"listings": listing.objects.all(), "address": listingAddress.objects.all(), 'terms': paymentTerms.objects.all()})

def account_form(request):
    if request.method == "POST" or request.FILES:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        age = request.POST['age']
        phoneNumber = request.POST['phoneNumber']
        email = request.POST['email']
        is_landowner = request.POST.get('is_landowner')


        account.objects.create(user=request.user, gender=gender, age=age, phoneNumber=phoneNumber, is_landowner=is_landowner)
        User.objects.filter(id=request.user.id).update(email=email, first_name=first_name, last_name = last_name)
        form=profileForm(request.POST, request.FILES, instance=account.objects.filter(pk=request.user.account.id).first())
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        form = profileForm()
    
    return render(request, "cribconnect/accountform.html", {'form': form})

def logout_view(request):
    logout(request)
    return render(request, "cribconnect/guest.html")