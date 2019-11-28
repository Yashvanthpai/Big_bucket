from django.db import models

# Create your models here.
class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'
    
    def __str__(self):
        return str(self.username)+"( "+str(self.first_name)+" )"

    
class User_extends(models.Model):
    username = models.CharField(max_length=150,primary_key=True)
    gender = models.CharField(max_length=10,choices=[("male",'Male'),('female','Female')])
    bdate = models.DateField()
    myfile = models.CharField(max_length=50)
    address = models.TextField()
    
class Product(models.Model):
    ch=(('Stationary','Stationary'),('Household_supplies','Household_supplies'),('Furnitures','Furnitures'),('Sport-item','Sport-item'),('Electronic-item','Electronic-item'),('Bags_and_Luggage','Bags_and_Luggage'))
    Id = models.AutoField(primary_key =True)
    product_mage = models.ImageField(upload_to='product/',blank=True)
    username  = models.ForeignKey(AuthUser,db_column='username', blank=True, null=True,on_delete=models.CASCADE)
    price = models.IntegerField()
    Productname = models.CharField(max_length=50)
    Description = models.TextField()
    Upload_date = models.DateField()
    status = models.CharField(max_length=15,default="sell")
    catogory = models.CharField(max_length=30,choices=ch,default='Books')
    payment_mode = models.CharField(max_length=20,choices=(('mode1',"Phone-pay"),('mode2','Google-pay'),('mode3','Paytm'),('mode4','Cash')),default='mode4')
    payment_qr = models.ImageField(upload_to='payment_mode/',blank=True,null=True)

    def __str__(self):
        return str(self.Productname)+"->"+str(self.username)

class cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    product_id  = models.ForeignKey(Product, blank=True, null=True,on_delete=models.CASCADE)
    request_id = models.ForeignKey(AuthUser,blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product_id)+","+str(self.cart_id)+","+str(self.request_id)
