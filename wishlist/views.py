from django.shortcuts import render
from wishlist.models import BarangWishlist
from django.http import HttpResponse
from django.core import serializers

# Create your views here.
def show_wishlist(request):
    return render(request, "wishlist.html", context)

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

data_barang_wishlist = BarangWishlist.objects.all()

context = {
    'list_barang': data_barang_wishlist,
    'nama': 'Muhammad Hilman Al Ayubi'
}