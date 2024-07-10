from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from mysql.connector import connection, connect

# Usar o Tkinter
# Ter um sistema de autenticação e registo de utilizadores (utilizador/palavra-chave)​
# Usar uma base de dados para os utilizadores e palavras-chave​
# Usar uma base de dados para gestão das informações dos ​alunos
# Ter controlo da informação a ser visualizada (p.e. mostrar alunos de forma ordenada (id, médias, nome ou por turmas), destacar melhor aluno, destacar que tem média insuficiente, etc.)
# Mostrar apenas os alunos da turma da pessoa autenticada (exceto administrador do sistema que mostra tudo)
# Opção:  adicionar, eliminar e alterar informação dos alunos

root = Tk()

####################################################################################### 
#                                    CLASSE BACKEND                                   #
#######################################################################################
class Funcoes():


    # Conectar bd
    def conecta_bd(self):
       
        self.conexao = connection.MySQLConnection(user='root',password='', host='localhost', database='python_bd')
        self.cursor = self.conexao.cursor()

    # Desconectar bd
    def desconecta_bd(self):
        self.conexao.close()

    def variaveis(self):
        self.usuario = self.entry_user.get()
        self.senha = self.entry_senha.get()
    
    # Função que solicita login(adim ou aluno) e mostra dados dos alunos na treeview
    def select_lista_login(self):

        self.variaveis()
        self.lista_cli.delete(*self.lista_cli.get_children())
        self.conecta_bd()
    
        self.cursor.execute(""" SELECT * FROM login Where senha = %s AND usuario = %s AND permissao = 1""",
                                (self.senha, self.usuario))
        adim = self.cursor.fetchall()

        self.cursor.execute(""" SELECT * FROM login Where senha = %s AND usuario = %s AND permissao IS NULL """,
                                (self.senha, self.usuario))
        aluno = self.cursor.fetchall()
        
        if(adim):
            
            self.cursor.execute(""" SELECT pi04.nr_formando, NomeAluno, NomeCurso, mediafinalcurso FROM pi04, login  
                                WHERE pi04.nr_formando = login.nr_formando """)
            lista = self.cursor.fetchall()
            for i in lista:
                self.lista_cli.insert("", END, values =i)

        elif(aluno):
            
            self.cursor.execute(""" SELECT pi04.nr_formando, NomeAluno, NomeCurso, mediafinalcurso FROM pi04, login  
                                WHERE pi04.nr_formando = login.nr_formando AND senha = %s  AND usuario = %s""",
                                (self.senha, self.usuario))
           
            lista = self.cursor.fetchall()

        # adicionando os dados para mostrar na treeview(lista)
            for i in lista:
                self.lista_cli.insert("", END, values =i)
        else:
            messagebox.showerror("ERROR", "LOGIN OU SENHA INVÁLIDOS")

        self.conexao.commit()
        #self.delete_entry()
        self.desconecta_bd()

    # Função para novo registro no bd com criação de uma nova janela   
    def novo_user(self):

        if (self.login_adim() != "1"):
    
            messagebox.showerror("Erro ", "Login administrador necessário")
            return
        self.root1 = Tk()
        self.root1.title("Novo Registros Alunos")
        self.root1.configure(background= "#FFE4C4")
        self.root1.geometry("700x500")#tamanho tela ao abrir
        self.root1.resizable(True,True)#tornar a tela responsiva,
        self.root1.maxsize(width=900, height=700)#max que pode aumentar a tela
        self.root1.minsize(width=500, height=300)# min que pode diminuir

        self.label_user1 = Label(self.root1, text="Novo Login", bg="#FFE4C4", fg="#800000")
        self.label_user1.place(relx=0.4,rely=0.2)
        self.entry_user1 = Entry(self.root1, bg= "#F2F2F2")
        self.entry_user1.place(relx=0.35, rely=0.25, relwidth=0.2)

        # Criação da label e entry da nova senha
        self.label_senha1 = Label(self.root1, text="Nova Senha", bg="#FFE4C4", fg="#800000")
        self.label_senha1.place(relx=0.4,rely=0.3)
        self.entry_senha1 = Entry(self.root1, show= "*", bg= "#F2F2F2")
        self.entry_senha1.place(relx=0.35, rely=0.35, relwidth=0.2)

        # Criação da label e entry do nome formando
        self.label_nome = Label(self.root1, text="Nome", bg="#FFE4C4", fg="#800000")
        self.label_nome.place(relx=0.42,rely=0.4)
        self.entry_nome = Entry(self.root1, bg= "#F2F2F2")
        self.entry_nome.place(relx=0.35, rely=0.45, relwidth=0.2)

        # Criação da label e entry do curso
        self.label_curso = Label(self.root1, text="Curso", bg="#FFE4C4", fg="#800000")
        self.label_curso.place(relx=0.42,rely=0.5)
        self.entry_curso = Entry(self.root1, bg= "#F2F2F2")
        self.entry_curso.place(relx=0.35, rely=0.55, relwidth=0.2)

        # Criação da label e entry do MediaFinal
        self.label_media = Label(self.root1, text="Média Final", bg="#FFE4C4", fg="#800000")
        self.label_media.place(relx=0.4, rely=0.6)
        self.entry_media = Entry(self.root1, bg= "#F2F2F2")
        self.entry_media.place(relx=0.35, rely=0.65, relwidth=0.2)

        # Botão Salvar
        self.bt_login =Button(self.root1, text="Salvar", command=self.inserir_novo_user, bd=2, bg="#FFE4C4", fg="#800000", font=("Verdana", 9, "italic"))
        self.bt_login.place(relx=0.4, rely=0.75, relwidth=0.1)

        self.root1.mainloop()
    
    # Função login adiministrador
    def login_adim(self):
        self.conecta_bd()
        self.variaveis()
        self.cursor.execute(""" SELECT permissao FROM login Where senha = %s AND usuario = %s AND permissao = 1 """,
                                (self.senha, self.usuario))
        adim = self.cursor.fetchall()
        n = ''.join(str(num[0]) for num in adim) #extrai string da tuple
        return n

    # Insere os dados do novo user no bd    
    def inserir_novo_user(self):
        
        self.novoUser = self.entry_user1.get()
        self.nova_senha = self.entry_senha1.get()
        self.nome = self.entry_nome.get()
        self.curso = self.entry_curso.get()
        self.media = self.entry_media.get()

        self.conecta_bd()
      
        if not self.novoUser.strip() or not self.nova_senha.strip()  or not self.nome.strip() or not self.curso.strip() or not self.media.strip():
            messagebox.showerror("ERROR", "Todos os campos devem ser preenchidos")

        else:
            self.cursor.execute("""INSERT INTO pi04 ( NomeAluno, NomeCurso, MediaFinalCurso) 
                                VALUES (%s, %s, %s)""",( self.nome, self.curso, self.media))
            
            
            self.cursor.execute(""" SELECT nr_formando from pi04 where NomeAluno = %s and NomeCurso = %s and MediaFinalCurso = %s """
                                ,( self.nome, self.curso, self.media))
            
            nr_aluno = self.cursor.fetchall()

            # operador ternário python
            n = ''.join(str(num[0]) for num in nr_aluno)
        
            self.cursor.execute("""INSERT INTO login (usuario, senha, nr_formando)
                                    VALUES (%s, %s, %s)""",( self.novoUser, self.nova_senha, (n)))
            
            
            messagebox.showinfo("Registro", "Registro efetuado"+ " "+ self.novoUser)
    
            self.conexao.commit()
            self.desconecta_bd()
            self.closeWindow()
            self.select_lista_login() # Atualizar a treeview com o novo user
            #self.delete_entry()

    def delete_entry(self):
        self.entry_user.delete(0,END)
        self.entry_senha.delete(0,END) 
    
    # Função para fechar a janela   
    def closeWindow(self):
        self.root1.destroy()


    # Função deletar aluno do banco de dados
    def apagar_aluno(self):
        selected_item = self.lista_cli.focus()

        if (self.login_adim() != "1"):
    
            messagebox.showerror("Erro ", "Login administrador necessário")
            return
        
        if not selected_item:
            messagebox.showwarning("Erro", "Nenhum aluno selecionado.")
            return
        
        aluno_id = self.lista_cli.item(selected_item, "values")[0]  # Pegar o ID do aluno selecionado

        self.conecta_bd()

        try:
            # Apagar registros na tabela login que tem ligação com o aluno selecionado
            self.cursor.execute("DELETE FROM login WHERE nr_formando = %s", (aluno_id,))
            self.conexao.commit()

            # Apagar o registro na tabela pi04
            self.cursor.execute("DELETE FROM pi04 WHERE nr_formando = %s", (aluno_id,))
            self.conexao.commit()

            messagebox.showinfo("Sucesso", f"Aluno ID {aluno_id} apagado com sucesso.")
            self.select_lista_login()
        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao apagar aluno: {str(ex)}")
        
        self.desconecta_bd()

    # Função alterar dados de um aluno selecionado da treeview
    def alterar_aluno(self):
        selected_item = self.lista_cli.focus()

        if (self.login_adim() != "1"):
    
            messagebox.showerror("Erro ", "Login administrador necessário")
            return
        
        if not selected_item:
            messagebox.showwarning("Erro", "Nenhum aluno selecionado.")
            return
        
        aluno_id = self.lista_cli.item(selected_item, "values")[0] # ID

        self.conecta_bd()
        self.cursor.execute("SELECT NomeAluno, NomeCurso, MediaFinalCurso FROM pi04 WHERE nr_formando = %s", (aluno_id,))
        aluno = self.cursor.fetchone()
        self.desconecta_bd()

        if not aluno:
            messagebox.showwarning("Erro", "Aluno não encontrado.")
            return

        # Criar uma nova janela para editar os dados
        self.root2 = Toplevel()
        self.root2.title("Alterar Dados do Aluno")
        self.root2.configure(background="#FFE4C4")
        self.root2.geometry("400x400")

        self.label_nome = Label(self.root2, text="Nome", bg="#FFE4C4", fg="#800000")
        self.label_nome.place(relx=0.1, rely=0.1)
        self.entry_nome = Entry(self.root2, bg="#F2F2F2")
        self.entry_nome.place(relx=0.1, rely=0.15, relwidth=0.8)
        self.entry_nome.insert(0, aluno[0])

        self.label_curso = Label(self.root2, text="Curso", bg="#FFE4C4", fg="#800000")
        self.label_curso.place(relx=0.1, rely=0.25)
        self.entry_curso = Entry(self.root2, bg="#F2F2F2")
        self.entry_curso.place(relx=0.1, rely=0.3, relwidth=0.8)
        self.entry_curso.insert(0, aluno[1])

        self.label_media = Label(self.root2, text="Média Final", bg="#FFE4C4", fg="#800000")
        self.label_media.place(relx=0.1, rely=0.4)
        self.entry_media = Entry(self.root2, bg="#F2F2F2")
        self.entry_media.place(relx=0.1, rely=0.45, relwidth=0.8)
        self.entry_media.insert(0, aluno[2])

        self.bt_salvar = Button(self.root2, text="Salvar", command=lambda: self.salvar_alteracao(aluno_id), bd=2, bg="#FFE4C4", fg="#800000", font=("Verdana", 9, "italic"))
        self.bt_salvar.place(relx=0.4, rely=0.75, relwidth=0.2)
        
    
    # Função para salvar as alterações
    def salvar_alteracao(self, aluno_id):
        novo_nome = self.entry_nome.get()
        novo_curso = self.entry_curso.get()
        nova_media = self.entry_media.get()

        if not (novo_nome and novo_curso and nova_media):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
            return

        self.conecta_bd()
        try:
            self.cursor.execute("UPDATE pi04 SET NomeAluno = %s, NomeCurso = %s, MediaFinalCurso = %s WHERE nr_formando = %s",
                                (novo_nome, novo_curso, nova_media, aluno_id))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", f"Dados do aluno {novo_nome} alterados com sucesso.")
            
            # Atualizar a Treeview após a alteração
            self.select_lista_login()
            self.root2.destroy()

        except Exception as ex:
            messagebox.showerror("Erro", f"Erro ao alterar dados do aluno: {str(ex)}")
        self.desconecta_bd()
        self.root2.destroy()
        
####################################################################################### 
#                                    CLASSE FRONTEND                                  #
#######################################################################################        
class Aplicacao(Funcoes):

    def __init__(self):
        self.root = root
        self.config_tela()
        self.frames_tela()
        self.widgets_frame1()
        self.list_frame2()

        root.mainloop()

    # Configurações da janela principal
    def config_tela(self):

        self.root.title("Registros Alunos")
        self.root.configure(background= "#FFE4C4")
        self.root.geometry("700x500")#tamanho tela ao abrir
        self.root.resizable(True,True)#tornar a tela responsiva,
        self.root.maxsize(width=900, height=700)#max que pode aumentar a tela
        self.root.minsize(width=500, height=300)# min que pode diminuir
    

    # criando frames(quadros) na tela principal
    def frames_tela(self):

        self.frame1 = Frame(self.root, bd=4, bg="#FFFACD",
                            highlightcolor="#FFEFD5",highlightthickness=4)# tamanho borda, cor fundo, cor borda, altura da borda
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame2 = Frame(self.root, bd=4, bg="#FFFACD",
                            highlightcolor="#FFEFD5",highlightthickness=4)
        self.frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    # Objetos(botões e labels) da Frame1
    def widgets_frame1(self):
    
        # Criação da label e entry do usuário
        self.label_user = Label(self.frame1, text="Login", bg="#FFFACD", fg="#800000")
        self.label_user.place(relx=0.05,rely=0.02)
        self.entry_user = Entry(self.frame1)
        self.entry_user.place(relx=0.05,rely=0.12, relwidth=0.2)

        # Criação da label e entry da senha
        self.label_senha = Label(self.frame1, text="Senha", bg="#FFFACD", fg="#800000")
        self.label_senha.place(relx=0.05,rely=0.4)
        self.entry_senha = Entry(self.frame1, show= "*")
        self.entry_senha.place(relx=0.05,rely=0.51, relwidth=0.2)

        # Botão Login
        self.bt_login =Button(self.frame1, text="login", command=self.select_lista_login, bd=2, bg="#FFE4C4", fg="#800000", font=("Verdana", 9, "italic"))
        self.bt_login.place(relx=0.1,rely=0.71, relwidth=0.1)

        # Botão Novo registro alunos
        self.bt_login =Button(self.frame1, text="Novo",  command= lambda:self.novo_user(), bd=2, bg="#FFE4C4", fg="#800000", font=("Verdana", 9, "italic"))
        self.bt_login.place(relx=0.70,rely=0.02, relwidth=0.1)

        # Botão Alterar
        self.bt_login =Button(self.frame1, text="Alterar", command=self.alterar_aluno, bd=2, bg="#FFE4C4", fg="#800000", font=("Verdana", 9, "italic"))
        self.bt_login.place (relx=0.80,rely=0.02, relwidth=0.1)

        # Botão Apagar
        self.bt_login =Button(self.frame1, text="Apagar", command=self.apagar_aluno, bd=2, bg="#FFE4C4", fg="#800000", font=("Verdana", 9, "italic"))
        self.bt_login.place (relx=0.90,rely=0.02, relwidth=0.1)
        
    
    # Objetos(lista) da Frame2
    def list_frame2(self):

        self.lista_cli = ttk.Treeview(self.frame2, height=3, columns=("col1", "col2", "col3", "col4"))
        self.lista_cli.heading("#0", text="")
        self.lista_cli.heading("#1", text="nr_formando")
        self.lista_cli.heading("#2", text="NomeAluno")
        self.lista_cli.heading("#3", text="NomeCurso")
        self.lista_cli.heading("#4", text="MediaFinalCurso")

        self.lista_cli.column("#0", width=1) #na lista a proporção é de 500 =100% da tela da lista
        self.lista_cli.column("#1", width=60) #10% da tela
        self.lista_cli.column("#2", width=125) #corresponde a 40% da tela da lista
        self.lista_cli.column("#3", width=125) #25% da tela...
        self.lista_cli.column("#4", width=125) #divide o valor por 5.

        self.lista_cli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)




Aplicacao()