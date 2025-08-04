# core/views.py
from django.shortcuts import render, get_object_or_404
from .models import City  # Add Supermarket when model is ready
from restaurants.models import Restaurant, MenuItem, MenuItemCategory  # Add Supermarket when model is ready
from supermarkets.models import Supermarket  # Add when model is ready
# from pharmacy.models import Pharmacy  # Assuming Pharmacy model exists

from django.shortcuts import redirect

def homepage(request):
    # query = request.GET.get("city")
    # if query:
    #     return redirect(f'/explore/?city={query.lower()}')

    return render(request, 'core/index.html')

from django.shortcuts import render, get_object_or_404
from .models import City


## ADD MORE CITIES BY ##
# python manage.py shell
# >>> from core.models import City
# >>> City.objects.create(name="Lekki")
# >>> City.objects.create(name="Enugu")

# ###

# def explore(request):
#     query = request.GET.get("city")
#     city = None
#     restaurants = []
#     supermarkets = []

#     if query:
#         try:
#             city = City.objects.get(slug=query.lower())
#             restaurants = Restaurant.objects.filter(city=city)
#             supermarkets = Supermarket.objects.filter(city=city)
#         except City.DoesNotExist:
#             city = None

#     context = {
#         'city': city,
#         'restaurants': restaurants,
#         'supermarkets': supermarkets,
#     }
#     return render(request, 'core/explore.html', context)

def explore(request):
    # city_slug = request.GET.get("city", "").lower()
    # city = get_object_or_404(City, slug=city_slug)

    # restaurants = Restaurant.objects.filter(city=city)
    restaurants = Restaurant.objects.all()  # For now, show all restaurants
    # supermarkets = Supermarket.objects.filter(city=city)
    # pharmacies = Pharmacy.objects.filter(city=city)  # For later
    

    context = {
        # "city": city,
        "restaurants": restaurants,
        # "supermarkets": supermarkets,
    }
    return render(request, "core/explore.html", context)

def all_restaurants(request):
    restaurants = Restaurant.objects.all()
    sponsored_restaurants = restaurants.filter(is_sponsored=True).order_by('-rating')[:5]  # Example logic for sponsored restaurants
    context = {
        'restaurants': restaurants,
        'sponsored_restaurants': sponsored_restaurants,
    }
    return render(request, 'core/all_restaurants.html', context)

def all_supermarkets(request):
    supermarkets = Supermarket.objects.all()
    context = {
        'supermarkets': supermarkets,
    }
    return render(request, 'core/all_supermarkets.html', context)

# def all_pharmacies(request):
#     pharmacies = Pharmacy.objects.all()  # Assuming Pharmacy model exists
#     context = {
#         'pharmacies': pharmacies,
#     }
#     return render(request, 'core/all_pharmacies.html', context)

# core/views.py
from django.http import JsonResponse
from geopy.geocoders import Nominatim
from core.models import City
from django.utils.text import slugify

def get_location_data(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    if not lat or not lon:
        return JsonResponse({"success": False, "message": "Invalid coordinates"})

    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.reverse(f"{lat}, {lon}", language='en')

    if not location:
        return JsonResponse({"success": False, "message": "Location not found"})

    address = location.raw.get("address", {})
    area_name = address.get("city") or address.get("town") or address.get("suburb") or ""

    if not area_name:
        return JsonResponse({"success": False, "message": "Area could not be detected"})

    try:
        city = City.objects.get(slug=slugify(area_name))
        return JsonResponse({"success": True, "city_slug": city.slug})
    except City.DoesNotExist:
        return JsonResponse({"success": False, "message": f"We are not yet in '{area_name.title()}'"})

def restaurant_detail(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug)
    # meals = MenuItem.objects.filter(restaurant=restaurant, available=True)
    # Display all the meals according to the MenuItemCategory using prefetch_related
    # meals = MenuItem.objects.filter(restaurant=restaurant, available=True).prefetch_related('item_category')
    categories = MenuItemCategory.objects.filter(restaurant=restaurant).prefetch_related('menu_items')
    most_popular = MenuItem.objects.filter(restaurant=restaurant, available=True).order_by('-date_posted')[:5]

    context = {
        'restaurant': restaurant,
        'categories': categories,
        'most_popular': most_popular,
    }
    return render(request, 'core/restaurant_detail.html', context)


def general_search(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return render(request, 'core/general_search.html', {'results': []})

    # Search for restaurants
    restaurants = Restaurant.objects.filter(name__icontains=query)

    # Search for supermarkets
    supermarkets = Supermarket.objects.filter(name__icontains=query)
    
    # diaplay recent searches
    recent_searches = request.session.get('recent_searches', [])
    if query not in recent_searches:
        recent_searches.append(query)
        if len(recent_searches) > 5:
            recent_searches.pop(0)

    context = {
        'query': query,
        'restaurants': restaurants,
        'supermarkets': supermarkets,
        'recent_searches': recent_searches,
    }
    return render(request, 'core/general_search.html', context)


# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Cart, CartPack, CartItem
# from django.contrib.contenttypes.models import ContentType
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required

# @login_required
# def view_cart(request):
#     cart, _ = Cart.objects.get_or_create(user=request.user)
#     packs = cart.packs.prefetch_related('items__content_type')
#     return render(request, 'core/cart.html', {'cart': cart, 'packs': packs})

# 

# @login_required
# def add_item_to_pack(request, pack_id):
#     pack = get_object_or_404(CartPack, id=pack_id, cart__user=request.user)

#     # Simulate a product (or adjust if you have real models like Product)
#     product_model = ContentType.objects.get(app_label='shop', model='product')
#     object_id = request.POST.get("object_id")

#     item, created = CartItem.objects.get_or_create(
#         pack=pack,
#         content_type=product_model,
#         object_id=object_id
#     )
#     if not created:
#         item.quantity += 1
#         item.save()

#     return render(request, 'cart/partials/pack_items.html', {'pack': pack})


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Cart, CartPack, CartItem
from restaurants.models import Restaurant, MenuItem
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType

@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    packs = cart.packs.select_related('restaurant').prefetch_related('items__content_type')
    return render(request, 'core/cart.html', {'cart': cart, 'packs': packs})

@login_required
def add_pack(request):
    if request.method == "POST":
        cart = get_object_or_404(Cart, user=request.user)
        pack = CartPack.objects.create(cart=cart, name=request.POST.get("name", "New Pack"))
        return render(request, 'partials/pack.html', {'pack': pack})
    return HttpResponse(status=400)

@login_required
def delete_pack(request, pack_id):
    pack = get_object_or_404(CartPack, id=pack_id, cart__user=request.user)
    pack.delete()
    return HttpResponse(status=204)

@login_required
def add_menu_item_to_cart(request, restaurant_id, item_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_item = get_object_or_404(MenuItem, id=item_id, restaurant=restaurant)

    # Find existing pack for this restaurant
    pack, created = CartPack.objects.get_or_create(
        cart=cart,
        restaurant=restaurant,
        defaults={'name': f"Order from {restaurant.name}"}
    )

    content_type = ContentType.objects.get_for_model(MenuItem)

    item, item_created = CartItem.objects.get_or_create(
        pack=pack,
        content_type=content_type,
        object_id=menu_item.id,
        defaults={'quantity': 1}
    )

    if not item_created:
        item.quantity += 1
        item.save()
        
    messages.success(request, f"{menu_item.name} has been added to your cart.")

    return render(request, 'partials/pack_items.html', {'pack': pack})


@login_required
def add_to_pack(request, pack_id, app_label, model_name, object_id):
    pack = get_object_or_404(CartPack, id=pack_id, cart__user=request.user)
    content_type = ContentType.objects.get(app_label=app_label, model=model_name)
    content_object = content_type.get_object_for_this_type(id=object_id)

    item, created = CartItem.objects.get_or_create(
        pack=pack,
        content_type=content_type,
        object_id=object_id,
        defaults={"quantity": 1},
    )
    if not created:
        item.quantity += 1
        item.save()

    return render(request, "partials/pack_items.html", {"pack": pack})