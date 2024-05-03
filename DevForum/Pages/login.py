import reflex as rx
from DevForum.Components.navbar import navbar
from DevForum.Backend.Controllers.UserController import userAuth
from DevForum.Backend.Controllers.UserController import userData

class FormState(rx.State):
    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data

class LoginState(rx.State):
    loginSection: bool = True
    loginValidation: bool = False

    def setLoginSection(self):
        self.loginSection = not self.loginSection
    def setLoginValidation(self, state:bool):
        self.loginValidation = state

class LoginBackend(rx.State):

    async def setLogin(self):
        state = await self.get_state(userAuth)

        await state.LoginUser()
        if state.response is not None:
            LoginState.setLoginValidation(False)
            return rx.redirect("/profile")
        else:
           return LoginState.setLoginValidation(True)
 
def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.box(
            rx.callout(
                "Mensaje del dev: Hice algunos cambios en la base de datos y arreglé algunas funciones. Quienes tengan una cuenta creada entre 02/05 y 03/05, por favor registrarse nuevamente. Disculpe los inconvenientes ♥",
                icon="info",
                color_scheme="yellow",
                variant="outline"
            ),
            rx.center(
                rx.vstack(
                    rx.box(
                        rx.heading(rx.cond(LoginState.loginSection,"Inicio de sesión", "Registro de usuario"), size="4", weight="light", width="100%", textAlign="center"),
                        rx.divider(size="4"),
                        width="100%",
                        paddingTop="1rem"
                    ),
                    rx.form(
                        rx.callout(
                            "El usuario y/o contraseña no son correctos. Por favor, intente nuevamente",
                            icon="triangle_alert",
                            color_scheme="red",
                            role="alert",
                            display=rx.cond(LoginState.loginValidation == True, "block", "none")
                        ),
                        rx.cond(
                           LoginState.loginSection,
                            loginComponent(),
                            registerComponent()
                        ),
                        on_submit=FormState.handle_submit,
                        reset_on_submit=True,
                        display="flex",
                        flexDirection="column",
                        alignItems="center",
                        justifyContent="center",
                        width="100%",
                        height="100%"
                    ),
                    width="20rem", 
                    boxShadow="rgba(0, 0, 0, 0.24) 0px 3px 8px",
                    backgroundColor="white",
                    borderRadius="12px", 
                    class_name=[
                        "animate__animated",
                        "animate__fadeInUp",
                        "animate__delay-0.5s"
                    ]               
                ),
                width="100%",
                height="100%",
                background="linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/loginImage.jpg');",
                backgroundReapeat="no-repeat",
                backgroundSize="cover",
                display="flex",
                flexDirection="column",
                justifyContent="center",
                alignItems="center"
            ),
            width="100%",
            height="100%"
        ),
        gap="0",
        height="100vh",
        width="100vw",
        overflow="hidden"
    ) 

def loginComponent() -> rx.Component:
    return rx.vstack(
            rx.flex(
                rx.icon("at-sign", size=18),
                rx.input(
                    placeholder="Correo",
                    name="mail",
                    type="email",
                    value=userAuth.email,
                    on_change=userAuth.set_email,
                    required=True
                ),
                direction="row",
                gap="1",
                align="center",
            ),
            rx.flex(
                rx.icon("rectangle-ellipsis", size=18),
                rx.input(
                    placeholder="Contraseña",
                    name="password",
                    type="password",
                    value=userAuth.passwrd,
                    on_change=userAuth.set_passwrd,
                    required=True
                ),
                direction="row",
                gap="1",
                align="center",
            ),
            rx.button("Iniciar sesión", color_scheme="cyan", on_click=LoginBackend.setLogin()),
            rx.button("Registrarse", color_scheme="plum", on_click=LoginState.setLoginSection()),
            display="flex",
            flexDirection="column",
            alignItems="center",
            justifyContent='center',
            gap="1rem",
            margin="2rem 0"
        )


class validateRegisterPassword(rx.State):
    samePass:bool = True
    errorUpdate = False

    async def validatePass(self,text):
        user = await self.get_state(userData)
        if text == user.passwrd:
            self.samePass = True
        else:
            self.samePass = False
        user.set_confirmPasswrd(text)
    
    def setErrorUpdate(self, update:bool):
        self.errorUpdate = update

class sumbitRegister(rx.State):
    async def updateUser(self):
        user = await self.get_state(userData)
        response = await user.registerUser()
        if response == True:
            return LoginState.setLoginSection()
        else:
            print("es false")
            validateRegisterPassword.errorUpdate = True

def registerComponent() -> rx.Component:
    return rx.vstack(
        rx.callout(
            "Las contraseñas no son las mismas. Intente nuevamente",
            icon="triangle_alert",
            color_scheme="red",
            role="alert",
            display=rx.cond(validateRegisterPassword.samePass == False, "block", "none")
        ),
        rx.callout(
            "Error al intentar registrar el usuario. Intente nuevamente",
            icon="triangle_alert",
            color_scheme="red",
            role="alert",
            display=rx.cond(validateRegisterPassword.errorUpdate, "block", "none")
        ),
        rx.flex(
            rx.icon("user", size=18),
            rx.input(
                placeholder="Nombre de usuario",
                name="username",
                type="text",
                value=userData.username,
                on_change=userData.set_username
            ),
            direction="row",
            gap="1",
            align="center",
        ),
        rx.flex(
            rx.icon("at-sign", size=18),
            rx.input(
                placeholder="Correo",
                name="mail",
                type="email",
                value=userData.mail,
                on_change=userData.set_mail
            ),
            direction="row",
            gap="1",
            align="center",
        ),
        rx.flex(
            rx.icon("rectangle-ellipsis", size=18),
            rx.input(
                placeholder="Contraseña",
                name="password",
                type="password",
                value=userData.passwrd,
                on_change=userData.set_passwrd
            ),
            direction="row",
            gap="1",
            align="center",
        ),
        rx.flex(
            rx.icon("rectangle-ellipsis", size=18),
            rx.input(
                placeholder="Repetir contraseña",
                name="password",
                type="password",
                value=userData.confirmPasswrd,
                on_change=validateRegisterPassword.validatePass

            ),
            direction="row",
            gap="1",
            align="center",
        ),
        rx.button("Registro", color_scheme="plum", disabled=rx.cond(validateRegisterPassword.samePass, False, True), on_click=sumbitRegister.updateUser),
        rx.button("Inicio de sesión", color_scheme="plum", on_click=LoginState.setLoginSection()),
        display="flex",
        flexDirection="column",
        alignItems="center",
        justifyContent='center',
        gap="1rem",
        margin="2rem 0"
    )          