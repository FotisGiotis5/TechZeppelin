from django.contrib import admin


from polls import models

admin.site.register(models.Cart)
admin.site.register(models.Payment)
admin.site.register(models.Address)
admin.site.register(models.Product)
admin.site.register(models.Username)
admin.site.register(models.Manufacturer)
admin.site.register(models.Order)
admin.site.register(models.ProductCategory)


