from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage, Comment, Additional


admin.site.register(Additional)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_parent_or_image')
    list_display_links = ('name',)
    prepopulated_fields = {"slug": ("name",)}

    def get_parent_or_image(self, obj):
        if obj.parent:
            return f"Subcategory of: {obj.parent.name}"
        elif obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100">')
        return "No Image"

    get_parent_or_image.short_description = "Parent / Image"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment')
    list_display_links = ('comment',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'quantity', 'volume', 'get_images')
    list_display_links = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]

    def get_images(self, product):
        images = product.images.all()
        if not images.exists():
            return "No Image"

        slider_id = f"slider_{product.id}"
        images_html = "".join(
            [f'<img src="{img.image.url}" class="slider-img" style="width:100px; display:none;">' for img in images]
        )

        return mark_safe(f"""
            <div class="slider-container" id="{slider_id}" data-current-index="0">
                <button type="button" onclick="changeSlide('{slider_id}', -1)" class="slider-btn">◀</button>
                <div class="slider">
                    {images_html}
                </div>
                <button type="button" onclick="changeSlide('{slider_id}', 1)" class="slider-btn">▶</button>
            </div>
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    document.querySelectorAll(".slider-container").forEach(slider => {{
                        showSlide(slider.id, 0);
                    }});
                }});

                function showSlide(sliderId, index) {{
                    let sliderContainer = document.getElementById(sliderId);
                    let slides = sliderContainer.querySelectorAll(".slider-img");
                    if (!slides.length) return;

                    index = (index + slides.length) % slides.length;  // 
                    sliderContainer.dataset.currentIndex = index;

                    slides.forEach((img, i) => {{
                        img.style.display = (i === index) ? "block" : "none";
                    }});
                }}

                function changeSlide(sliderId, direction) {{
                    let sliderContainer = document.getElementById(sliderId);
                    let currentIndex = parseInt(sliderContainer.dataset.currentIndex);
                    showSlide(sliderId, currentIndex + direction);
                }}
            </script>
        """)

    get_images.short_description = "Images"