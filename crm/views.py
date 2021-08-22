from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from crm.forms import PhoneFormSet, EmailFormSet, ManagerFormSet, CompanyModelForm, InteractionModelForm, \
    ManagerCRMFormSet, CustomerFormSet
from crm.models import Company, User, Project, Interaction, ManagerCRM, Customer


class CompanyListView(ListView):
    """
    Класс отображения списка компаний на сайте.
    """
    model = Company
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        context = super(CompanyListView, self).get_context_data(**kwargs)
        context['current_order'] = self.get_ordering()
        return context

    def get_ordering(self):
        """
        Определяет по каким полям можно делать сортировку на странице.
        """
        ordering = self.request.GET.get('sort', 'title')
        return ordering if ordering in ('-title', 'created_date', '-created_date', 'title') else 'title'

    def get_queryset(self):
        """
        Определяет список объектов модели Company, которые мы хотим отобразить.
        """
        qs = Company.objects.order_by(self.get_ordering())
        return qs


class CompanyDetailView(DetailView):
    """
    Класс отображения информации о конкретной компании по pk.
    """
    model = Company
    query_pk_and_slug = True


class CompanyCreateView(CreateView):
    """
    Класс создания записи о новой компании.
    """
    model = Company
    fields = ['title', 'leader_name', 'description', 'address']

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        context = super(CompanyCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['phone_formset'] = PhoneFormSet(self.request.POST)
            context['email_formset'] = EmailFormSet(self.request.POST)
            context['manager_formset'] = ManagerFormSet(self.request.POST)
        else:
            context['phone_formset'] = PhoneFormSet()
            context['email_formset'] = EmailFormSet()
            context['manager_formset'] = ManagerFormSet()
        return context

    def form_valid(self, form):
        """
        Проверяет валидность заполненной информации в форме.
        """
        context = self.get_context_data(form=form)
        self.author = self.request.user
        formsets = [context['phone_formset'], context['email_formset'], context['manager_formset']]
        count = 0
        for formset in formsets:
            if formset.is_valid():
                response = super().form_valid(form)
                # formset.instance = self.object
                # formset.save()
                contacts = formset.save(commit=False)
                for contact in contacts:
                    contact.user = self.request.user
                    contact.company = self.object
                    contact.save()
                count += 1
                if count == len(formsets):
                    return response
            else:
                return super().form_invalid(form)


class CompanyUpdateView(UpdateView):
    """
    Класс редаактированния записи о компании на странице.
    """
    model = Company
    query_pk_and_slug = True
    template_name_suffix = '_update'
    fields = ['title', 'leader_name', 'description', 'address']

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['phone_formset'] = PhoneFormSet(self.request.POST, instance=self.object)
            context['phone_formset'].full_clean()
            context['email_formset'] = EmailFormSet(self.request.POST, instance=self.object)
            context['email_formset'].full_clean()
            context['manager_formset'] = ManagerFormSet(self.request.POST, instance=self.object)
            context['manager_formset'].full_clean()
        else:
            context['phone_formset'] = PhoneFormSet(instance=self.object)
            context['email_formset'] = EmailFormSet(instance=self.object)
            context['manager_formset'] = ManagerFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        """
        Проверяет валидность заполненной информации в форме.
        """
        context = self.get_context_data(form=form)
        formsets = [context['phone_formset'], context['email_formset'], context['manager_formset']]
        count = 0
        for formset in formsets:
            if formset.is_valid():
                response = super().form_valid(form)
                # formset.instance = self.object
                # formset.save()
                contacts = formset.save(commit=False)
                for contact in contacts:
                    contact.user = self.request.user
                    contact.company = self.object
                    contact.save()
                count += 1
                if count == len(formsets):
                    return response
            else:
                return super().form_invalid(form)


class CompanyDeleteView(DeleteView):
    """
    Класс для удаления записи о компании из сайта.
    """
    model = Company
    success_url = reverse_lazy('companies')


class UserDetailView(DetailView):
    """
    Класс отображения информации о текущем пользователе.
    """
    model = User

    def get_object(self):
        """
        Берет информацю только о текущем пользователе.
        """
        return self.request.user


class UpdatePassword(PasswordChangeView):
    """
    Класс по редактированию(изменению) пароля учетной записи текущего пользователя.
    """
    form_class = PasswordChangeForm
    success_url = '/user/profile/'
    template_name = 'crm/change-password.html'


class UserUpdateView(UpdateView):
    """
    Класс по редактированию(изменению) личной информации текущего пользователя,
    если пользователь не имеет статус - менеджер-CRM, или статус - заказчик.
    """
    model = User
    fields = ['photo', 'username', 'first_name', 'last_name', 'email', 'phone_number']
    template_name_suffix = '_update'
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        """
        Берет информацю только о текущем пользователе.
        """
        return self.request.user


class UserManagerCRMUpdateView(UpdateView):
    """
    Класс по редактированию(изменению) личной информации текущего пользователя со статусом - менеджер-CRM.
    """
    model = User
    fields = ['photo', 'username', 'first_name', 'last_name', 'email', 'phone_number']
    template_name = 'crm/user_managercrm_update.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        """
        Берет информацю только о текущем пользователе.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        context = super(UserManagerCRMUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['managercrm_formset'] = ManagerCRMFormSet(self.request.POST, instance=self.object)
            context['managercrm_formset'].full_clean()
        else:
            context['managercrm_formset'] = ManagerCRMFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        """
        Проверяет валидность заполненной информации в форме.
        """
        context = self.get_context_data(form=form)
        if context['managercrm_formset']:
            formset = context['managercrm_formset']
            if formset.is_valid():
                response = super().form_valid(form)
                formset.instance = self.object
                formset.save()
                return response
            else:
                return super().form_invalid(form)


class UserCustomerUpdateView(UpdateView):
    """
    Класс по редактированию(изменению) личной информации текущего пользователя со статусом - заказчик.
    """
    model = User
    fields = ['photo', 'username', 'first_name', 'last_name', 'email', 'phone_number']
    template_name = 'crm/user_customer_update.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        """
        Берет информацю только о текущем пользователе.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        context = super(UserCustomerUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['customer_formset'] = CustomerFormSet(self.request.POST, instance=self.object)
            context['customer_formset'].full_clean()
        else:
            context['customer_formset'] = CustomerFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        """
        Проверяет валидность заполненной информации в форме.
        """
        context = self.get_context_data(form=form)
        if context['customer_formset']:
            formset = context['customer_formset']
            if formset.is_valid():
                response = super().form_valid(form)
                formset.instance = self.object
                formset.save()
                return response
            else:
                return super().form_invalid(form)


class ManagerCRMListView(ListView):
    """
    Класс по отображению списка пользователей со статусом - менеджер-CRM.
    """
    model = ManagerCRM
    paginate_by = 3
    template_name = 'crm/manager_crm_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        context = super(ManagerCRMListView, self).get_context_data(**kwargs)
        context['current_order'] = self.get_ordering()
        return context

    def get_ordering(self):
        """
        Определяет по каким полям можно делать сортировку на странице.
        """
        ordering = self.request.GET.get('sort', 'user')
        return ordering if ordering in ('name', '-name',) else 'user'

    def get_queryset(self):
        """
        Определяет список объектов модели ManagerCRM, которые мы хотим отобразить.
        """
        qs = ManagerCRM.objects.order_by(self.get_ordering())
        return qs


class ManagerCRMDetailView(DetailView):
    """
    Класс отображает информацию о конкретном пользователе со статусом - менеджер-CRM по pk.
    """
    model = ManagerCRM
    query_pk_and_slug = True
    template_name = 'crm/manager_crm_detail.html'


class CustomerListView(ListView):
    """
    Класс по отображению списка пользователей со статусом - заказчик.
    """
    model = Customer
    paginate_by = 3
    template_name = 'crm/customer_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        context = super(CustomerListView, self).get_context_data(**kwargs)
        context['current_order'] = self.get_ordering()
        return context

    def get_ordering(self):
        """
        Определяет по каким полям можно делать сортировку на странице.
        """
        ordering = self.request.GET.get('sort', 'user')
        return ordering if ordering in ('-name', 'name') else 'user'

    def get_queryset(self):
        """
        Определяет список объектов модели Customer, которые мы хотим отобразить.
        """
        qs = Customer.objects.order_by(self.get_ordering())
        return qs


class CustomerDetailView(DetailView):
    """
    Класс отображает информацию о конкретном пользователе со статусом - заказчик по pk.
    """
    model = Customer
    query_pk_and_slug = True
    template_name = 'crm/customer_detail.html'


class CompanyProjectsDetailView(DetailView, MultipleObjectMixin):
    """
    Класс отображает список всех проектов конкретной компании по ее pk.
    """
    model = Company
    paginate_by = 3
    query_pk_and_slug = True
    template_name = 'crm/companyproject_detail.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        object_list = Project.objects.filter(company=self.object)
        context = super(CompanyProjectsDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['current_order'] = self.get_ordering()
        context['form'] = CompanyModelForm()
        return context


class CompanyProjectsNotStartedDetailView(DetailView, MultipleObjectMixin):
    """
    Класс отображает список проектов со статусом - Еще не начат, конкретной компании по ее pk.
    """
    model = Company
    paginate_by = 3
    query_pk_and_slug = True
    template_name = 'crm/companyproject_detail_not_started.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        object_list = Project.objects.filter(company=self.object)
        context = super(CompanyProjectsNotStartedDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['current_order'] = self.get_ordering()
        context['form'] = CompanyModelForm()
        return context


class CompanyProjectsInProcessDetailView(DetailView, MultipleObjectMixin):
    """
    Класс отображает список проектов со статусом - В процессе разработки, конкретной компании по ее pk.
    """
    model = Company
    paginate_by = 3
    query_pk_and_slug = True
    template_name = 'crm/companyproject_detail_in_process.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        object_list = Project.objects.filter(company=self.object)
        context = super(CompanyProjectsInProcessDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['current_order'] = self.get_ordering()
        context['form'] = CompanyModelForm()
        return context


class CompanyProjectsCompletedDetailView(DetailView, MultipleObjectMixin):
    """
    Класс отображает список проектов со статусом - Выполнен, конкретной компании по ее pk.
    """
    model = Company
    paginate_by = 3
    query_pk_and_slug = True
    template_name = 'crm/companyproject_detail_completed.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        object_list = Project.objects.filter(company=self.object)
        context = super(CompanyProjectsCompletedDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['current_order'] = self.get_ordering()
        context['form'] = CompanyModelForm()
        return context


class ProjectListView(ListView):
    """
    Класс отображает список всех проектов на сайте.
    """
    model = Project
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['current_order'] = self.get_ordering()
        return context

    def get_ordering(self):
        """
        Определяет по каким полям можно делать сортировку на странице.
        """
        ordering = self.request.GET.get('sort', 'start_date')
        return ordering if ordering in ('-start_date', 'name', '-name',
                                        'company', '-company', 'start_date',
                                        'price', '-price', 'status_pro') else 'start_date'

    def get_queryset(self):
        """
        Определяет список объектов модели Project, которые мы хотим отобразить.
        """
        qs = Project.objects.order_by(self.get_ordering())
        return qs


class ProjectDetailView(DetailView):
    """
    Класс отображает информацию по конкретному проекту по pk.
    """
    model = Project
    query_pk_and_slug = True


class ProjectCustomerListView(ListView):
    """
    Класс отображает список всех проектов,
    заказчиком которых является текущий пользователь со статусом - заказчик.
    """
    model = Project
    paginate_by = 5
    template_name = 'crm/customer_project_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        if self.request.user.is_authenticated:
            context = super(ProjectCustomerListView, self).get_context_data(**kwargs)
            context['current_order'] = self.get_ordering()
            return context

    def get_ordering(self):
        """
        Определяет по каким полям можно делать сортировку на странице.
        """
        ordering = self.request.GET.get('sort', 'start_date')
        return ordering if ordering in ('-start_date', 'name', '-name',
                                        'company', '-company', 'start_date',
                                        'price', '-price', 'status_pro') else 'start_date'

    def get_queryset(self):
        """
        Определяет список объектов модели Project, которые мы хотим отобразить.
        """
        if self.request.user.is_authenticated:
            qs = Project.objects.order_by(self.get_ordering())
            return qs


class ProjectInteractionsDetailView(DetailView, MultipleObjectMixin):
    """
    Класс отображает список всех взаимодействий по конкретному проекту по pk.
    """
    model = Project
    paginate_by = 3
    query_pk_and_slug = True
    template_name = 'crm/project_interactions.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        object_list = Interaction.objects.filter(project=self.object)
        context = super(ProjectInteractionsDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['current_order'] = self.get_ordering()
        return context


class CompanyProjectInteractionsDetailView(DetailView, MultipleObjectMixin):
    """
    Класс отображает список всех взаимодействий c конкретномой компанией по pk.
    """
    model = Company
    paginate_by = 3
    query_pk_and_slug = True
    template_name = 'crm/company_interactions.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        object_list = Interaction.objects.filter(company=self.object)
        context = super(CompanyProjectInteractionsDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['current_order'] = self.get_ordering()
        return context


class ProjectCreateView(CreateView):
    """
    Класс создания записи о новом проекте.
    """
    model = Project
    fields = ['company', 'name', 'customer', 'description', 'start_date', 'end_date', 'price']

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        return context


class ProjectUpdateView(UpdateView):
    """
    Класс редаактированния записи о проекте на сайте.
    """
    model = Project
    fields = ['company', 'name', 'customer', 'description', 'start_date', 'end_date', 'price']
    template_name_suffix = '_update'


class ProjectDeleteView(DeleteView):
    """
    Класс для удаления записи о проекте из сайта.
    """
    query_pk_and_slug = True
    model = Project
    success_url = reverse_lazy('companies')


class ProjectInteractionsPhonesDetailView(DetailView, MultipleObjectMixin):
    """
    Класс отображает список взаимодействий по проекту с каналом связи - Телефонный звонок.
    """
    model = Project
    paginate_by = 3
    query_pk_and_slug = True
    template_name = 'crm/projectinteractions_detail_phones.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        object_list = Interaction.objects.filter(project=self.object)
        context = super(ProjectInteractionsPhonesDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['current_order'] = self.get_ordering()
        context['form'] = CompanyModelForm()
        return context


class ProjectInteractionsEmailDetailView(DetailView, MultipleObjectMixin):
    """
    Класс отображает список взаимодействий по проекту с каналом связи - Переписка по E-mail.
    """
    model = Project
    paginate_by = 3
    query_pk_and_slug = True
    template_name = 'crm/projectinteractions_detail_email.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        object_list = Interaction.objects.filter(project=self.object)
        context = super(ProjectInteractionsEmailDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['current_order'] = self.get_ordering()
        context['form'] = CompanyModelForm()
        return context


class ProjectInteractionsMessengerDetailView(DetailView, MultipleObjectMixin):
    """
    Класс отображает список взаимодействий по проекту с каналом связи - Переписка в мессенджере.
    """
    model = Project
    paginate_by = 3
    query_pk_and_slug = True
    template_name = 'crm/projectinteractions_detail_messenger.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        object_list = Interaction.objects.filter(project=self.object)
        context = super(ProjectInteractionsMessengerDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['current_order'] = self.get_ordering()
        context['form'] = CompanyModelForm()
        return context


class InteractionListView(ListView):
    """
    Класс отображает список всех взаимодействий на сайте.
    """
    model = Interaction
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        context = super(InteractionListView, self).get_context_data(**kwargs)
        context['current_order'] = self.get_ordering()
        return context

    def get_ordering(self):
        """
        Определяет по каким полям можно делать сортировку на странице.
        """
        ordering = self.request.GET.get('sort', '-created_date')
        return ordering if ordering in ('-project', 'channel_of_reference',
                                        'user', 'created_date', '-created_date', 'project') else '-created_date'

    def get_queryset(self):
        """
        Определяет список объектов модели Interaction, которые мы хотим отобразить.
        """
        qs = Interaction.objects.order_by(self.get_ordering())
        return qs


class InteractionManagerCRMListView(ListView):
    """
    Класс отображает список всех взаимодействий,
    автором которой является текущий пользователь со статусом - менеджер-CRM.
    """
    model = Interaction
    paginate_by = 5
    template_name = 'crm/manager_crm_interactions_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        if self.request.user.is_authenticated:
            context = super(InteractionManagerCRMListView, self).get_context_data(**kwargs)
            context['current_order'] = self.get_ordering()
            return context

    def get_ordering(self):
        """
        Определяет по каким полям можно делать сортировку на странице.
        """
        ordering = self.request.GET.get('sort', '-created_date')
        return ordering if ordering in ('-project', 'channel_of_reference',
                                        'created_date', '-created_date', 'project') else '-created_date'

    def get_queryset(self):
        """
        Определяет список объектов модели Interaction, которые мы хотим отобразить.
        """
        if self.request.user.is_authenticated:
            qs = Interaction.objects.order_by(self.get_ordering()).filter(user=self.request.user)
            return qs


class InteractionDetailView(DetailView):
    """
    Класс отображает информацию по конкретному взаимодействию по pk.
    """
    model = Interaction
    query_pk_and_slug = True


class CompanyInteractionsPhonesDetailView(DetailView, MultipleObjectMixin):
    """
    Класс отображает список взаимодействий с компанией имеющих канал связи - Телефонный звонок.
    """
    model = Company
    paginate_by = 3
    query_pk_and_slug = True
    template_name = 'crm/companyinteractions_detail_phones.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        object_list = Interaction.objects.filter(company=self.object)
        context = super(CompanyInteractionsPhonesDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['current_order'] = self.get_ordering()
        context['form'] = CompanyModelForm()
        return context


class CompanyInteractionsEmailDetailView(DetailView, MultipleObjectMixin):
    """
    Класс отображает список взаимодействий с компанией имеющих канал связи - Переписка по E-mail.
    """
    model = Company
    paginate_by = 3
    query_pk_and_slug = True
    template_name = 'crm/companyinteractions_detail_email.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        object_list = Interaction.objects.filter(company=self.object)
        context = super(CompanyInteractionsEmailDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['current_order'] = self.get_ordering()
        context['form'] = CompanyModelForm()
        return context


class CompanyInteractionsMessengerDetailView(DetailView, MultipleObjectMixin):
    """
    Класс отображает список взаимодействий с компанией имеющих канал связи - Переписка в мессенджере.
    """
    model = Company
    paginate_by = 3
    query_pk_and_slug = True
    template_name = 'crm/companyinteractions_detail_messenger.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает словарь, представляющий контекст шаблона.
        Приведенные аргументы ключевого слова составят возвращаемый контекст.
        """
        object_list = Interaction.objects.filter(company=self.object)
        context = super(CompanyInteractionsMessengerDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['current_order'] = self.get_ordering()
        context['form'] = CompanyModelForm()
        return context


class InteractionCreateView(FormView):
    """
    Класс по созданию записи о взаимодействии на сайте.
    """
    form_class = InteractionModelForm
    template_name = "crm/interaction_create.html"

    def form_valid(self, form):
        """
        Сохраняет данные о пользователе, который создал запись о взаимодействии.
        """
        self.interaction = form.save(commit=True)
        self.interaction.user = self.request.user
        self.interaction.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Определяет и перенаправляет на старницу информации о взаимодействии после его создания.
        :return:
        """
        url = reverse('interaction-detail', kwargs={'pk': self.interaction.pk})
        return url


class InteractionUpdateView(UpdateView):
    """
    Класс редаактированния записи о взаимодействии на сайте.
    """
    model = Interaction
    fields = ['project', 'channel_of_reference', 'reference_obj', 'company', 'description', 'rating']
    template_name_suffix = '_update'


class InteractionDeleteView(DeleteView):
    """
    Класс для удаления записи о взаимодействии из сайта.
    """
    model = Interaction
    success_url = reverse_lazy('interactions')


class AboutPageDetailView(ListView):
    """
    Класс для отображения страницы о сайте - О нас.
    """
    model = Company
    template_name = 'crm/about_page.html'
