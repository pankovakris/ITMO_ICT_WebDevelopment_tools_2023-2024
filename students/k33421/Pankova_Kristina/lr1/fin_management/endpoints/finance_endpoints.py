from fastapi import APIRouter, HTTPException, Security, security, Depends

from authentification.auth import AuthHandler

from sqlalchemy.exc import NoResultFound
from models.models import *
from models.user_models import *
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import joinedload
from sqlmodel import select
from endpoints.user_endpoints import user_router

from db.connection import *
from typing_extensions import TypedDict
app = FastAPI()
finance_router = APIRouter()
app.include_router(finance_router)


@finance_router.get("/budgets")
def get_budgets(session: Session = Depends(get_session)):
    budgets = session.exec(select(Budget)).all()
    return budgets

@finance_router.get("/budget/{budget_id}")
def get_budget(budget_id: int, session: Session = Depends(get_session)):
    try:
        budget = session.get(Budget, budget_id)
        return budget
    except NoResultFound:
        return {"message": "Budget not found"}

@finance_router.post("/budget")
def create_budget(budget: Budget, session: Session = Depends(get_session)):
    session.add(budget)
    session.commit()
    session.refresh(budget)
    return budget


@finance_router.get("/budget_categories")
def get_budget_categories(session: Session = Depends(get_session)):
    budget_categories = session.exec(select(BudgetCategory)).all()
    return budget_categories

@finance_router.get("/budget_category/{budget_category_id}")
def get_budget_category(budget_category_id: int, session: Session = Depends(get_session)):
    try:
        budget_category = session.get(BudgetCategory, budget_category_id)
        return budget_category
    except NoResultFound:
        return {"message": "Budget Category not found"}

@finance_router.post("/budget_category")
def create_budget_category(budget_category: BudgetCategory, session: Session = Depends(get_session)):
    session.add(budget_category)
    session.commit()
    session.refresh(budget_category)
    return budget_category


@finance_router.get("/categories")
def get_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Category)).all()
    return categories

@finance_router.get("/category/{category_id}")
def get_category(category_id: int, session: Session = Depends(get_session)):
    try:
        category = session.get(Category, category_id)
        return category
    except NoResultFound:
        return {"message": "Category not found"}

@finance_router.post("/category")
def create_category(category: Category, session: Session = Depends(get_session)):
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@finance_router.get("/transactions")
def get_transactions(session: Session = Depends(get_session)):
    transactions = session.exec(select(FinancialTransaction)).all()
    return transactions

@finance_router.get("/transaction/{transaction_id}")
def get_transaction(transaction_id: int, session: Session = Depends(get_session)):
    try:
        transaction = session.get(FinancialTransaction, transaction_id)
        return transaction
    except NoResultFound:
        return {"message": "Transaction not found"}

@finance_router.post("/transaction")
def create_transaction(transaction: FinancialTransaction, session: Session = Depends(get_session)):
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


# Goal API endpoints
@finance_router.get("/goals")
def get_goals(session: Session = Depends(get_session)):
    goals = session.exec(select(Goal)).all()
    return goals

@finance_router.get("/goal/{goal_id}")
def get_goal(goal_id: int, session: Session = Depends(get_session)):
    try:
        goal = session.get(Goal, goal_id)
        return goal
    except NoResultFound:
        return {"message": "Goal not found"}

@finance_router.post("/goal")
def create_goal(goal: Goal, session: Session = Depends(get_session)):
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal
