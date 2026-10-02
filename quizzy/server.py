#!/usr/bin/env python3

from pathlib import Path
from typing import Annotated, Self

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import JSON, Column, ForeignKey, Table, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


# ORM model: classes mapped to database tables

class Base(DeclarativeBase):
    pass


quiz_questions = Table(
    'quiz_questions', Base.metadata,
    Column('quiz_id', ForeignKey('quizzes.id'), primary_key=True),
    Column('question_id', ForeignKey('questions.id'), primary_key=True),
)


class Question(Base):
    __tablename__ = 'questions'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    options: Mapped[list[str]] = mapped_column(JSON)
    correct_option: Mapped[int]


class Quiz(Base):
    __tablename__ = 'quizzes'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    questions: Mapped[list[Question]] = relationship(
        secondary=quiz_questions, order_by=Question.id)


# Schemas: representations that the API receives and returns.
# FastAPI builds the returned ones from the ORM objects.

class QuestionData(BaseModel):
    text: str = Field(min_length=1)
    options: list[str] = Field(min_length=2, max_length=6)
    correct_option: int = Field(ge=0)

    @model_validator(mode='after')
    def check_correct_option(self) -> Self:
        if self.correct_option >= len(self.options):
            raise ValueError('correct_option must be the index of one of the options')
        return self


class QuestionWithSolution(QuestionData):
    id: int


class QuestionWithoutSolution(BaseModel):
    id: int
    text: str
    options: list[str]


class QuizData(BaseModel):
    title: str = Field(min_length=1)
    question_ids: list[int] = Field(min_length=1)


class QuizSummary(BaseModel):
    id: int
    title: str


class QuizWithQuestions(QuizSummary):
    questions: list[QuestionWithoutSolution]


Answers = dict[int, int]  # question id -> index of the chosen option


class Grade(BaseModel):
    score: int  # one point for each correct answer
    total: int


# API

engine = create_engine('sqlite:///quizzy.db')
Base.metadata.create_all(engine)
app = FastAPI(title='Quizzy')


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_or_404(session, model, key):
    instance = session.get(model, key)
    if instance is None:
        raise HTTPException(404, f'{model.__name__} {key} not found')
    return instance


def get_questions_or_422(session, question_ids):
    questions = session.scalars(
        select(Question).where(Question.id.in_(question_ids))).all()
    unknown_ids = set(question_ids) - {question.id for question in questions}
    if unknown_ids:
        raise HTTPException(422, f'unknown questions: {sorted(unknown_ids)}')
    return questions


@app.post('/questions', status_code=201)
def create_question(data: QuestionData, response: Response,
                    session: SessionDep) -> QuestionWithSolution:
    question = Question(**data.model_dump())
    session.add(question)
    session.commit()
    response.headers['Location'] = f'/questions/{question.id}'
    return question


@app.get('/questions')
def list_questions(session: SessionDep) -> list[QuestionWithSolution]:
    return session.scalars(select(Question).order_by(Question.id)).all()


@app.get('/questions/{question_id}')
def get_question(question_id: int, session: SessionDep) -> QuestionWithSolution:
    return get_or_404(session, Question, question_id)


@app.put('/questions/{question_id}')
def replace_question(question_id: int, data: QuestionData,
                     session: SessionDep) -> QuestionWithSolution:
    question = get_or_404(session, Question, question_id)
    question.text = data.text
    question.options = data.options
    question.correct_option = data.correct_option
    session.commit()
    return question


@app.post('/quizzes', status_code=201)
def create_quiz(data: QuizData, response: Response,
                session: SessionDep) -> QuizWithQuestions:
    quiz = Quiz(title=data.title,
                questions=get_questions_or_422(session, data.question_ids))
    session.add(quiz)
    session.commit()
    response.headers['Location'] = f'/quizzes/{quiz.id}'
    return quiz


@app.get('/quizzes')
def list_quizzes(session: SessionDep) -> list[QuizSummary]:
    return session.scalars(select(Quiz).order_by(Quiz.id)).all()


@app.get('/quizzes/{quiz_id}')
def get_quiz(quiz_id: int, session: SessionDep) -> QuizWithQuestions:
    return get_or_404(session, Quiz, quiz_id)


@app.put('/quizzes/{quiz_id}')
def replace_quiz(quiz_id: int, data: QuizData,
                 session: SessionDep) -> QuizWithQuestions:
    quiz = get_or_404(session, Quiz, quiz_id)
    quiz.title = data.title
    quiz.questions = get_questions_or_422(session, data.question_ids)
    session.commit()
    return quiz


@app.post('/quizzes/{quiz_id}/grade')
def grade_quiz(quiz_id: int, answers: Answers, session: SessionDep) -> Grade:
    quiz = get_or_404(session, Quiz, quiz_id)
    score = sum(answers.get(question.id) == question.correct_option
                for question in quiz.questions)
    return Grade(score=score, total=len(quiz.questions))


@app.get('/', include_in_schema=False)
def web_client():
    return FileResponse(Path(__file__).with_name('index.html'))


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
