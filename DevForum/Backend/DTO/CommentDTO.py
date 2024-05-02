import reflex as rx

class CommentDTO(rx.Base):

    commentId:str
    postId:str
    username:str
    imgProfile:str
    comment:str
    date:str

