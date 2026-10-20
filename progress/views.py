from django.http import HttpResponse

def home(request):
    html_content = """
    <html>
        <head>
            <title>Філософська LMS</title>
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1>Вітаємо в системі організації філософського контенту!</h1>
            <p>Ваш Django-проєкт успішно запущено.</p>
            <br>
            <a href="/admin/" style="padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">
                Увійти в Адмін-панель
            </a>
        </body>
    </html>
    """
    return HttpResponse(html_content)