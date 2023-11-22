from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from contents.models import Post

def is_editor(user):
    return user.groups.filter(name="Editors").exists()

editor_required = user_passes_test(is_editor)


def user_is_post_author(function):
    def wrap(request, *args, **kwargs):
        entry = Post.objects.get(pk=kwargs['user_id'])
        if entry.created_by == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap