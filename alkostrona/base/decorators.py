from django.shortcuts import redirect, reverse
from django.contrib import messages


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            approved = False
            if request.user.groups.exists():
                for group in request.user.groups.all():
                    if group.name in allowed_roles:
                        approved = True
            if approved:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f'You are not authorised to enter this page.')
                return redirect(reverse('main_menu'))
        return wrapper_func
    return decorator

