from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     # print(db.query(models.Post))  # print the actual sql query
#     return {"data": posts}


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,  # query param
    skip: int = 0,  # query param
    search: Optional[str] = "",  # query param for search
):
    print(limit)

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    print(posts)
    # return {"data": my_posts}
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()  # fetch all the data from the database
    # print(posts)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    print(current_user.email)

    new_post = models.Post(
        owner_id=current_user.id, **post.model_dump()
    )  # ** is used to unpack the dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()  # fetch the new post
    # conn.commit()  # commit the changes

    # print(post)  # can acess params using . operator
    # print(post.model_dump())  # if want to convert to dict
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0, 1000)
    # my_posts.append(post_dict)
    return new_post


# @router.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return {"detail": post}


# Note : control will match posts/latest first so this will be called , if latest is written after /posts/{id} then if we try to call posts/latest then it will throw error as it will be taken as id so , always keep api like this before api containing path params


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    # # post = find_post(id)
    # # return {"post_detail": f"Here is the detail of post : {id}"}
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} was not found",
        )
    # if post.owner_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to perform requested action",
    #     )
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id : {id} was not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} does not exist",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    post_query.delete(
        synchronize_session=False
    )  # synchronize_session=False will not commit the changes
    db.commit()

    # index = find_index_post(id)  # find the index of the post
    # if deleted_post == None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"post with id : {id} does not exist",
    #     )
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(
    id: int,
    updated_data: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )
    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.update(updated_data.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(existing_post)

    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    # index = find_index_post(id)
    # if updated_post == None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"post with id : {id} was not found",
    #     )
    # post_dict = post.model_dump()  # convert to dict
    # post_dict["id"] = id  # update the id
    # my_posts[index] = post_dict  # update the post
    return post_query.first()  # return the updated post
