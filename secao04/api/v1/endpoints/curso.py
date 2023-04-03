from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import Path

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CursoModel
from schemas.curso_schema import CursoSchema
from core.deps import get_session


router = APIRouter()

#POST curso
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CursoSchema)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo,
                            aulas=curso.aulas, horas=curso.horas)

    db.add(novo_curso)
    await db.commit()

    return novo_curso


#GET cursos
@router.get('/', response_model=List[CursoSchema])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()

        return cursos


#GET curso
@router.get('/{id}', response_model=List[CursoSchema])
async def get_curso(id: int = Path(title="ID do curso desejado", description="Deve ser maior que 0",gt=0), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).where(CursoModel.id == id)
        result = await session.execute(query)
        curso: List[CursoModel] = result.scalars().one_or_none()

        if curso:
            return curso
        else:
            raise HTTPException(detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND)



#PUT curso
@router.put('/{id}', response_model=CursoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_curso(curso: CursoSchema, id: int = Path(title="ID do curso que deseja atualizar", description="Deve ser maior que 0",gt=0), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).where(CursoModel.id == id)
        result = await session.execute(query)
        curso_up: List[CursoModel] = result.scalars().one_or_none()

        if curso_up:
            curso_up.titulo = curso.titulo
            curso_up.horas = curso.horas
            curso_up.aulas = curso.aulas

            await session.commit()

            return curso_up
        else:
            raise HTTPException(detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND)



#DELETE curso
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso( id: int = Path(title="ID do curso que deseja atualizar", description="Deve ser maior que 0",gt=0), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).where(CursoModel.id == id)
        result = await session.execute(query)
        curso_del: List[CursoModel] = result.scalars().one_or_none()

        if curso_del:
            await session.delete(curso_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND)
