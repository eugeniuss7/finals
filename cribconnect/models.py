from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = {
    "MALE": "Male",
    "FEMALE": "Female"
}

# Create your models here.

class rateReviews(models.Model):
    rating = models.PositiveSmallIntegerField()
    review = models.CharField(max_length=255, blank=True)

class account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    phoneNumber = models.IntegerField(null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=8, null=True, blank=True, choices=GENDER_CHOICES)
    is_verified = models.BooleanField(default=0, blank=True)
    is_landowner = models.BooleanField(default=0, null=True, blank=True)
    profilePicture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    rating = models.ForeignKey(rateReviews, on_delete=models.CASCADE, related_name="urating", null=True)
    
    def __str__(self):
        return f"[{self.pk}] {self.user.last_name}"

class listingAddress(models.Model):
    houseNumber = models.CharField(max_length=16)
    street = models.CharField(max_length=64)
    barangay = models.CharField(max_length=64)
    municipality = models.CharField(max_length=64)
    province = models.CharField(max_length=64)
    postalCode = models.SmallIntegerField()
    
class listingFeatures(models.Model):
    pets = models.BooleanField()
    nearbyLaundry = models.BooleanField()
    nearbyTransit = models.BooleanField()
    wifi = models.BooleanField()
    bathroom = models.BooleanField()
    kitchen = models.BooleanField()
    airConditioning = models.BooleanField()
    parking = models.BooleanField()
    curfew = models.BooleanField()
    visitor = models.BooleanField()
    maleOnly = models.BooleanField()
    femaleOnly = models.BooleanField()
    accessibility = models.BooleanField()

class paymentTerms(models.Model):
    advancePayment = models.IntegerField()
    securityDeposit = models.IntegerField()
    minimumStay = models.IntegerField()
    utilityPayment = models.IntegerField(blank=True)

class imageGallery(models.Model):
    image1 = models.ImageField(upload_to='listing_image/', null=True, blank=True)
    image2 = models.ImageField(upload_to='listing_image/', null=True, blank=True)
    image3 = models.ImageField(upload_to='listing_image/', null=True, blank=True)
    image4 = models.ImageField(upload_to='listing_image/', null=True, blank=True)

class listing(models.Model):
    landowner = models.ManyToManyField(account)
    address = models.ForeignKey(listingAddress, on_delete=models.CASCADE)
    terms = models.ForeignKey(paymentTerms, on_delete=models.CASCADE)
    features = models.ForeignKey(listingFeatures, on_delete=models.CASCADE, null=True, blank=True)
    capacity = models.IntegerField()
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=16)
    price = models.BigIntegerField()
    dimension = models.IntegerField()   
    primaryImage = models.ImageField(upload_to='listing_image/')
    images = models.OneToOneField(imageGallery, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=1)
    rating = models.ForeignKey(rateReviews, on_delete=models.CASCADE, related_name="prating", null=True)
    
    def __str__(self):
        return f"{self.landowner}: {self.description}"

class inquiryRequest(models.Model):
    from_userID = models.ForeignKey(account, on_delete=models.CASCADE, related_name="from_userID")
    to_userID = models.ForeignKey(account, on_delete=models.CASCADE, related_name="to_userID")
    listingID = models.ForeignKey(listing, on_delete=models.CASCADE, null=True)
    requestType = models.CharField(max_length=16)
    requestStatus = models.CharField(max_length=16, default="Pending")

    def __str__(self):
        return f"[{self.pk}] {self.from_userID} TO {self.to_userID}"


class cribshare(models.Model):
    userID = models.ForeignKey(account, on_delete=models.CASCADE)
    listingID = models.ForeignKey(listing, on_delete=models.CASCADE, related_name="listings")
    
    def __str__(self):
        return f"[{self.pk}] {self.userID}: {self.listingID.description}"
    
class tenant(models.Model):
    userID = models.ForeignKey(account, on_delete=models.CASCADE)
    listingID = models.ForeignKey(listing, on_delete=models.CASCADE)
    status = models.CharField(max_length=16)

class forVerification(models.Model):
    userID = models.ForeignKey(account, on_delete=models.CASCADE)
    frontPhoto = models.ImageField(upload_to='for_verification/')
    backPhoto = models.ImageField(upload_to='for_verification/')