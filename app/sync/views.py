from django.shortcuts import render


def confirm_sync(request):
    return render(request, 'sync/confirm_sync.html')


def sync_success(request):
    return render(request, 'sync/sync_success.html')
