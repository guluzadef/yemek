from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.sites import requests
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from default.helper_task import user_location, meal_location
from default.mixins import UserTypeMixin
from .models import *
from .forms import AddFood, OrderingForm, CommentForm, ProfilePhotouser, SocialUser, ChangePassword
from django.views import generic
from django.contrib.auth import login, authenticate
from default.models import TokenModel, CommentPost
from base_user.forms import MyUserChangeForm
import json
from django.http import JsonResponse, request
from default.forms import UserRegisterForm, CookerRegisterForm, LoginForm, Ordering


def user_login(request):
    context = {}
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/')
    context['form'] = LoginForm()
    return render(request, 'login.html', context)


def user_register(request):
    context = {}
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = form.save(commit=False)
            user.user_type = 'User'
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'{username} Zehmet olmasa emailinizi yoxlayin')
            return redirect('index')
        else:
            print(form.errors.as_data())
            messages.warning(request, form.errors)
            return redirect('index')
    context['form'] = form
    return render(request, 'user-register.html', context)


def cooker_register(request):
    context = {}
    form = CookerRegisterForm()
    if request.method == 'POST':
        form = CookerRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # phone = form.cleaned_data['phone']
            user = form.save(commit=False)
            user.user_type = 'Cooker'
            # user.phone = phone
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'{username} Zehmet olmasa emailinizi yoxlayin')
            return redirect('index')
        else:
            messages.warning(request, form.errors)
            return redirect('index')
    context['form'] = form
    return render(request, 'cooker-register.html', context)


def verify_view(request, token, id):
    verify = TokenModel.objects.filter(
        token=token,
        expired=False,
        user_id=id
    ).last()
    if verify:
        verify.user.is_active = True
        verify.user.save()
        verify.expired = True
        verify.save()
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        return redirect('index')
    else:
        print('---------------------------------------------')
        return redirect('index')


def common():
    context = {}
    context["sitename"] = Site_name.objects.all()
    context['menu'] = Menu.objects.all()
    context['main'] = Main.objects.all()
    context['footer'] = Footer.objects.all()
    context['photos'] = Photos_Pages.objects.last()
    context['text'] = Texts_Pages.objects.last()
    context['instagram'] = Instagramfield.objects.all()

    return context


def Home(request):
    context = common()
    context['first'] = First.objects.last()
    context['second'] = Second.objects.last()
    context['meals'] = Meals.objects.all()
    if request.user.is_authenticated:
        context['notify_check'] = True if Notifications.objects.filter(to_user=request.user, read=False) else False
    # context['meals'] = Meals.objects.all()
    if 'q' in request.GET:
        query = request.GET.get('q')
        return redirect('search', str=query)
        # return redirect_params('search_view', your_params)

    pagination = Paginator(Meals.objects.all(), 6)
    context["meals"] = pagination.get_page(request.GET.get('page', 1))
    context['like_meal'] = Meals.objects.all().annotate(num_posts=Count('like')).order_by('-num_posts')

    context["page_range"] = pagination.page_range
    return render(request, "index.html", context)


def detail(request, id):
    context = common()
    current_post = Meals.objects.filter(id=id).last()
    context['object'] = current_post
    # me = Meals.objects.all().filter(user=current_post.user).count()
    current_post_comment = current_post.commentpost_set.all()
    pagination = Paginator(current_post_comment, 4)
    context["current_post_comment"] = pagination.get_page(request.GET.get('page'))
    context["page_range"] = pagination.page_range
    if request.user.is_authenticated:
        context['check_like'] = Like.objects.filter(post_id=id, user=request.user)
    # context["current_post_comment"] = current_post_comment
    context["form"] = CommentForm()
    if request.method == "POST" and request.is_ajax():
        post_id_cm = request.POST.get("post_id_cm")
        print(post_id_cm)
        if post_id_cm:
            text_coment = request.POST.get('text_comment')
            CommentPost.objects.create(
                user=request.user,
                comment=text_coment,
                post=Meals.objects.filter(id=post_id_cm).last(),
            )
            return JsonResponse({
                'append': True,
                'image': request.user.profile_photo.url,
                'user': request.user.username,
                'text_comment': text_coment,
                'comment_count': current_post_comment.count()
            })
    return render(request, 'DetailFood.html', context)


def like_view(request):
    if request.method == "POST" and request.is_ajax():
        post_id = request.POST.get("post_id")
        post = Meals.objects.filter(id=post_id).last()
        if post:
            like = Like.objects.filter(post=post, user=request.user).last()
            if like:
                like.delete()
                return JsonResponse({
                    "like_count": post.like_set.all().count(),
                    "status": False
                })
            else:
                Like.objects.create(
                    user=request.user,
                    post=post
                )
                return JsonResponse({
                    "like_count": post.like_set.all().count(),
                    "status": True
                })
        else:
            return redirect("/")
    else:
        return redirect("/")


class add_food(UserTypeMixin, generic.CreateView):
    form_class = AddFood
    template_name = 'yemek.html'
    success_url = "/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.cord_lng = self.request.POST.get('lng')
        form.instance.cord_lat = self.request.POST.get('lat')
        form.instance.location = self.request.POST.get('location_cooker')
        if self.request.POST.get('delivery_price'):
            form.instance.delivery_price = self.request.POST.get('delivery_price')
        post = form.save()
        image_data = self.request.POST.get('image_data')
        image_list = MealsImages.objects.filter(image_token=image_data).all()
        if image_data:
            for image in image_list:
                image.post = post
                image.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(add_food, self).get_context_data(**kwargs)
        context['image_data'] = str(uuid.uuid4())
        context['menu'] = Menu.objects.all()
        context["sitename"] = Site_name.objects.all()
        context['photos'] = Photos_Pages.objects.last()
        return context


def picture_add(request):
    print(request.FILES)
    if request.method == "POST":
        img = MealsImages.objects.create(
            image=request.FILES.get('file'),
            image_token=request.POST.get('image_data')
        )
        return JsonResponse({
            'uploaded': True,
            'pk': img.id,
        })
    else:
        return JsonResponse({
            'uploaded': False,
        })


def picture_delete(request):
    if request.method == 'POST':
        pk = request.POST.get('remove_object')
        img = MealsImages.objects.filter(id=pk)
        if img:
            img.delete()
            return JsonResponse({
                'deleted': True
            })
        else:
            return JsonResponse({
                'deleted': False
            })


def ProfileUser(request, id):
    context = common()
    context['user'] = User.objects.filter(id=id).last()
    meal = Meals.objects.filter(author_id=id).all()
    pagination = Paginator(meal, 8)
    context["meals"] = pagination.get_page(request.GET.get('page', 1))
    context["page_range"] = pagination.page_range
    context['profilephoto'] = ProfilePhotouser()
    context["count"] = Meals.objects.filter(author_id=id).all().count()

    if request.method == "POST":
        form = ProfilePhotouser(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"{id}")
        else:
            return redirect('/')
    return render(request, 'userprofile.html', context)


def SettingUser(request):
    context = common()
    context['profilephoto'] = ProfilePhotouser()
    context['form'] = MyUserChangeForm(instance=request.user, initial={
        "fullname": request.user.get_full_name(),
        "username": request.user.get_username(),
        "email": request.user.email
    })
    if request.method == "POST":
        profile = request.POST.get('profile_settings')
        settings = request.POST.get('settings')
        if profile is not None:
            form1 = ProfilePhotouser(request.POST, request.FILES, instance=request.user)
            if form1.is_valid():
                form1.save()
                return redirect('/')
        elif settings is not None:
            form = MyUserChangeForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('/')
    return render(request, "settings_user.html", context)


def setting_social(request):
    context = common()
    context['form'] = SocialUser(instance=request.user, initial={
        'facebook': request.user.facebook,
        'instagram': request.user.instagram
    })
    if request.method == "POST":
        form = SocialUser(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            context['form'] = SocialUser()
    return render(request, 'setting-socials.html', context)


# @login_required
def order(request, id):
    object = Meals.objects.filter(id=id).last()
    delivery_price = object.delivery_price if object.delivery_price is not None else 0
    print(delivery_price)
    if request.user != object.author and request.user.is_authenticated:
        context = common()
        form = OrderingForm()
        if request.method == 'POST':
            form = OrderingForm(request.POST)
            quantity = request.POST.get('quantity')
            if form.is_valid():
                form.instance.total_price = int(quantity) * object.price + delivery_price
                form.instance.customer = request.user
                form.instance.meal = object
                form.instance.author_of_meal = object.author
                form.save()
                messages.success(request, 'Sifarisiniz ugurla aspaza gonderildi')
                return redirect('index')
            else:
                print('+++++++++++++++++++', form.errors)
                messages.error(request, 'Melumat Sehfdir')
        context['order_form'] = form
        context['object'] = Meals.objects.filter(id=id).last()
        return render(request, 'order.html', context)
    else:
        messages.error(request, 'Sifaris etmek ucun qeydiyatdan kecin')
        return redirect('index')


def AllFood(request):
    context = common()
    pagination = Paginator(Meals.objects.all(), 8)
    context["meals"] = pagination.get_page(request.GET.get('page', 1))
    context["page_range"] = pagination.page_range
    return render(request, 'allfood.html', context)


def search(request, str):
    context = common()
    explore = Meals.objects.filter(
        Q(author__username__icontains=str)
    )
    pagination = Paginator(explore, 8)
    context['meals'] = pagination.get_page(request.GET.get('page', 1))
    return render(request, 'search.html', context)


class Delete(generic.DeleteView):
    model = Meals
    template_name = "delete.html"
    success_url = "/"
    messages = '%(<a href=''>hyperlink</a>)'

    # messages= (request,'<a href='/delete'>hyperlink</a>')
    def get_queryset(self):
        qs = super(Delete, self).get_queryset()
        return qs.filter(author=self.request.user)


def close_foods(request):
    context = common()
    return render(request, 'close_foods.html', context)


def close_foods_helper(request):
    context = {}
    if request.method == 'POST' and request.is_ajax():
        user_lng = request.POST.get('lng')
        user_lat = request.POST.get('lat')
        print(user_lng, user_lat)
        # data=serializers.serialize('json', list(filter(lambda x: user_location(float(user_lat),float(user_lng))-meal_location(x.cord_lat,x.cord_lng)<1000, Meals.objects.all())))
        # return JsonResponse({
        #     'data':data
        # })
        data = list(filter(
            lambda x: user_location(float(user_lat), float(user_lng)) - meal_location(x.cord_lat, x.cord_lng) < 1000,
            Meals.objects.all()))

        paginator = Paginator(data, 5)  # Show 5 per page
        page = request.GET.get('page')
        check = paginator.get_page(page)
        context['objects'] = check
    return render(request, 'close_foods_helper.html', context)


@login_required
def orders(request, id):
    context = common()
    user = MyUser.objects.filter(id=id).last()
    if user.user_type == 'User':
        read = Notifications.objects.filter(to_user=user, read=False)
        read.update(read=True)
        context['orders_user'] = user.customer.all()
        return render(request, 'orders_user.html', context)
    else:
        read = Notifications.objects.filter(to_user=user, read=False)
        read.update(read=True)
        context['orders_cooker'] = user.meals_set.all()
        context['orders_checker'] = True if Ordering.objects.filter(
            author_of_meal=request.user).last() is not None else False

        return render(request, 'orders_cooker.html', context)


@login_required
def changepassword(request):
    context = common()
    context['form'] = ChangePassword()
    if request.method == "POST":
        form = ChangePassword(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            request.user.set_password(password)
            request.user.save()
            return redirect('/')

    return render(request, 'user-forget-pass.html', context)


def time_day(request):
    context = {}
    if request.method == "POST" and request.is_ajax():

        category = request.POST.get('category')
        if category != 'All':
            pagination = Paginator(Meals.objects.filter(category=category).all(),6)
            context["meals"] = pagination.get_page(request.GET.get('page'))
            context['category']=category
        else:
            pagination = Paginator(Meals.objects.all(), 6)
            context["meals"] = pagination.get_page(request.GET.get('page'))
            context['category']=category

    return render(request, 'pagination_foods.html', context)


def morningfood(request):
    context=common()
    pagination = Paginator(Meals.objects.filter(category='Morning'), 6)
    context["meals"] = pagination.get_page(request.GET.get('page'))
    # context['meals']=Meals.objects.filter(category='Morning')
    return  render(request,'morning.html',context)


def lunchfood(request):
    context=common()
    pagination = Paginator(Meals.objects.filter(category='Lunch'), 6)
    context["meals"] = pagination.get_page(request.GET.get('page'))
    # context['meals']=Meals.objects.filter(category='Morning')
    return  render(request,'lunch.html',context)


def supperfood(request):
    context=common()
    pagination = Paginator(Meals.objects.filter(category='Supper'), 6)
    context["meals"] = pagination.get_page(request.GET.get('page'))
    # context['meals']=Meals.objects.filter(category='Morning')
    return  render(request,'supper.html',context)

def bestlikes(request):
    context = common()
    pagination = Paginator(Meals.objects.all().annotate(num_posts=Count('like')).order_by('-num_posts'), 6)
    context["meals"] = pagination.get_page(request.GET.get('page', 1))
    context["page_range"] = pagination.page_range
    return render(request, 'bestlike.html', context)
