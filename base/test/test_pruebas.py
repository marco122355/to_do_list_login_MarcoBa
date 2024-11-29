from django.test import TestCase
from base.models import Task  # Importación corregida a absoluta
from django.urls import reverse
from django.contrib.auth.models import User

class TaskTestCase(TestCase):
    
    def setUp(self):
        # Crear un usuario y autenticarlo para las pruebas
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')  # Simular el inicio de sesión
        Task.objects.create(title="Tarea de prueba", description="Descripción de prueba", complete=False, user=self.user)

    def test_task_creation(self):
        """Probar si se puede crear una tarea correctamente"""
        tarea = Task.objects.get(title="Tarea de prueba")
        self.assertEqual(tarea.title, "Tarea de prueba")
        self.assertEqual(tarea.description, "Descripción de prueba")
        self.assertFalse(tarea.complete)

    def test_create_task_empty_title(self):
        """Probar creación de tarea con título vacío"""
        response = self.client.post(reverse('task-create'), {'title': '', 'description': 'Descripción de prueba'})
        
        # Verificar que se devuelva el formulario con errores de validación
        self.assertEqual(response.status_code, 200)
        
        # Verificar que el formulario tiene el error en el campo 'title'
        form = response.context.get('form')
        self.assertIsNotNone(form)  # Confirma que el formulario está en el contexto
        self.assertTrue(form.errors.get('title'))  # Verifica que hay un error en 'title'
        self.assertEqual(form.errors['title'][0], "This field is required.")

    def test_delete_task(self):
        """Probar eliminación de una tarea"""
        # Crear la tarea para el usuario de prueba
        tarea = Task.objects.create(title="Tarea de prueba", description="Descripción de prueba", complete=False, user=self.user)
    
        # Intentar eliminar la tarea
        response = self.client.post(reverse('task-delete', args=[tarea.id]))
        self.assertEqual(response.status_code, 302)  # Verifica que fue redirigido después de la eliminación
        self.assertFalse(Task.objects.filter(id=tarea.id).exists())  # Verifica que la tarea ya no exista

    def test_update_task(self):
        """Probar actualización de una tarea"""
        tarea = Task.objects.get(title="Tarea de prueba")
        response = self.client.post(reverse('task-update', args=[tarea.id]), {
            'title': 'Tarea actualizada', 
            'description': 'Descripción actualizada', 
            'complete': True
        })

        tarea.refresh_from_db()  # Refresca la tarea desde la base de datos
        self.assertEqual(tarea.title, 'Tarea actualizada')  # Verifica que el título se haya actualizado
        self.assertEqual(tarea.description, 'Descripción actualizada')  # Verifica que la descripción se haya actualizado
        self.assertTrue(tarea.complete)  # Verifica que la tarea esté marcada como completa
        self.assertRedirects(response, reverse('tasks'))  # Verifica la redirección

    def test_login(self):
        """Probar el proceso de inicio de sesión"""
        response = self.client.post('/login/', {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_create_complete_task(self):
        """Probar la creación de una tarea marcada como completa"""
        response = self.client.post('/task-create/', {'title': 'Nueva tarea', 'description': 'Tarea completa', 'complete': True})
        tarea = Task.objects.get(title="Nueva tarea")
        self.assertTrue(tarea.complete)
        
    def test_task_list_with_search_input(self):
        """Probar TaskList con un término de búsqueda"""
        response = self.client.get(reverse('tasks') + '?search-area=Tarea')
        self.assertEqual(response.status_code, 200)
        self.assertIn('search_input', response.context)  # Verifica que 'search_input' esté en el contexto
        self.assertEqual(response.context['search_input'], 'Tarea')  # Verifica que el término de búsqueda sea 'Tarea'

        # Verificar que las tareas en el contexto contienen el término de búsqueda
        tasks = response.context['tasks']
        for task in tasks:
            self.assertIn('Tarea', task.title)
