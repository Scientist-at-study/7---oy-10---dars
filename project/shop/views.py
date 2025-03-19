from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Min, Max, Count, Sum, Avg
from .models import Product, Category, Comment, Additional
from .forms import CommentForm


class IndexView(ListView):
    queryset = Product.objects.all()[:8]
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.filter(parent=None)
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    pk_url_kwarg = 'product_id'
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context



class CommentCreateView(CreateView):
    model = Comment
    template_name = 'shop/comment_form.html'
    form_class = CommentForm

    def form_valid(self, form):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        form.instance.product = product
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'product_id': self.kwargs.get('product_id')})


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'shop/comment_form.html'
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'product_id': self.object.product.pk})


class CommentDeleteView(DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'product_id': self.object.product.pk})


class ShopView(ListView):
    model = Product
    template_name = 'shop/shop.html'
    context_object_name = "products"

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        if self.request.method == 'POST':
            range_input = int(self.request.POST.get("rangeInput"))
            additional_pk = self.request.POST.get('Categories-1')
            if category_slug:
                return Product.objects.filter(category__parent__slug=category_slug, price__lte=range_input,
                                              additional__pk=additional_pk)
            return Product.objects.filter(price__lte=range_input, additional__pk=additional_pk)
        else:
            if category_slug:
                products = Product.objects.filter(category__parent__slug=category_slug)
                return products
            return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            subcategories = Category.objects.filter(parent__slug=category_slug)
        else:
            subcategories = Category.objects.exclude(parent=None)
        context['subcategories'] = subcategories
        context['additions'] = Additional.objects.all()

        min_price = self.get_queryset().aggregate(Min('price')).get("price__min")
        max_price = self.get_queryset().aggregate(Max('price')).get("price__max")
        context['min_price'] = min_price
        context['max_price'] = max_price
        return context

    def post(self, request, category_slug=None):
        return self.get(request, category_slug)