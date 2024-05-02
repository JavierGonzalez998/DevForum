import reflex as rx
from DevForum.Backend.Models.Comment import Comment
from typing import List
class DTOPostDetail(rx.Base):
    postId: int
    title: str
    desc: str
    content: str
    username: str
    cat: str
    posted_at:str
    updated_at: str
    comments:List[Comment]

class DTORankPost(rx.Base):
    postId: int
    title: str
    desc: str
    username: str
    cat: str
    posted_at:str
    comments: int