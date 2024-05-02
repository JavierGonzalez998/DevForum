import reflex as rx

class LoadingState(rx.State):
    Loading: bool = False

    def ChangeState(self, state:bool):
        self.Loading = state