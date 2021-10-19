from django.urls import path

from .views import IndexView, AboutView, AgentsView, BlogView, BlogDetailsView, ContactView, ProfileView, \
    PropertyView, PropertyComparisonView, PropertyDetailsView, PropertySubmitView, PassengerLoginView, \
    PassengerSignUpView, VerifyEmail, log_out

urlpatterns = [
    path('logout/', log_out, name="logout"),
    path('verify/<uidb64>/<token>/', VerifyEmail.as_view(), name='verify'),
    path('sign-up/', PassengerSignUpView.as_view(), name="sign_up"),
    path('login/', PassengerLoginView.as_view(), name="login"),
    path('property-submit/', PropertySubmitView.as_view(), name="property-submit"),
    path('property-details/', PropertyDetailsView.as_view(), name="property-details"),
    path('property-comparison/', PropertyComparisonView.as_view(), name="property-comparison"),
    path('property/', PropertyView.as_view(), name="property"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('blog-details/', BlogDetailsView.as_view(), name="blog-details"),
    path('blog/', BlogView.as_view(), name="blog"),
    path('agents/', AgentsView.as_view(), name="agents"),
    path('about/', AboutView.as_view(), name="about"),
    path('', IndexView.as_view(), name="index"),
]