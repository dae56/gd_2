from pydantic import BaseModel, Field


class CreateTaskScheme(BaseModel):
    name: str = Field(max_length=50)
    text: str = Field(max_length=1000)


class TaskScheme(CreateTaskScheme):
    id: int
    user_id: int
