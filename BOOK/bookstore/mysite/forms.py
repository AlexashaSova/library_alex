from django import forms
from django.views.generic import FormView
from django.core.validators import RegexValidator, EmailValidator, validate_email, MaxValueValidator, MinValueValidator
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class RegisterFormView(FormView):
    form_class = UserCreationForm
    template_name = "mysite/register.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


class AuthForm(FormView):
    form_class = AuthenticationForm
    template_name = 'mysite/login.html'
    success_url = '/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(AuthForm, self).form_valid(form)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"user-box"}))
    password = forms.CharField(widget=forms.TextInput(attrs={"class":"user-box"}))



class PostForm(forms.Form):
    book_name = forms.CharField(max_length=256, label='',  required=False,
                                widget=forms.TextInput(attrs={'style': 'outline:none; border: 1px solid #D0CFCE; '
                                                                       'width:200px; border-radius: 5px;'}))

class AddBookForm(forms.ModelForm):
    book_name = models.CharField(max_length=256)
    book_author = models.CharField(max_length=256)
    book_description = forms.CharField(widget=forms.Textarea, max_length=600)
    book_amount = models.IntegerField()
    book_price = models.DecimalField(max_digits=10, decimal_places=0)
    book_available = models.CharField(max_length=20)
    book_image = models.CharField(max_length=256, blank=True, null=True,)

    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['book_description'].widget.attrs['cols'] = 50
        self.fields['book_description'].widget.attrs['rows'] = 6

    class Meta:
        model = Book
        exclude = {}
        fields = [
            'id_category_id',
            'book_name',
            'book_author',
            'book_description',
            'book_amount',
            'book_price',
            'book_available',
            'book_image'
        ]
        labels = {
            'id_category_id': 'Категория',
            'book_name': 'Название книги',
            'book_author': 'Автор',
            'book_description': 'Описание',
            'book_amount': 'Количество на складе',
            'book_price': 'Цена',
            'book_available': 'Наличие',
            'book_image': 'Изображение',
        }


class ChangeBookForm(forms.ModelForm):
    book_name = models.CharField(max_length=256)
    book_author = models.CharField(max_length=256)
    book_description = forms.CharField(widget=forms.Textarea, max_length=600)
    book_amount = models.IntegerField()
    book_price = models.DecimalField(max_digits=10, decimal_places=0)
    book_available = models.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        super(ChangeBookForm, self).__init__(*args, **kwargs)
        self.fields['book_description'].widget.attrs['cols'] = 50
        self.fields['book_description'].widget.attrs['rows'] = 6

    class Meta:
        model = Book
        exclude = {}
        fields = [
            'id_category_id',
            'book_name',
            'book_author',
            'book_description',
            'book_amount',
            'book_price',
            'book_available',
            'book_image'
        ]
        labels = {
            'id_category_id': 'Категория',
            'book_name': 'Название книги',
            'book_author': 'Автор',
            'book_description': 'Описание',
            'book_amount': 'Количество на складе',
            'book_price': 'Цена',
            'book_available': 'Наличие',
            'book_image': 'Image'
        }


class AmountForm(forms.Form):
    def __init__(self, minval, maxval, *args, **kwargs):
        super(AmountForm, self).__init__(*args, **kwargs)
        self.fields['amount'] = forms.IntegerField(label="Кол-во", widget=forms.NumberInput(attrs={'style': 'width: 50px'}), validators=[
            MaxValueValidator(maxval, message="Недостаточно товара на складе"),
            MinValueValidator(1, message="Вы не можете купить столько единиц товара")
        ], error_messages = {
                 'MaxValueValidator':"Please Enter your Name",
                    'MinValueValidator':'Please Enter your Name'
                 })

class ProfileChangeForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False, validators=[RegexValidator(r'^[a-zA-ZА-Яа-яїіёЇІЁЄє]*$', 'Введите корректное имя')],
                                 widget=forms.TextInput(attrs={'style': 'outline:none; border: 1px solid #D0CFCE; width:200px; border-radius: 5px;'}))
    last_name = forms.CharField(max_length=150, required=False, validators=[RegexValidator(r'^[a-zA-ZА-Яа-яїіёЇІЁЄє]*$', 'Введите корректную фамилию')],
                                widget=forms.TextInput(attrs={'style': 'outline:none; border: 1px solid #D0CFCE; width:200px; border-radius: 5px;'}))
    email = forms.CharField(max_length=100, required=False, validators=[validate_email],
                            widget=forms.TextInput(attrs={'style': 'outline:none; border: 1px solid #D0CFCE; width:200px; border-radius: 5px;'}))
    telephone_num = forms.CharField(max_length=20, required=False, validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Введите корректный номер телефона')],
                                    widget=forms.TextInput(attrs={'style': 'outline:none; border: 1px solid #D0CFCE; width:200px; border-radius: 5px;'}))


    def __init__(self, *args, **kwargs):
        super(ProfileChangeForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['email'].widget.attrs['cols'] = 50
        self.fields['email'].widget.attrs['rows'] = 2

    class Meta:
        fields = [
            'first_name',
            'last_name',
            'email',
            'telephone_num'
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
            'telephone_num' : 'Номер телефона'
        }


class DeliveryForm(forms.ModelForm):

    class Meta:
        model = Delivery
        fields = [
            'client_address',
        ]
        labels = {
            'client_address': 'Адрес',
        }


class OrderForm(ProfileChangeForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'style': 'outline:none; border: 1px solid #D0CFCE; width:200px; border-radius: 5px;'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'style': 'outline:none; border: 1px solid #D0CFCE; width:200px; border-radius: 5px;'}))
    email = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'style': 'outline:none; border: 1px solid #D0CFCE; width:200px; border-radius: 5px;'}))
    telephone_num = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
                                        'style': 'outline:none; border: 1px solid #D0CFCE; width:200px; border-radius: 5px;'}))


class StatusForm(forms.Form):
    def __init__(self, variatins, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['status'] = forms.ChoiceField(label="", initial='', widget=forms.Select(attrs={'class' : 'myfieldclass'}), choices=variatins, required=True)