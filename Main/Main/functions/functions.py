
def handle_uploaded_file(f):  
    with open('Main/static/upload/text.txt', 'wb+') as destination:
        for chunk in f.chunks():  
            destination.write(chunk)
