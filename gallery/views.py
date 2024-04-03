from django.shortcuts import render, redirect

from .forms import PhotoForm
from .models import Photo


def gallery(request):
    photos = Photo.objects.all()
    context = {"photos": photos}
    return render(request, "gallery/index.html", context)


def gallery_upload(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    form = PhotoForm()
    context = {"form": form}
    return render(request, "gallery/upload.html", context)
