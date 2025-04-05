from pydantic import BaseModel
from typing import Optional, List
from model.study import Study


class StudySchema(BaseModel):
    """ Define como um novo study a ser inserido deve ser representado
    """
    title: str = "NodeJS"
    description: str = "Estudar NodeJS" 
    content: str = "https://nodejs.org/docs/latest/api/" 
    priority: str = "high"
    schedule: str = 'Cronograma'
    category_id: int = None

class StudyBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do study.
    """
    id: int = 1

class StudyBuscaSchemaByFilters(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no status do study e tambem na ordenação, ambas são opcionais.
    """
    status: str = None
    sort: str = None
    category: str = None


class ListagemStudiesSchema(BaseModel):
    """ Define como uma listagem de studies será retornada.
    """
    studies:List[StudySchema]

def apresenta_studies(studies):
    """ Retorna uma representação do studies seguindo o schema definido em
        StudyViewSchema.
    """
    def study_to_dict(study):
        return {
            "id": study.id,
            "title": study.title,
            "description": study.description,
            "content": study.content,
            "status": study.status,
            "priority": study.priority,
            "schedule": study.schedule,
            "category_id": study.category_id,
            "category_name": study.category.name if study.category else None
        }

    return {"studies": [study_to_dict(study) for study in studies]}


class StudyViewSchema(BaseModel):
    """ Define como um study será retornado: study.
    """
    id: int = 1
    title: str = "Estudar Nodejs"
    description: str = "Descrição Nodejs"
    content: str = "Link PDF Nodejs"
    priority: str = "high"
    schedule: str = "Cronograma"
    status: str = "completed"
    category_id: int = 1

class StudyViewSchemaCompleted(BaseModel):
    """ Define mensagem quando o status for atualizado para completado.
    """
    message: str = "Study completado"

class StudyViewSchemaUncompleted(BaseModel):
    """ Define mensagem quando o status for atualizado para não completado.
    """
    message: str = "Study Uncompleted"



class StudyDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    title: str

def apresenta_study(study: Study):
    """ Retorna uma representação do study seguindo o schema definido em
        StudyViewSchema.
    """
    return {
        "id": study.id,
        "title": study.title,
        "description": study.description,
        "content": study.content,
        "status": study.status,
        "priority": study.priority,
        "schedule": study.schedule,
        "category_id": study.category_id
    }