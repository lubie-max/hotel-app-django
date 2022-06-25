
from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.


class BaseModel(models.Model):
    uid= models.UUIDField(primary_key=True,default=uuid.uuid4,  editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta :
        abstract= True


class Amenities(BaseModel):
    amenity = models.CharField(max_length=200) 


    class Meta:
        managed = True
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'
        

    def __str__(self) -> str:
        return self.amenity

    




class Hotel(BaseModel):

    name= models.CharField(max_length=150)
    price = models.IntegerField()
    location = models.CharField(max_length=200, default='Mumbai')
    description = models.TextField()
    amenities = models.ManyToManyField(Amenities,related_name='hotel_amenties')
    room_count = models.IntegerField(default=10)


    def __str__(self) -> str:
        return self.name


class hotelImages(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_img')
    image= models.ImageField(upload_to= 'media/hotel')

    
    class Meta:
        managed = True
        verbose_name = 'Images'
        verbose_name_plural = 'Hotel Images'

    def __str__(self) -> str:
        return  f" {self.hotel} -{self.image}"
        


class hotelBooking(BaseModel):
    hotel= models.ForeignKey(Hotel, related_name='hotel_booking', on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE , related_name='user_booking')
    start_date = models.DateField()
    end_date = models.DateField()
    booking_type = models.CharField(max_length=200, choices=(('pre_paid','pre_paid'),('post_paid','post_paid')) )

    def __str__(self) -> str:
        return  f"{self.user}- {self.hotel} - {self.booking_type}"
        





