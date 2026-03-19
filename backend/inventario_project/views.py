from django.shortcuts import redirect

def root_redirect(request):
    """Redirige '/' al dashboard."""
    return redirect('dashboard')