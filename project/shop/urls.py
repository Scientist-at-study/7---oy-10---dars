from django.urls import path
from .views import (
    IndexView, ProductDetailView, CommentCreateView,
    CommentUpdateView, CommentDeleteView, ShopView
)

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:product_id>/comment/create/', CommentCreateView.as_view(), name='add_comment'),
    path('comments/<int:comment_id>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('shop/<slug:category_slug>', ShopView.as_view(), name='shop_by_category'),
]
