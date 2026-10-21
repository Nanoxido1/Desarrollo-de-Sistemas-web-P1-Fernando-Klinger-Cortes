from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Producto, Pedido, Categoria
from .forms import PedidoForm

# Vista de Catálogo de Productos con Filtros Dinámicos[cite: 2]
def catalogo_productos(request):
    productos = Producto.objects.all()
    refrigerado = request.GET.get('refrigerado')
    
    if refrigerado == '1':
        productos = productos.filter(requiere_refrigeracion=True)
    elif refrigerado == '0':
        productos = productos.filter(requiere_refrigeracion=False)

    return render(request, 'gestion_pedidos/catalogo.html', {
        'productos': productos
    })

# Vista de Registro de Pedido + Reto A (Control Automático de Inventario)
def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            
            # RETO A: Descontar stock del producto al comprar
            if pedido.producto:
                if pedido.producto.stock <= 0:
                    form.add_error('producto', 'El producto seleccionado no tiene stock disponible.')
                    return render(request, 'gestion_pedidos/formulario_pedido.html', {'form': form})
                
                # Descuenta 1 unidad del stock
                pedido.producto.stock -= 1
                pedido.producto.save()

            pedido.save()
            return redirect('catalogo_productos')
    else:
        form = PedidoForm()

    return render(request, 'gestion_pedidos/formulario_pedido.html', {'form': form})

# RETO B: Dashboard de Resumen Operativo[cite: 3]
def dashboard(request):
    total_pedidos = Pedido.objects.count()
    pedidos_express = Pedido.objects.filter(modalidad='EXPRESS').count()
    pedidos_pickup = Pedido.objects.filter(modalidad='PICKUP').count()
    ingresos_totales = Pedido.objects.aggregate(total=Sum('total_estimado'))['total'] or 0

    return render(request, 'gestion_pedidos/dashboard.html', {
        'total_pedidos': total_pedidos,
        'pedidos_express': pedidos_express,
        'pedidos_pickup': pedidos_pickup,
        'ingresos_totales': ingresos_totales,
    })