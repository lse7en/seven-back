# routers/game.py

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from src.deps import CurrentUserId, DBSession
from src.repositories.user_repository import UserRepository
from src.repositories.game_repository import RpsGameRepository
from src.models.game import RpsGame, RpsGameStatus, Choice
from src.schemas.game_schemas import RpsGameSchema, ChoiceSchema, RpsGameResultSchema
import random

router = APIRouter(prefix="/game/rps", tags=["game"])


def determine_winner(choice1: Choice, choice2: Choice):
    # Returns 1 if player1 wins, 2 if player2 wins, 0 if tie
    rules = {
        Choice.ROCK: Choice.SCISSORS,
        Choice.PAPER: Choice.ROCK,
        Choice.SCISSORS: Choice.PAPER,
    }
    if choice1 == choice2:
        return 0
    elif rules[choice1] == choice2:
        return 1
    else:
        return 2


@router.post("/start", response_model=RpsGameSchema)
async def start_game(
    user_id: CurrentUserId,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    game_repository: Annotated[RpsGameRepository, Depends()],
):
    async with session.begin():
        activate_game = await game_repository.get_active_game_for_user(user_id)
        if activate_game:
            return activate_game

        user = await user_repository.get_user_for_update(user_id)

        if user.points < 200:
            raise HTTPException(status_code=400, detail="Not enough points to start a game.")


        waiting_game = await game_repository.get_waiting_game()

        if waiting_game:
            waiting_game.player2_id = user_id
            waiting_game.status = RpsGameStatus.WAITING_FOR_CHOICES
            waiting_game.started_at = datetime.utcnow()
            await game_repository.update_game(waiting_game)
            return waiting_game
        else:
            new_game = RpsGame(player1_id=user_id)
            await game_repository.add_game(new_game)
            return new_game


@router.get("/status", response_model=RpsGameSchema)
async def game_status(
    user_id: CurrentUserId,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    game_repository: Annotated[RpsGameRepository, Depends()],
):
    async with session.begin():
        game = await game_repository.get_active_game_for_user(user_id)

        if not game:
            raise HTTPException(status_code=404, detail="No active game found.")

        if game.status == RpsGameStatus.WAITING_FOR_PLAYER and datetime.utcnow() >= game.created_at + timedelta(seconds=10):
            bot_user = await user_repository.get_random_bot()
            game.player2_id = bot_user.id
            game.status = RpsGameStatus.WAITING_FOR_CHOICES
            game.started_at = datetime.utcnow()

            game.player2_choice = random.choice(list(Choice))

            await game_repository.update_game(game)

        return game


@router.post("/choice", response_model=RpsGameSchema)
async def submit_choice(
    user_id: CurrentUserId,
    choice: ChoiceSchema,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    game_repository: Annotated[RpsGameRepository, Depends()],
):
    async with session.begin():
        game = await game_repository.get_active_game_for_user(user_id)

        if not game:
            raise HTTPException(status_code=404, detail="No active game found.")

        if game.player1_id == user_id:
            if game.player1_choice is not None:
                raise HTTPException(status_code=400, detail="Choice already submitted.")
            game.player1_choice = choice.choice
        else:
            if game.player2_choice is not None:
                raise HTTPException(status_code=400, detail="Choice already submitted.")
            game.player2_choice = choice.choice

        await game_repository.update_game(game)

        return game


@router.get("/result", response_model=RpsGameResultSchema)
async def get_game_result(
    user_id: CurrentUserId,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    game_repository: Annotated[RpsGameRepository, Depends()],
):
    async with session.begin():
        game = await game_repository.get_active_game_for_user(user_id)

        if not game:
            raise HTTPException(status_code=404, detail="No active game found.")

        if game.status == RpsGameStatus.COMPLETED:
            result = determine_winner(game.player1_choice, game.player2_choice)
            return RpsGameResultSchema(result=result, game=game)
        else:
            if datetime.utcnow() >= game.started_at + timedelta(seconds=10):
                if game.player1_choice and not game.player2_choice:
                    winner = 1
                elif not game.player1_choice and game.player2_choice:
                    winner = 2
                elif not game.player1_choice and not game.player2_choice:
                    winner = 0
                else:
                    winner = determine_winner(game.player1_choice, game.player2_choice)

                game.status = RpsGameStatus.COMPLETED
                game.completed_at = datetime.utcnow()

                player1 = await user_repository.get_user_for_update(game.player1_id)
                player2 = await user_repository.get_user_for_update(game.player2_id)

                if winner == 1:
                    player1.points += 200
                    player2.points -= 200
                elif winner == 2:
                    player2.points += 200
                    player1.points -= 200

                await game_repository.update_game(game)
                await user_repository.update_user(player1)
                await user_repository.update_user(player2)

                return RpsGameResultSchema(result=winner, game=game)
            else:
                return RpsGameResultSchema(result=None, game=game)
