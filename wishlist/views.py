from django.shortcuts import render, redirect
from wishlist.models import BarangWishlist
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.contrib.auth.models import User
import datetime

# Create your views here.
@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
    'list_barang': data_barang_wishlist,
    'nama': 'Muhammad Hilman Al Ayubi',
    }
    return render(request, "wishlist.html", context)

@login_required(login_url='/wishlist/login/')
def show_wishlist_ajax(request):
    data_barang_wishlist = BarangWishlist.objects.all()
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
        return JsonResponse({"instance": "Proyek Dibuat"}, status=200)
    
    return render(request, "create.html")

def show_xml(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("xml", data_barang_wishlist), content_type="application/xml")

def show_json(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("json", data_barang_wishlist), content_type="application/json")

def show_xml_by_id(request, id):
    data_barang_wishlist_by_id = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data_barang_wishlist_by_id), content_type="application/xml")

def show_json_by_id(request, id):
    data_barang_wishlist_by_id = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data_barang_wishlist_by_id), content_type="application/json")

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = UserCreationForm(request.POST)
        if username and password:
            try:
                acc = User.objects.create(username=username)
                if acc:
                    acc.set_password(password)
                    acc.save()
                    messages.success(request, 'Akun telah berhasil dibuat!')
                    return redirect('wishlist:login')
                else:
                    messages.success(request, 'Terjadi masalah!')
            except:
                messages.success(request, 'Username sudah pernah digunakan!')
        else:
            messages.success(request, 'Tidak boleh kosong!')

    
    context = {}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            response = HttpResponseRedirect(reverse("wishlist:show_wishlist_ajax")) 
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

@login_required(login_url='/wishlist/login/')
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('wishlist:login'))
    return response