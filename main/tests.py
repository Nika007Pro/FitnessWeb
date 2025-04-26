from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

class RegistrationTest(TestCase):
    def test_registration_view(self):
        data = {
            'login': 'testuser',
            'email': 'testuser@example.com',
            'pass1': 'testpassword',
            'pass2': 'testpassword',
        }
        # Отправляем POST-запрос на URL для регистрации
        response = self.client.post(reverse('register'), data)
        # Проверяем, что после успешной регистрации происходит перенаправление
        self.assertEqual(response.status_code, 302)
        # Проверяем, что создан новый пользователь с указанным именем
        self.assertTrue(User.objects.filter(username='testuser').exists())
        # Проверяем, что произошло перенаправление на страницу входа
        self.assertRedirects(response, reverse('auth'))
        # Проверяем, что доступ к странице входа разрешен после регистрации
        response = self.client.get(reverse('auth'))
        self.assertEqual(response.status_code, 200)  # Ожидаем успешный доступ
        # Проверяем, что используется правильный шаблон для страницы входа
        self.assertTemplateUsed(response, 'main/login.html')




