from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,ListView,UpdateView,DetailView,TemplateView
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator

from styleshines.forms import RegistrationForm,LoginForm,CategoryAddForm,JewelleryAddForm,\
    JewelleryVarientsAddForm,OfferAddForm
from styleshines.models import User,Category,Jewellery,JewelleryVarients,Offers

# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'invalid session')
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
    return wrapper   


def is_admin(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_superuser:
            messages.error(request,'permission denied for current user!!!')
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
    return wrapper

desc=[signin_required,is_admin]

class SignUpView(CreateView):
    template_name='styleshines/register.html'
    model=User
    form_class=RegistrationForm
    success_url=reverse_lazy('signup')

    def form_valid(self, form):
        messages.success(self.request,'Successfully created account')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Failed to create account')
        return super().form_invalid(form)
    
class SignInView(FormView):
    template_name='styleshines/login.html'
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,'login successfully')
                return redirect('index')
            else:
                messages.error(request,'invalid username or password')
                return render(request,self.template_name,{'form':form})
            
# --------------------------view for Category Adding and Listing------------------------------------------

@method_decorator(desc,name='dispatch')
class CategoryAddView(CreateView,ListView):
    template_name='styleshines/category_add.html'
    form_class=CategoryAddForm
    model=Category
    context_object_name='categories'
    success_url=reverse_lazy('cat-add')

    def form_valid(self, form):
        messages.success(self.request,'Successfully Added Category')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Failed to Add Category')
        return super().form_invalid(form)
    
    def get_queryset(self):
        qs=Category.objects.filter(is_active=True)
        return qs
    
# -------------------------- View for Remove Category (inactive not delete)-------------------------------

@signin_required
@is_admin
def remove_categories(request,*args,**kwargs):
    id=kwargs.get('pk')
    Category.objects.filter(id=id).update(is_active=False)
    messages.success(request,'Category-removed')
    return redirect('cat-add')
    
# -------------------------- View for Add Jewellery------------------------------------------------------------

@method_decorator(desc,name='dispatch')
class JewelleryCreateView(CreateView):
    template_name='styleshines/jewellery_add.html'
    form_class=JewelleryAddForm
    model=Jewellery
    success_url=reverse_lazy('jewellery-list')

    def form_valid(self, form):
        messages.success(self.request,'Successfully Added jewellery')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Failed to Add jewellery')
        return super().form_invalid(form)

# --------------------View for List jewellery------------------------------------------------------------

@method_decorator(desc,name='dispatch')
class JewelleryListView(ListView):
    template_name='styleshines/jewellery_list.html'
    context_object_name='Jewellery'
    model=Jewellery


# --------------------View for Update jewellery------------------------------------------------------------

@method_decorator(desc,name='dispatch')
class JewelleryUpdateView(UpdateView):
    template_name='styleshines/jewellery_edit.html'
    form_class=JewelleryAddForm
    model=Jewellery
    success_url=reverse_lazy('jewellery-list')

    def form_valid(self, form):
        messages.success(self.request,'Successfully Updated jewellery')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Failed to Update jewellery')
        return super().form_invalid(form)

# ---------------------------View for Remove jewellery-------------------------------------------------------

@signin_required
@is_admin
def remove_jewellery(request,*args,**kwargs):
    id=kwargs.get('pk')
    Jewellery.objects.filter(id=id).delete()
    messages.success(request,'Plant removed')
    return redirect('jewellery-list')

# ---------------------------View for Add jewellery Varients---------------------------------------------

@method_decorator(desc,name='dispatch')
class JewelleryVarientsAddView(CreateView):
    template_name='styleshines/jewellery_varient_add.html'
    form_class=JewelleryVarientsAddForm
    model=JewelleryVarients
    success_url=reverse_lazy('jewellery-list')

    def form_valid(self, form):
        id=self.kwargs.get('pk')
        obj=Jewellery.objects.get(id=id)
        form.instance.jewel=obj
        messages.success(self.request,'Successfully Added jewellery Varients')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Failed to Add jewellery Varients')
        return super().form_invalid(form)

# ---------------------------View for jewellery Details------------------------------------------------

@method_decorator(desc,name='dispatch')
class JewelleryDetailView(DetailView):
    template_name='styleshines/jewellery_detail.html'
    model=Jewellery
    context_object_name='jewellery'

# ----------------------------View for Update Jewellery Varient -------------------------------------

@method_decorator(desc,name='dispatch')
class JewelleryVarientUpdateView(UpdateView):
    template_name='styleshines/varient_edit.html'
    form_class=JewelleryVarientsAddForm
    model=JewelleryVarients
    success_url=reverse_lazy('jewellery-list')

    def form_valid(self, form):
        messages.success(self.request,'Successfully Updated Jewellery Varients')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,'Failed to Update jewellery Varients')
        return super().form_invalid(form)
    
    def get_success_url(self):
        id=self.kwargs.get("pk")
        jewellery_varient_object=JewelleryVarients.objects.get(id=id)
        jewellery_id=jewellery_varient_object.jewel.id
        return reverse("jewellery-detail",kwargs={"pk":jewellery_id})
    
# ----------------------------View for Remove jewellery Varient----------------------------------------

@signin_required
@is_admin
def remove_jewellery_varient(request,*args,**kwargs):
    id=kwargs.get('pk')
    JewelleryVarients.objects.filter(id=id).delete()
    messages.success(request,'jewellery Varient removed')
    return redirect('jewellery-list')


# ----------------------------View for add offer ----------------------------------------

@method_decorator(desc,name='dispatch')
class OfferAddView(CreateView):
    template_name='styleshines/offer_add.html'
    form_class=OfferAddForm
    model=Offers
    success_url=reverse_lazy('jewellery-list')

    def form_valid(self, form):
        id=self.kwargs.get('pk')
        obj=JewelleryVarients.objects.get(id=id)
        form.instance.jewel_varient=obj
        messages.success(self.request,'Successfully Added Offers')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,'Failed to Add Offers')
        return super().form_invalid(form)
    
    def get_success_url(self):
        # lh:8000/jewellery/int:pk
        id=self.kwargs.get('pk')
        jewellery_varient_object=JewelleryVarients.objects.get(id=id)
        jewellery_id=jewellery_varient_object.jewel.id
        return reverse('jewellery-detail',kwargs={'pk':jewellery_id})
        # return super().get_success_url()

# ----------------------- remove offer-----------------------------

@signin_required
@is_admin
def remove_offers(request,*args,**kwargs):
    id=kwargs.get('pk')
    offer_object=Offers.objects.get(id=id)
    jewellery_id=offer_object.jewel_varient.jewel.id
    offer_object.delete()
    messages.success(request,'Removed offer')
    return redirect('jewellery-detail',pk=jewellery_id)




class IndexView(TemplateView):
    template_name='styleshines/index.html'

