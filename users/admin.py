from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from movies.forms import MoviesForm

from .forms import UserChangeForm, UserCreationForm
from .models import User

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name", "movies")}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


class MovieChangeList(ChangeList):
    def __init__(self, request, model, list_display,
                 list_display_links, list_filter, date_hierarchy,
                 search_fields, list_select_related, list_per_page,
                 list_max_show_all, list_editable, model_admin):
        super(MovieChangeList, self).__init__(request, model, list_display,
                                              list_display_links, list_filter,
                                              date_hierarchy, search_fields,
                                              list_select_related,
                                              list_per_page, list_max_show_all,
                                              list_editable,
                                              model_admin)

        # these need to be defined here, and not in MovieAdmin
        self.list_display = ['action_checkbox', 'name', 'genre']
        self.list_display_links = ['name']
        self.list_editable = ['genre']

class CompanyAdmin(admin.ModelAdmin):

    def get_changelist(self, request, **kwargs):
        return MovieChangeList

    def get_changelist_form(self, request, **kwargs):
        return MoviesForm
