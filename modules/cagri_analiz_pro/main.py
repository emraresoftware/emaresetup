from pydantic import BaseModel

class TaskInput(BaseModel):
    payload: str

async def run(task: TaskInput) -> dict:
    return {'status': 'fallback', 'module': 'cagri_analiz_pro', 'payload': task.payload}
