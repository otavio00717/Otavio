import tkinter as tk
from tkinter import messagebox
import pickle

class Personagem:

    def __init__(self, personagem, iniciativa, hp):
        self.personagem = personagem
        self.iniciativa = iniciativa
        self.hp = hp

    def __str__(self):
        return f"{self.personagem}"

    def damage(self, dano):
        self.hp -= dano

    def cure(self, cura):
        self.hp += cura

    @classmethod
    def show_list(cls):
        for personagem in cls.personagens:
            print(f"{personagem.personagem}: Iniciativa - {personagem.iniciativa}, HP - {personagem.hp}")

    @classmethod
    def show_general_list(cls):
        print("Lista Geral de Personagens:")
        for personagem in cls.personagens:
            print(f"{personagem.personagem}")


#janela principal
main = tk.Tk()
main.configure(bg="#444654")


#variaveis e listas
personagens = []
name_entry_var = tk.StringVar()
iniciativa_entry_var = tk.IntVar()
hp_entry_var = tk.IntVar()
item_selecionado = None
index_selecionado = None


#fonts
default_font = ("Proggy", 15)
big_font = ("Proggy", 30)


#frames
frame_entrys = tk.Frame(main,bg="#202123", padx=20, pady= 20)
frame_entry_nome = tk.Frame(frame_entrys,bg="#202123")
frame_entry_iniciativa = tk.Frame(frame_entrys,bg="#202123")
frame_entry_hp = tk.Frame(frame_entrys,bg="#202123")
frame_entrys_on_clicked = tk.Frame(main,bg="#202123", padx=20, pady= 20)

frame_entry_nome_selected = tk.Frame(frame_entrys_on_clicked,bg="#202123")
frame_entry_iniciativa_selected = tk.Frame(frame_entrys_on_clicked, bg="#202123")
frame_entry_hp_selected = tk.Frame(frame_entrys_on_clicked, bg="#202123")

frame_listbox = tk.Frame(main,bg="#202123")
frame_labels_persons = tk.Frame(main,bg="#202123")
frame_buttons = tk.Frame(main,bg="#202123")


#entrys
entry_nome = tk.Entry(frame_entry_nome, textvariable="0", font=default_font, fg="white", bg="black")
entry_iniciativa = tk.Entry(frame_entry_iniciativa, textvariable="1", font=default_font, fg="white", bg="black")
entry_hp = tk.Entry(frame_entry_hp, textvariable="2", font=default_font, fg="white", bg="black")

entry_nome_selected = tk.Entry(frame_entry_nome_selected, textvariable=name_entry_var, font=big_font, fg="white", bg="black")
entry_iniciativa_selected = tk.Entry(frame_entry_iniciativa_selected, textvariable=iniciativa_entry_var, font=big_font, fg="white", bg="black")
entry_hp_selected = tk.Entry(frame_entry_hp_selected, textvariable=hp_entry_var, font=big_font, fg="white", bg="black")


#labels
label_nome = tk.Label(frame_entry_nome, text="Nome", font=default_font,bg="#202123", fg="#8e8ea0")
label_iniciativa = tk.Label(frame_entry_iniciativa, text="Iniciativa", font=default_font,bg="#202123", fg="#8e8ea0")
label_hp = tk.Label(frame_entry_hp, text="Vida", font=default_font,bg="#202123", fg="#8e8ea0")

label_nome_selected = tk.Label(frame_entry_nome_selected, text="Nome", font=big_font,bg="#202123", fg="#8e8ea0")
label_iniciativa_selected = tk.Label(frame_entry_iniciativa_selected, text="Iniciativa", font=big_font,bg="#202123", fg="#8e8ea0")
label_hp_selected = tk.Label(frame_entry_hp_selected, text="Vida", font=big_font,bg="#202123", fg="#8e8ea0")


#listbox
listbox = tk.Listbox(frame_listbox, height=22, width=32,font=default_font,fg="white",bg="#202123", activestyle="underline",selectbackground="yellow", selectforeground="black")


# funções
def salvar_dados():
    with open('dados_personagens.pkl', 'wb') as file:
        pickle.dump(personagens, file)

def carregar_dados():
    try:
        with open('dados_personagens.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

def delete_item():
    selected = listbox.curselection()
    if selected:
        index = int(selected[0])
        del personagens[index]
        listbox.delete(selected)
        salvar_dados()

def adicionar_lista():
    nome = entry_nome.get()
    iniciativa = entry_iniciativa.get()
    vida = entry_hp.get()
    if not nome or not iniciativa or not vida:
        messagebox.showerror("Erro", "Preencha todos os campos.")
    else:
        try:
            iniciativa = int(iniciativa)
            vida = int(vida)
            personagem = Personagem(nome, iniciativa, vida)
            personagens.append(personagem)
            listbox_update()
            clear_entrys()
            salvar_dados()  # Salva os dados após adicionar um item
        except ValueError:
            messagebox.showerror("Erro", "Iniciativa e Vida devem ser números.")

def listbox_update():
    clear_entrys()
    try:
        personagens.sort(key=lambda personagem: int(personagem.iniciativa), reverse=True)
        listbox.delete(0, tk.END)
        for item in personagens:
            listbox.insert(tk.END, item)
    except:
        messagebox.showerror("Erro", "Iniciativa e Vida devem ser números.")

def clear_entrys():
    entry_nome.delete(0, tk.END)
    entry_iniciativa.delete(0,tk.END)
    entry_hp.delete(0,tk.END)

def clear_entrys_selected():
    entry_nome_selected.delete(0, tk.END)
    entry_iniciativa_selected.delete(0, tk.END)
    entry_hp_selected.delete(0, tk.END)

def on_select(event):
    global item_selecionado, index_selecionado
    # Obter os índices dos itens selecionados
    indices_selecionados = listbox.curselection()
    if indices_selecionados:
        index = int(indices_selecionados[0])
        item_selecionado = personagens[index]
        index_selecionado = index
        mostrar_detalhes(item_selecionado,indices_selecionados)

def mostrar_detalhes(personagem,indice):
    if indice:
        frame_entrys_on_clicked.grid(row=1, column=2, padx=30)
        name_entry_var.set(personagem.personagem)
        iniciativa_entry_var.set(personagem.iniciativa)
        hp_entry_var.set(personagem.hp)

def editar_per():
    global item_selecionado, index_selecionado
    nome = entry_nome_selected.get()
    iniciativa = entry_iniciativa_selected.get()
    hp = entry_hp_selected.get()
    if item_selecionado is not None and index_selecionado is not None:
        if not nome or not iniciativa or not hp:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        else:
            try:
                iniciativa = int(iniciativa)
                hp = int(hp)
            except ValueError:
                messagebox.showerror("Erro", "Iniciativa e Vida devem ser números.")
                return
            item_selecionado.personagem = nome
            item_selecionado.iniciativa = iniciativa
            item_selecionado.hp = hp
            personagens[index_selecionado] = item_selecionado
            listbox_update()
            clear_entrys_selected()
    else:
        messagebox.showerror("Erro", "Nenhum item selecionado para editar.")


#buttons
button_add_pers = tk.Button(frame_listbox, text="Adicionar", command= adicionar_lista, font=default_font, relief="flat", bg= "#202123",activebackground="#444654", fg= "white")
button_delete_per = tk.Button(frame_listbox, text="deletar", command= delete_item, font=default_font, relief="flat", bg= "#202123",activebackground="#444654", fg= "white")
button_edit_per = tk.Button(frame_entrys_on_clicked, text="editar", command= editar_per, font=default_font, relief="flat", bg= "#202123",activebackground="#444654", fg= "white")


#posicionamento
frame_entrys.grid(row = 0,column = 0, pady=20,padx = 20)

frame_entry_nome.pack(pady= 10)
label_nome.pack()
entry_nome.pack()

frame_entry_iniciativa.pack(pady=10)
label_iniciativa.pack()
entry_iniciativa.pack()

frame_entry_hp.pack(pady=10)
label_hp.pack()
entry_hp.pack()

frame_listbox.grid(row=1,column=0,padx = 20)
button_add_pers.pack(pady = 8)
listbox.pack()
button_delete_per.pack()

frame_entry_nome_selected.pack(pady=10)
label_nome_selected.pack()
entry_nome_selected.pack()

frame_entry_iniciativa_selected.pack(pady=10)
label_iniciativa_selected.pack()
entry_iniciativa_selected.pack()

frame_entry_hp_selected.pack(pady=10)
label_hp_selected.pack()
entry_hp_selected.pack()

button_edit_per.pack()

'''
frame_entrys.place(x=105,y=20)

frame_entry_nome.pack(pady= 10)
label_nome.pack()
entry_nome.pack()

frame_entry_iniciativa.pack(pady=10)
label_iniciativa.pack()
entry_iniciativa.pack()

frame_entry_hp.pack(pady=10)
label_hp.pack()
entry_hp.pack()


frame_listbox.place(x=60, y=300)
button_add_pers.pack(pady = 8)
listbox.pack()
button_delete_per.pack()
'''

#codigo
personagens = carregar_dados()  # Carrega os dados ao iniciar o programa
listbox_update()
listbox.bind("<<ListboxSelect>>", on_select)


#executar a janela
main.mainloop()