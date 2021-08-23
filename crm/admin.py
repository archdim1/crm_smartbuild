from django.contrib import admin


from .models import Company, Phone, Email, Manager, User, Project, Interaction, Customer, ManagerCRM
from django.contrib.auth.admin import UserAdmin


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0


class EmailInline(admin.TabularInline):
    model = Email
    extra = 0


class ManagerInline(admin.TabularInline):
    model = Manager
    extra = 0


class InteractionInline(admin.TabularInline):
    model = Interaction
    extra = 0


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0


class CustomerInLine(admin.TabularInline):
    model = Customer
    extra = 0


class ManagerCRMInLine(admin.TabularInline):
    model = ManagerCRM
    extra = 0


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_admin', 'is_manager', 'is_customer',)
    inlines = [ManagerCRMInLine, CustomerInLine]

    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Дополнительная информация',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'phone_number', 'photo', 'is_manager', 'is_customer', 'is_admin',
                ),
            },
        ),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'leader_name', 'created_date', 'updated_date')
    inlines = [PhoneInline, EmailInline, ManagerInline, ProjectInline]


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'company',)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'company',)


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('manager_name', 'company',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'status_pro', 'price')
    inlines = [InteractionInline,]


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('channel_of_reference', 'reference_obj', 'project', 'user', 'rating', 'created_date')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')


@admin.register(ManagerCRM)
class ManagerCRMAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')


