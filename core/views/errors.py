from django.shortcuts import render, redirect

def custom_403(request, exception=None):
    # Redireciona para a página inicial em caso de erro 403 (Proibido/Permissão negada)
    return redirect('core:home')

def custom_404(request, exception=None):
    # Renderiza a página customizada de erro 404 (Não Encontrado)
    return render(request, 'core/errors/404.html', status=404)

def custom_500(request, exception=None):
    # Renderiza a página customizada de erro 500 (Erro Interno do Servidor)
    return render(request, 'core/errors/500.html', status=500)
