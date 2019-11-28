from django import template
from firstapp.models import Product,AuthUser,cart,User_extends
register = template.Library()

@register.filter(name="modulus")
def xyz(value,arg1):
    return int(value)% int(arg1)

@register.filter(name="cartexistatnce")
def cart_data(value,productid):
    instace = cart.objects.filter(request_id__username=value).filter(product_id=Product.objects.get(Id=productid))
    if len(instace) > 0:
        return 'True'
    else:
        return 'False'

@register.filter(name="getaddress")
def get_address(value):
    instace = User_extends.objects.get(username=value).address
    return str(instace)
