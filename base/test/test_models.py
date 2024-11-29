# base/tests/test_models.py
import pytest
from base.models import Task

@pytest.mark.django_db
def test_create_task():
    task = Task.objects.create(title="Sample Task", complete=False)
    assert task.title == "Sample Task"
    assert not task.complete
