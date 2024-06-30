from pydantic import BaseModel
from typing import Optional, List
from model.category import Category


class CategorySchema(BaseModel):
    """ Define como um novo category a ser inserido deve ser representado
    """
    name: str = "Backend"

class CategoryBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do category.
    """
    id: int = 1

class ListagemCategoriesSchema(BaseModel):
    """ Define como uma listagem de categories será retornada.
    """
    categories:List[CategorySchema]


def apresenta_categories(categories: List[Category]):
    """ Retorna uma representação do categories seguindo o schema definido em
        CategoryViewSchema.
    """
    result = []
    for category in categories:
        result.append({
            "id": category.id,
            "name": category.name
        })

    return {"categories": result}


class CategoryViewSchema(BaseModel):
    """ Define como um category será retornado: category.
    """
    id: int = 1
    name: str = "Backend"

class CategoryDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    name: str

def apresenta_category(category: Category):
    """ Retorna uma representação do category seguindo o schema definido em
       CategoryViewSchema.
    """
    return {
        "id": category.id,
        "name": category.name
    }