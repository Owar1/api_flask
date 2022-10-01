from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)




@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False

    return Usuarios.query.filter_by(login=login, senha=senha).first()




class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                    "nome": pessoa.nome,
                    "idade": pessoa.idade,
                    "id": pessoa.id
                    }
        except AttributeError:
            response = {"status": "Erro", "msg": "pessoa nao encontrada"}

        return response 


    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        
        pessoa.save()
        response = {
                "nome": pessoa.nome,
                "idade": pessoa.idade,
                "id": pessoa.id
                }

        return response


    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        pessoa.delete()
        msg = f'Pessoa {pessoa.nome} excluida com sucesso!'

        return {"status": "sucesso", "msg": msg}
        



class ListaPessoa(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id':p.id, "nome":p.nome, "idade":p.idade} for p in pessoas]

        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
                "id": pessoa.id,
                "nome": pessoa.nome,
                "idade": pessoa.idade
                }

        return response



class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id':p.id, 'pessoa':p.pessoa.nome, 'atividade':p.nome} for p in atividades]

        return response


    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['atividade'], pessoa=pessoa)
        atividade.save()
        response = {
                "id": atividade.id,
                "pessoa": atividade.pessoa.nome,
                "atividade": atividade.nome
                }

        return response


class CriarUsuario(Resource):
    def get(self):
        ususarios = Usuarios.query.all()
        response = [{"login":u.login, "senha":u.senha} for u in ususarios]

        return response

    def post(self):
        dados = request.json
        ususario = Usuarios(login=dados['login'], senha=dados['senha'])
        ususario.save()
        response = {
                "login": ususario.login,
                "senha": ususario.senha
                }

        return response


api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(ListaPessoa, '/pessoa')
api.add_resource(ListaAtividades, '/atividade')
api.add_resource(CriarUsuario, '/usuario')


if __name__ == '__main__':
    app.run(debug=True)
