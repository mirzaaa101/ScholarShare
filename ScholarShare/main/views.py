from django.shortcuts import render

def welcoming_page(request):
    image_filenames = [
        'review1.jpg',
        'review2.jpg',
        'review3.jpg',
        'review4.jpg',
        'review5.jpg',
        'review6.jpg',
    ]
    return render(request, 'welcoming_page.html',{'image_filenames': image_filenames})
