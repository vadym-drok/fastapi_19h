from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.models import Vote, User
from app.oauth2 import get_current_user
from app.schemas import VoteAddDelete
from app.database import get_db


router = APIRouter(
    prefix='/votes',
    tags=['Votes'],
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote_add_delete(vote: VoteAddDelete, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    # Add vote
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'user {current_user.id} has already voted on post {vote.post_id}'
            )
        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    # Delete vote
    else:
        if not found_vote:
            raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist' )
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deletes vote"}
