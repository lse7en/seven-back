# routers/game.py

import random
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from src.constants import WAITING_TIME_TO_MATCH_BOT, WAITING_TIME_TO_SUBMIT_CHOICES
from src.core.database import DBSession
from src.deps import CurrentUserId
from src.models.game import RpsChoice, RpsGame, RpsGameStatus
from src.repositories.game_repository import RpsGameRepository
from src.repositories.user_repository import UserRepository
from src.schemas.game_schemas import RpsChoiceSchema, RpsGameSchema

router = APIRouter(prefix="/game/rps", tags=["game"])


async def get_playable_game(
    user_id: CurrentUserId,
    game_id: int | None,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    game_repository: Annotated[RpsGameRepository, Depends()],
) -> RpsGame | None:
    async with session.begin():
        if game_id:
            game = await game_repository.get_game_for_update(game_id)
        else:
            game = await game_repository.get_active_game_for_user(user_id)

        if not game:
            print("Game not found")
            return None
        
        print("Game found", game.id, game.status)

        if (
            game.status == RpsGameStatus.WAITING_FOR_CHOICES
            and (
                datetime.now(UTC)
                >= game.started_at + timedelta(seconds=WAITING_TIME_TO_SUBMIT_CHOICES)
            )
        ) or (game.player1_choice and game.player2_choice):
            winner = game.winner
            game.status = RpsGameStatus.COMPLETED
            game.completed_at = datetime.now(UTC)

            player1 = await user_repository.get_user_for_update(game.player1_id)
            player2 = await user_repository.get_user_for_update(game.player2_id)

            if winner == player1.id:
                player1.points += 200
                player2.points -= 200
            elif winner == player2.id:
                player2.points += 200
                player1.points -= 200

            await game_repository.add_game(game)
            await user_repository.add_user(player1)
            await user_repository.add_user(player2)
        

        return game


async def fetch_players(game: RpsGame, user_repository: UserRepository) -> RpsGame:
    game.player1 = await user_repository.get_user_or_none_by_id(game.player1_id)
    game.player2 = await user_repository.get_user_or_none_by_id(game.player2_id)
    return game


@router.post("/start", response_model=RpsGameSchema)
async def start_game(
    user_id: CurrentUserId,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    game_repository: Annotated[RpsGameRepository, Depends()],
):
    game = await get_playable_game(
        user_id=user_id,
        game_id=None,
        session=session,
        game_repository=game_repository,
        user_repository=user_repository,
    )


    
    


    async with session.begin():

        if game:
            return await fetch_players(game, user_repository)


        user = await user_repository.get_user_for_update(user_id)

        if user.points < 200:
            raise HTTPException(
                status_code=400, detail="Not enough points to start a game."
            )

        waiting_game = await game_repository.get_waiting_game()

        if waiting_game:
            waiting_game.player2_id = user_id
            waiting_game.status = RpsGameStatus.WAITING_FOR_CHOICES
            waiting_game.started_at = datetime.now(UTC)
            await game_repository.add_game(waiting_game)
            return await fetch_players(waiting_game, user_repository)
        else:
            new_game = RpsGame(player1_id=user_id)
            await game_repository.add_game(new_game)
            return await fetch_players(new_game, user_repository)


@router.get("/{game_id}", response_model=RpsGameSchema)
async def game_status(
    game_id: int,
    session: DBSession,
    user_id: CurrentUserId,
    user_repository: Annotated[UserRepository, Depends()],
    game_repository: Annotated[RpsGameRepository, Depends()],
):
    game = await get_playable_game(
        user_id=user_id,
        game_id=game_id,
        session=session,
        user_repository=user_repository,
        game_repository=game_repository,
    )

    if not game:
        raise HTTPException(status_code=404, detail="Game not found.")

    if game.status == RpsGameStatus.WAITING_FOR_PLAYER and datetime.now(
        UTC
    ) >= game.created_at + timedelta(seconds=WAITING_TIME_TO_MATCH_BOT):
        bot_user = await user_repository.get_random_bot()

        game.player2_id = bot_user.id
        game.status = RpsGameStatus.WAITING_FOR_CHOICES
        game.started_at = datetime.now(UTC)
        game.player2_choice = random.choice(list(RpsChoice))
        await game_repository.add_game(game)

    return await fetch_players(game, user_repository)


@router.post("/{game_id}/choice", response_model=RpsGameSchema)
async def submit_choice(
    game_id: int,
    user_id: CurrentUserId,
    choice: RpsChoiceSchema,
    session: DBSession,
    game_repository: Annotated[RpsGameRepository, Depends()],
    user_repository: Annotated[UserRepository, Depends()],
):
    game = await get_playable_game(
        user_id=user_id,
        game_id=game_id,
        session=session,
        user_repository=user_repository,
        game_repository=game_repository,
    )

    if not game:
        raise HTTPException(status_code=404, detail="Game not found.")

    if game.player1_id == user_id:
        if game.player1_choice is not None:
            raise HTTPException(status_code=400, detail="Choice already submitted.")
        game.player1_choice = choice.choice
    else:
        if game.player2_choice is not None:
            raise HTTPException(status_code=400, detail="Choice already submitted.")
        game.player2_choice = choice.choice
    
    await game_repository.add_game(game)
    return await fetch_players(game, user_repository)
