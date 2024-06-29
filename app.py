import enum
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from model import Session, Study
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
study_tag = Tag(name="Study", description="Adição, visualização e remoção de study à base")


class PriorityEnum(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/study', tags=[study_tag],
          responses={"200": StudyViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_study(body: StudySchema):
    """Adiciona um novo Study à base de dados

    Retorna uma representação dos studies.
    """
    try:
        if not body:
            error_msg = "Não foi possível salvar novo item :/"
            return {"message": error_msg}, 400
        
        # Validando prioridade
        if body.priority not in PriorityEnum.__members__:
            error_msg = f"Prioridade inválida: {body.priority}. Deve ser uma das seguintes: high, medium, low."
            return {"message": error_msg}, 400
        study = Study(
            title=body.title,
            description=body.description,
            content=body.content,
            priority=body.priority)
        logger.debug(f"Adicionando study de titulo: '{study.title}'")
        # criando conexão com a base
        session = Session()
        # adicionando study
        session.add(study)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado study de title: '{study.title}'")
        return apresenta_study(study), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar study '{study.title}', {error_msg}")
        return {"mesage": error_msg}, 400
    

@app.put('/study/completed', tags=[study_tag],
          responses={"200": StudyViewSchemaCompleted, "409": ErrorSchema, "400": ErrorSchema})
def completed_study(query: StudyBuscaSchema):
    """Atualiza o status do Study à base de dados

    Retorna uma representação dos studies.
    """
    try:
        study_id = query.id
        logger.debug(f"Completa study de id: '{study_id}'")
        # criando conexão com a base
        session = Session()
        # Atualizando o status do estudo
        updated_rows = session.query(Study).filter(Study.id == study_id).update({'status': "completed"})
        
        if updated_rows == 0:
            # Se nenhum estudo foi atualizado, retorna 404
            error_msg = "Study não encontrado na base :/"
            logger.warning(f"Erro ao buscar study '{study_id}', {error_msg}")
            return {"message": error_msg}, 404
        session.commit()
        logger.debug(f"Completa study de id: '{query.id}'")
        sucess_msg = "Study completado"
        return {"mesage": sucess_msg}, 200
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível completar study :/"
        logger.warning(f"Erro ao atualizar para completed o study '{query.id}', {error_msg}")
        return {"mesage": error_msg}, 400
    
@app.put('/study/uncompleted', tags=[study_tag],
          responses={"200": StudyViewSchemaCompleted, "409": ErrorSchema, "400": ErrorSchema})
def uncompleted_study(query: StudyBuscaSchema):
    """Atualiza o status do Study à base de dados

    Retorna uma representação dos studies.
    """
    study_id = query.id
    logger.debug(f"Completa study de id: '{study_id}'")
    try:
        # criando conexão com a base
        session = Session()
        # Atualizando o status do estudo
        updated_rows = session.query(Study).filter(Study.id == study_id).update({'status': "uncompleted"})
        
        if updated_rows == 0:
            # Se nenhum estudo foi atualizado, retorna 404
            error_msg = "Study não encontrado na base :/"
            logger.warning(f"Erro ao buscar study '{study_id}', {error_msg}")
            return {"message": error_msg}, 404
        session.commit()
        logger.debug(f"Completa study de id: '{query.id}'")
        sucess_msg = "Study atualizado para não completado"
        return {"mesage": sucess_msg}, 200
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível completar study :/"
        logger.warning(f"Erro ao atualizar para uncompleted o study '{query.id}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/studies', tags=[study_tag],
         responses={"200": ListagemStudiesSchema, "404": ErrorSchema})
def get_studies(query: StudyBuscaSchemaByFilters ):
    """Faz a busca por todos os Studies cadastrados

    Retorna uma representação da listagem de studies.
    """
    try:
        logger.debug(f"Coletando studies ")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        print(query.status)
        if not query.status:
            studies = session.query(Study).all()
        else:
            studies = session.query(Study).filter(Study.status == query.status).all()
        print(studies)

        if not studies:
            # se não há studies cadastrados
            return {"studies": []}, 200
        else:
            logger.debug(f"%d rodutos econtrados" % len(studies))
            # retorna a representação de study
            return apresenta_studies(studies), 200
    except Exception as e:
        # se o study não foi encontrado
        error_msg = "Erro ao tentar buscar a lista de studies"
        logger.warning(f"Erro ao buscar a lista de studies, {error_msg}")
        return {"mesage": error_msg}, 404


@app.get('/study', tags=[study_tag],
         responses={"200": StudyViewSchema, "404": ErrorSchema})
def get_study(query: StudyBuscaSchema):
    """Faz a busca por um Study a partir do id do study

    Retorna uma representação dos studies
    """
    try:
        study_id = query.id
        logger.debug(f"Coletando dados sobre study #{study_id}")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        study = session.query(Study).filter(Study.id == study_id).first()

        if not study:
            # se o study não foi encontrado
            error_msg = "Study não encontrado na base :/"
            logger.warning(f"Erro ao buscar study '{study_id}', {error_msg}")
            return {"mesage": error_msg}, 404
        else:
            logger.debug(f"Study encontrado: '{study.title}'")
            # retorna a representação de study
            return apresenta_study(study), 200
    except Exception as e:
        # se o study não foi encontrado
        error_msg = "Erro ao tentar buscar o study"
        logger.warning(f"Erro ao buscar study #'{study_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.delete('/study', tags=[study_tag],
            responses={"200": StudyDelSchema, "404": ErrorSchema})
def del_study(query: StudyBuscaSchema):
    """Deleta um Study a partir do id de study informado

    Retorna uma mensagem de confirmação da remoção.
    """
    try:
        study_id = query.id
        print(study_id)
        logger.debug(f"Deletando dados sobre study #{study_id}")
        # criando conexão com a base
        session = Session()
        study = session.query(Study).filter(Study.id == study_id).first()
        if not study:
            error_msg = "Study não encontrado na base :/"
            logger.warning(f"Erro ao deletar study #{study_id}, {error_msg}")
            return {"message": error_msg}, 404
        
        # Faz a remoção
        session.delete(study)
        session.commit()
        return {"mesage": "Study removido", "id": study_id}, 200

    except Exception as e:
        # se o study não foi encontrado
        error_msg = "Erro ao tentar deletar o study"
        logger.warning(f"Erro ao deletar study #'{study_id}', {error_msg}")
        return {"message": error_msg}, 404