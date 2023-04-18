from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

import json

app = FastAPI()

# Post Model

class Post(BaseModel):
    id: Optional[int or str ]
    name: str
    username: str
    email: str
    phone: str
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False


with open('mockInfo.json') as mockInfo:
    data = json.load(mockInfo)


@app.get('/')
def read_root():
    return {'Welcome': 'que pasa gonorrea2'}


@app.get('/posts')
def get_posts():
    print(len(data))
    return data


@app.post('/posts')
def save_user(post: Post):
    post.id = uuid()
    data.append(post.dict())
    return data[-1]

@app.get('/posts/{post_id}')
def get_post(post_id):
    print(post_id)
    for post in data:
        if str(post['id']) == post_id:
            return post
    raise HTTPException(status_code=404, detail="Nada se encuentra")

@app.delete('/posts/{post_id}')
def delete_post(post_id):
    for index, post in enumerate(data):
        print(post, '<------🟠')
        if str(post['id']) == post_id:
            data.pop(index)
            return {'message' : 'Se pudo borrar'}
    raise HTTPException(status_code=404, detail="Nada se encuentra")

@app.post('/posts/{post_id}')
def update_post(post_id, update_post: Post):
    for index, post in enumerate(data):
        if str(post['id']) == post_id:
            update_post.id = uuid()
            data.insert(index, update_post.dict())
            data.pop(index+1)
            return {'message' : 'Se actualizar'}
    raise HTTPException(status_code=404, detail="Nada se encuentra")