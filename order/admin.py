from django import forms
from django.contrib import admin

from order.models import Order, OrderItem


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status', 'user')


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class TotalSumFilter(admin.SimpleListFilter):
    title = 'Фильтрация по сумме заказа'
    parameter_name = 'total_sum'

    def lookups(self, request, model_admin):
        return (
            ('0to50000', 'от 0 до 50000'),
            ('50000to100000', 'от 50000 до 100000'),
            ('100000to150000', 'от 100000 до 150000'),
            ('from150000', 'от 150000 и выше')
        )

    def queryset(self, request, queryset):
        if self.value() == '0to50000':
            return queryset.filter(total_sum__lte=50000)
        elif self.value() == '50000to100000':
            return queryset.filter(total_sum__range=[50000, 100000])
        elif self.value() == '100000to150000':
            return queryset.filter(total_sum__range=[100000, 150000])
        elif self.value() == 'from150000':
            return queryset.filter(total_sum__gte=150000)
        else:
            return queryset


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemsInline
    ]
    exclude = ('products', )
    form = OrderAdminForm
    readonly_fields = ['user', 'total_sum', 'created_at']
    list_display = ['id', 'status', 'total_sum', 'created_at']
    list_filter = ['status', TotalSumFilter]
    search_fields = ['products__title']
    list_display_links = ['id', 'status']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        total = 0
        for inline_form in formset:
            if inline_form.cleaned_data:
                price = inline_form.cleaned_data['product'].price
                quantity = inline_form.cleaned_data['quantity']
                total += price * quantity
        form.instance.total_sum = total
        form.instance.save()
        formset.save()



#TODO: исправить сохранение total_sum


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
