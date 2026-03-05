from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password: str

    todos: List['Todo'] = Relationship(back_populates="user")

    def set_password(self, plaintext_password):
        self.password = password_hash.hash(plaintext_password)

    def __str__(self) -> str:
        return f"(User id={self.id}, username={self.username}, email={self.email})"

class TodoCategory(SQLModel, table=True):
    todo_id: Optional[int] = Field(default=None, foreign_key='todo.id', primary_key=True)
    category_id: Optional[int] = Field(default=None, foreign_key='category.id', primary_key=True)

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    text: str = Field(max_length=255)

    
    user: User = Relationship()
    todos: List['Todo'] = Relationship(back_populates="categories", link_model=TodoCategory)

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    text: str = Field(max_length=255)
    done: bool = Field(default=False)

    
    user: User = Relationship(back_populates="todos")
    categories: List['Category'] = Relationship(back_populates="todos", link_model=TodoCategory)

    def toggle(self):
        self.done = not self.done
    
    
