from django.contrib.auth.mixins import AccessMixin


class UserTypeMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type == 'User':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)