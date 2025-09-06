from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBusinessUserOrReadOnly(BasePermission):
    """
    Allows only users with type='business' to perform write operations (POST).
    All users can perform read-only operations (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated and
            getattr(request.user, 'type', None) == 'business'
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Only the creator (owner) of an object is allowed to update or delete it.
    All users can read.
    """

    def has_permission(self, request, view):
        """Allow all users to access the view; object-level check happens separately."""
        return True

    def has_object_permission(self, request, view, obj):
        """Grant read access to all, but restrict write access to the object's owner."""
        if request.method in SAFE_METHODS:
            return True

        return obj.profile.user == request.user


class IsCustomerForPost(BasePermission):
    """
    Authenticated users can read (GET).
    Only users with type='customer' can create (POST).
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return getattr(request.user, 'type', None) == 'customer'


class IsReviewOwnerOrReadOnly(BasePermission):
    """
    Only the user who created the review can update or delete it.
    All users can read reviews.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.reviewer.user == request.user


class IsBusinessForPatchOrAdminForDelete(BasePermission):
    """
    PATCH is only allowed for users with type='business'.
    DELETE is only allowed for staff (admin) users.
    Read-only methods are always allowed (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'PATCH':
            return (
                request.user and 
                request.user.is_authenticated and 
                getattr(request.user, 'type', None) == 'business'
            )

        if request.method == 'DELETE':
            return (
                request.user and 
                request.user.is_authenticated and 
                request.user.is_staff
            )

        return False