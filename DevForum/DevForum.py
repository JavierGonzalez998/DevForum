import reflex as rx
from DevForum.Pages.forum import index as forum
from DevForum.Pages.categories import index as categories
from DevForum.Pages.login import index as login
from DevForum.Pages.profile import index as profile
from DevForum.Pages.index import index
from DevForum.Pages.post import index as post
from DevForum.Backend.app import hello
from DevForum.Pages.catDetails import index as catDetail
from DevForum.Pages.searchPost import index as Search,HandlePostState


app = rx.App(stylesheets=[
        "/animate.min.css",  # This path is relative to assets/
        "/main.css",
    ])


app.add_page(index)
app.add_page(forum, route="/forum")
app.add_page(categories, route="/categories")
app.add_page(login, route="/login")
app.add_page(profile, route="/profile")
app.add_page(catDetail, route="/categories/[detail]")
app.add_page(post, route="/post/[id]")
app.add_page(Search, route="/search/[text]", on_load=[HandlePostState.getItemLink, HandlePostState.getSearch])
#Backend
app.api.add_api_route("/hello", hello)
