from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from Hello import forms
from Hello.util import record_access


def index(request):
    return render(request, "index.html")


@record_access
def place_holder(request, height, width, color):
    ph = forms.PlaceHolderImage({'height':height,'width':width, 'bg_color':int('0x'+color, 16)})
    if not ph.is_valid(): raise Http404("Invalid Request")
    p = ph.generate()
    return HttpResponse(p, content_type='image/png')


@record_access
def human_face(request):
    hf = forms.HumanFace64()
    face = hf.generate()
    return HttpResponse(face, content_type='image/png')


@record_access
def random_pixels(request,h,w,cell_size,color):
    rp = forms.Pixels({'h':h,'w':w,'cell_size':cell_size,'color':int('0x'+color, 16)})
    if not rp.is_valid(): raise Http404("Invalid Request")
    p = rp.generate()
    return HttpResponse(p, content_type='image/png')


@record_access
def mosaic(request,h,w,cell_size,color):
    m = forms.Mosaic({'h':h,'w':w,'cell_size':cell_size,'color':int('0x'+color,16)})
    if not m.is_valid(): raise Http404("Invalid Request")
    p = m.generate()
    return HttpResponse(p, content_type='image/png')














