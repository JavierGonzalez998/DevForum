import reflex as rx
from DevForum.Backend.DTO.CommentDTO import CommentDTO
from DevForum.Backend.Models.Comment import Comment
from DevForum.States.UserCookies import userCookie
from DevForum.Backend.Models.Auth import Auth
from typing import List
import sqlalchemy
class BackendComment(rx.State):
    ListOfComment: List[CommentDTO] = []
    count: int = 0
    comment:str = ""

    def loadCommentPosts(self, idPost):
        with rx.session() as session:
            aux = session.exec(
                sqlalchemy.text(f'''select c."commentId", c.post_id , u.profileimg , u.username , c."comment" , c."date"  from "comment" c inner join "user" u on u."userId" = c.user_id where c."commentId" = {idPost} order by c."date" desc''')
            )
            del self.ListOfComment[:]
            self.count = 0
            for row in aux:
                row_as_dict = row._mapping
                res = CommentDTO(commentId=row_as_dict['commentId'], postId=row_as_dict["post_id"], username=row_as_dict["username"], imgProfile=row_as_dict["profileimg"], comment=row_as_dict["comment"], date=row_as_dict["date"])
                self.ListOfComment.append(res)
                self.count = self.count + 1

    async def submitComment(self, postId):
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            res = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()
        if res is not None:
            with rx.session() as session:
                session.add(
                    Comment(
                        post_id=postId,
                        user_id=res.user_id,
                        comment=self.comment
                    )
                )
                session.commit()
                self.comment = ""
            return True
        else:
            return False