import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib import messages
from .models import Alcohol, Profile, Like, Review
from .forms import ProfileUpdateForm, UserRegistrationForm, PasswordResetForm, ForgotPasswordForm, SetPasswordForm,\
    UserLoginForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.decorators import method_decorator
from .tokens import account_activation_token
from .decorators import allowed_users
from django.db.models.query_utils import Q


def custom_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('main_menu'))
    else:
        if request.method == "POST":
            form = UserLoginForm(request=request, data=request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password"],
                )
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Welcome back to Sommelier, <b>{user.profile.nickname}</b>!")
                    return redirect(reverse('main_menu'))

            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = UserLoginForm()

        return render(
            request=request,
            template_name="base/login.html",
            context={"form": form}
        )


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordResetForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed. You have been automatically logged in.")
            login(request, user)
            return redirect('main_menu')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    form = PasswordResetForm(user)
    return render(request, 'base/password_reset.html', {'form': form})


def forgot_password(request):
    if request.user.is_authenticated:
        return redirect(reverse('main_menu'))
    else:
        if request.method == 'POST':
            form = ForgotPasswordForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                lost_user = get_user_model().objects.filter(Q(email=email)).first()
                if lost_user:
                    subject = "Reset your password"
                    message = render_to_string("base/reset_mail_template.html", {
                        'user': lost_user,
                        'domain': get_current_site(request).domain,
                        'uid': urlsafe_base64_encode(force_bytes(lost_user.pk)),
                        'token': account_activation_token.make_token(lost_user),
                        "protocol": 'https' if request.is_secure() else 'http'
                    })
                    email = EmailMessage(subject, message, to=[lost_user.email])
                    if email.send():
                        messages.success(request, f'Dear {lost_user.profile.nickname}, we sent the instructions for setting \
                        your password anew on the email you provided. Please check your mailbox.')
                    else:
                        messages.error(request, "There was a problem sending reset password email.")

                return redirect(reverse('main_menu'))
        form = ForgotPasswordForm()
        return render(
            request=request,
            template_name="base/forgot_password.html",
            context={"form": form}
        )


def forgotPasswordConfirm(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may now log in using your new password.")
                return redirect('main_menu')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'base/password_reset.html', {'form': form})
    else:
        messages.error(request, "The reset link has expired.")

    messages.error(request, 'Something went wrong, you got redirected back to home page.')
    return redirect("main_menu")


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been verified. You have been logged in automatically.")
        login(request, user)
    else:
        messages.error(request, "Activation link was invalid!")

    return redirect(reverse('main_menu'))


def activateEmail(request, user, to_email):
    mail_subject = "Sommelier account activation"
    message = render_to_string("base/email_body.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Welcome, <b>{user.profile.nickname}</b>. please go to your email <b>{to_email}</b> to confirm \
            your email address. This will complete your registration and allow you to log in.')
    else:
        messages.error(request,
                       f'The was a problem sending an email to {to_email}, make sure the credentials put by you were correct.')


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('main_menu'))

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            Profile.objects.create(
                user=user,
                nickname=form['nickname'].value(),
            )
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect(reverse('main_menu'))
        else:
            for error in list(form.errors.values()):
                print(request, error)
    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name='base/register.html',
        context={'form': form}
    )


class MainMenu(ListView):
    model = Alcohol
    context_object_name = 'alcohols'
    template_name = 'base/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alcohol_types'] = Alcohol.ALCOHOL_TYPES
        return context


class AlcoholDetail(DetailView):
    model = Alcohol
    context_object_name = 'alcohol'
    template_name = 'base/alcohol.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(alcohol=self.object)
        # context['photo'] = Review.objects.filter(alcohol=self.object).user.profile.profile_picture.url
        reviewers = [x.user.username for x in Review.objects.filter(alcohol=self.object)]
        ratings = [x.rate for x in Review.objects.filter(alcohol=self.object)]
        dictionary = dict(zip(reviewers, ratings))
        print(dictionary)
        context['user_ratings'] = json.dumps(dictionary)
        print(json.dumps(dictionary))
        reviews = Review.objects.filter(alcohol=self.object)
        # prices_json = json.dumps(reviews, cls=DjangoJSONEncoder)
        # context['prices_json'] = prices_json
        return context


@login_required
def like_alcohol(request):
    alcohol_id = None
    if request.method == 'POST':
        alcohol_id = request.POST.get('alcohol_id')
        alcohol_obj = Alcohol.objects.get(id=alcohol_id)

        if request.user in alcohol_obj.likes.all():
            alcohol_obj.likes.remove(request.user)
        else:
            alcohol_obj.likes.add(request.user)

        like, created = Like.objects.get_or_create(user=request.user, alcohol_id=alcohol_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Dislike'
            else:
                like.value = 'Like'
        like.save()
    return redirect(reverse('alco_det', args=[alcohol_id]))


@login_required
def review_alcohol(request, pk):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            pl = data.get('payload')
            if len(pl['opinion']) > 3000:
                return JsonResponse({'status': 'The opinion is too long.'}, status=400)
            if pl['rate'] < 1 or pl['rate'] > 5:
                return JsonResponse({'status': 'Please try again.'}, status=400)

            alcohol_id = pk
            user = request.user
            alcohol_obj = Alcohol.objects.get(id=alcohol_id)
            if user in alcohol_obj.reviews.all():
                review_obj = Review.objects.get(user=user, alcohol_id=alcohol_id)
                review_obj.rate = pl['rate']
                review_obj.comment = pl['opinion']
                review_obj.save()
            else:
                alcohol_obj.reviews.add(user)
                review = Review.objects.create(user=user, alcohol_id=alcohol_id, comment=pl['opinion'], rate=pl['rate'])
                review.save()

            return JsonResponse({'status': 'alcohol reviewed', 'user': user.username}, status=200)
    else:
        return HttpResponseBadRequest('invalid request')


class AlcoholAdd(LoginRequiredMixin, CreateView):
    model = Alcohol
    fields = ['name', 'alcohol_picture', 'type', 'volume_l', 'percentage', 'description']
    success_url = reverse_lazy('main_menu')
    template_name = 'base/alcohol_add_modify.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

        mod = False
        for group in self.request.user.groups.all():
            if group.name == 'moderator':
                mod = True
                break
        form.instance.verified = mod

        return super(AlcoholAdd, self).form_valid(form)


class LikedAlcohols(LoginRequiredMixin, ListView):
    model = Alcohol
    context_object_name = 'alcohols'
    template_name = 'base/alcohol_liked.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_key = self.request.GET.get('search-key') or ''
        if search_key:
            context['alcohols'] = context['alcohols'].filter(name__icontains=search_key)
        context['search_key'] = search_key
        return context


class AlcoholChange(LoginRequiredMixin, UpdateView):
    model = Alcohol
    fields = ['name', 'type', 'volume_l', 'percentage', 'description']
    success_url = reverse_lazy('main_menu')
    template_name = 'base/alcohol_add_modify.html'

    @method_decorator(allowed_users(allowed_roles=['moderator']))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'base/edit_profile.html'
    form_class = ProfileUpdateForm

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'pk': self.object.id})


class AlcoholRemove(LoginRequiredMixin, DeleteView):
    model = Alcohol
    context_object_name = 'alcohol'
    success_url = reverse_lazy('main_menu')
    template_name = 'base/alcohol_remove.html'

    @method_decorator(allowed_users(allowed_roles=['moderator']))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'base/profile.html'


class AlcoholTypeChosen(ListView):
    model = Alcohol
    context_object_name = 'alcohol'
    template_name = 'base/alcohol_type.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_key = self.request.GET.get('search-key') or ''
        if search_key:
            context['alcohol'] = context['alcohol'].filter(name__icontains=search_key)
        context['search_key'] = search_key
        return context


class UnverifiedAlcohols(LoginRequiredMixin, ListView):
    model = Alcohol
    context_object_name = 'alcohol'
    template_name = 'base/alcohol_unverified.html'

    @method_decorator(allowed_users(allowed_roles=['moderator']))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def verify_alcohol(request):
    if request.method == 'POST':
        alcohol_id = request.POST.get('alcohol_id')
        alcohol_obj = Alcohol.objects.get(id=alcohol_id)
        alcohol_obj.verified = True
        alcohol_obj.save()
        messages.success(request, f'The alcohol <b>"{alcohol_obj.name}"</b> was successfully verified.')

    return redirect(reverse('unverified'))


def delete_review(request):
    alcohol_id = None
    if request.method == 'POST':
        alcohol_id = request.POST.get('alcohol_id')
        alcohol_obj = Alcohol.objects.get(id=alcohol_id)
        review_id = request.POST.get('review_id')

        alcohol_obj.reviews.remove(request.user)
        Review.objects.filter(id=review_id).delete()

    return redirect(reverse('alco_det', args=[alcohol_id]))

