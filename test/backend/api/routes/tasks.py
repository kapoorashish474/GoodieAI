"""
Task-related API routes.
"""

from fastapi import APIRouter
from ...tasks.story_tasks import fetch_and_process_stories, update_analytics_summary
from ...core.celery_app import celery_app

router = APIRouter()


@router.post("/tasks/fetch-stories/")
def trigger_fetch_stories():
    """Trigger background task to fetch and process stories."""
    task = fetch_and_process_stories.delay()
    return {"task_id": task.id, "status": "started"}


@router.post("/tasks/update-analytics/")
def trigger_update_analytics():
    """Trigger background task to update analytics summary."""
    task = update_analytics_summary.delay()
    return {"task_id": task.id, "status": "started"}


@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    """Get the status of a background task."""
    task_result = celery_app.AsyncResult(task_id)
    
    if task_result.state == 'PENDING':
        response = {
            'state': task_result.state,
            'current': 0,
            'total': 1,
            'status': 'Task is pending...'
        }
    elif task_result.state != 'FAILURE':
        response = {
            'state': task_result.state,
            'current': task_result.info.get('progress', 0),
            'total': 100,
            'status': task_result.info.get('status', '')
        }
        if 'result' in task_result.info:
            response['result'] = task_result.info['result']
    else:
        # Something went wrong in the background job
        response = {
            'state': task_result.state,
            'current': 1,
            'total': 1,
            'status': str(task_result.info),  # This is the exception raised
        }
    
    return response 