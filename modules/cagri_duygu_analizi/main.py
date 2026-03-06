from pydantic import BaseModel

class TaskInput(BaseModel):
    payload: str

async def run(task: TaskInput) -> dict:
    return {'status': 'AI pasif', 'module': 'cagri_duygu_analizi', 'payload': task.payload}
