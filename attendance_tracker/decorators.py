# Documenation sample usage is in 
# https://simpleisbetterthancomplex.com/2015/12/07/working-with-django-view-decorators.html
from django.core.exceptions import PermissionDenied

def user_is_ultimate(function):
    def wrap(request, *args, **kwargs):
        if request.user.license == 'Ultimate':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_professional(function):
    def wrap(request, *args, **kwargs):
        if request.user.license == 'Ultimate' or request.user.license == 'Professional':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_standard(function):
    def wrap(request, *args, **kwargs):
        if request.user.license == 'Ultimate' or request.user.license == 'Professional' or request.user.license == 'Standard':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap