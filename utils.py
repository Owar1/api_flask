from models import Pessoas, Usuarios


def insere_pessoas():
    pessoa = Pessoas(nome='Camille', idade=19)
    print(pessoa)
    pessoa.save()

def consulta_pessoas():
    pessoas = Pessoas.query.all()
    print(pessoas)


def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Janna').first()
    pessoa.nome = 'Arhi'
    pessoa.save()

def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='caua').first()
    pessoa.delete()


def insere_usuario(login, senha):
    usuario = Usuarios(login=login, senha=senha)
    usuario.save()

def consulta_ususarios():
    usuarios = Usuarios.query.all()
    print(usuarios)


if __name__ == '__main__':
    insere_usuario('darius', '1234')
    insere_usuario('camille', '5678')
    consulta_ususarios()
    #insere_pessoas()
    #consulta_pessoas()
    #altera_pessoa()
    #consulta_pessoas()
