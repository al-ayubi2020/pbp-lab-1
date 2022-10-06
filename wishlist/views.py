from django.shortcuts import render, redirect
from wishlist.models import BarangWishlist
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    context = {
    'list_barang': data_barang_wishlist,
    'nama': 'Muhammad Hilman Al Ayubi',
    }
    return render(request, "wishlist.html", context)

@login_required(login_url='/wishlist/login/')
def show_wishlist_ajax(request):
    context = {
    'nama': 'Muhammad Hilman Al Ayubi',
    }
    return render(request, "wishlist_ajax.html", context)

@login_required(login_url='/wishlist/login/')
def create(request):
    if request.method == 'POST':
        nama_barang = request.POST.get('nama_barang')
        harga_barang = request.POST.get('harga_barang')
        deskripsi = request.POST.get('deskripsi')
        item = BarangWishlist(nama_barang=nama_barang, harga_barang=harga_barang, deskripsi=deskripsi)
        item.save()
        return HttpResponseRedirect(reverse("wishlist:show_wishlist_ajax")) 
    
    context = {}
    return render(request, "create.html", context)

def show_xml(request):
    return HttpResponse(serializers.serialize("xml", data_barang_wishlist), content_type="application/xml")

def show_json(request):
    return HttpResponse(serializers.serialize("json", data_barang_wishlist), content_type="application/json")

def show_xml_by_id(request, id):
    data_barang_wishlist_by_id = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data_barang_wishlist_by_id), content_type="application/xml")

def show_json_by_id(request, id):
    data_barang_wishlist_by_id = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data_barang_wishlist_by_id), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('wishlist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            response = HttpResponseRedirect(reverse("wishlist:show_wishlist")) 
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('wishlist:login'))
    response.delete_cookie('last_login')
    return response


data_barang_wishlist = BarangWishlist.objects.all()

context = {
    'list_barang': data_barang_wishlist,
    'nama': 'Muhammad Hilman Al Ayubi',
}