from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Producto
from .forms import ProductoForm

# Create your views here.
def home(request):
    productos= Producto.objects.all()
    data={"productos": productos}
    return render(request,'tienda/index.html',data)

def login(request):
    context = {}
    return render(request, 'tienda/login.html', context)


def catalogo(request):
    productos= Producto.objects.all()
    context = {"productos":productos}
    return render(request, 'tienda/catalogo.html', context)


def agregar_producto(request):
    data= {'form': ProductoForm()}

    if request.method =='POST':
        formulario=ProductoForm(data=request.POST,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"]= "guardado corretamente"

        else:
            data['form']=formulario
    return render( request,'tienda/producto/agregar.html',data)

@login_required
def listar_producto(request):
    productos= Producto.objects.all()
    data={'productos':productos}
    return render(request,'tienda/producto/listar.html',data)

@login_required
def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    data = {'form': ProductoForm(instance=producto)}
    if request.method =='POST':
        formulario = ProductoForm(data=request.POST,instance=producto,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"]="Producto modificado con exito"
            return redirect(to="listar-producto")
        data['form']=formulario

    return render(request,'tienda/producto/modificar.html',data)

@login_required
def eliminar_producto(request, id):
    producto= get_object_or_404(Producto,id_producto=id)
    producto.delete()
    return redirect(to="listar-producto")

def salir(request):
    logout(request)
    return redirect('/')

