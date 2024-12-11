from typing import Optional
from fastapi import Body, FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor
import psycopg2
import time


app = FastAPI()



##### Database Connection
while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='postgres',
                                password='12345',
                                cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print('Database connection established')
        break
    except Exception as error:
        print('Error connecting to database failed')
        print(error)
        time.sleep(2)
    

my_posts = [
    {
    "title":"title of post 1",
    "content":"content of post 1",
    "id": 1
},
   {
    "title":"title of post 2",
    "content":"content of post 2",
    "id": 2
}]



 


###### Get methos
@app.get("/")
async def root():
    return {'message':"Hello World 123"}




###### Get methos
@app.get("/posts")
def get_posts():
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()
    return {"data":my_posts}




###### Post methos
# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"msg":"successfully created posts"}

# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"msg":f"title {payLoad['title']} and content {payLoad['content']}"}


class Post(BaseModel):
    title:str
    content:str
    published: bool = True
    rating: Optional[int] = None

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000)
    my_posts.append(post_dict)
    return {'data':post_dict}



# get individual post

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"details": post}
     

@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f'post with id: {id} was not found'}
    return {"post_details":post}






#########delete post
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    # deleting post
    # find the index of the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)




###### update post
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data':post_dict}
    