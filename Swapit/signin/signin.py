from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from sqlqueries import QueriesSQLite

Builder.load_file('signin/signin.kv')

class SigninWindow(BoxLayout):
    def __init__(self, nuevo_usuario_callback, **kwargs):
        super().__init__(*kwargs)
        self.nuevo_usuario = nuevo_usuario_callback
        
    def verificar_usuario(self, username, password):
        connection = QueriesSQLite.create_connection("pdvDB.sqlite")
        users = QueriesSQLite.execute_read_query(connection, "SELECT * from usuarios")
        if username == '' or password == '':
            self.ids.signin_notificacion.text = 'Falta nombre de usuario y/o contraseña'
        else:
            usuario = {}
            for user in users:
                if user[0] == username:
                    usuario['nombre'] = user[1]
                    usuario['username'] = user[0]
                    usuario['password'] = user[2]
                    usuario['tipo'] = user[3]
                    break
            if usuario:
                if usuario['password'] == password:
                    self.ids.username.text = ''
                    self.ids.password.text = ''
                    self.ids.signin_notificacion.text = ''
                    if usuario['tipo'] == 'trabajador':
                        self.parent.parent.current = 'scrn_ventas'
                    else:
                        self.parent.parent.current = 'scrn_admin'
                    self.nuevo_usuario(usuario)
                else:
                    self.ids.signin_notificacion.text = 'Usuario o contraseña incorrecta'
            else:
                self.ids.signin_notificacion.text = 'Usuario o Contraseña incorrecta'
                
class SigninApp(App):
    def build(self):
        return SigninWindow()
    
if __name__=="__main__":
    SigninApp().run()