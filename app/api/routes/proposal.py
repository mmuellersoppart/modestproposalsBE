import logging
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.dependencies.db import get_db
from app.db.repositories.proposal import ProposalRepository
from app.models.schema import proposal_schema
from app.db.util import row2dict

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def list_all_proposals(
        db: AsyncSession = Depends(get_db)
) -> [proposal_schema.ProposalPublic]:
    proposal_repository = ProposalRepository(db)
    proposals = await proposal_repository.list_all()
    return [proposal_schema.ProposalPublic(**proposal.dict()) for proposal in proposals]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=proposal_schema.ProposalPublic)
async def create_proposal(
    payload: proposal_schema.ProposalCreate, db: AsyncSession = Depends(get_db)
) -> proposal_schema.ProposalPublic:
    proposal_repository = ProposalRepository(db)
    proposal = await proposal_repository.create(payload)
    return proposal_schema.ProposalPublic(**row2dict(proposal))


@router.get(
    "/{proposal_id}", status_code=status.HTTP_200_OK, response_model=proposal_schema.ProposalPublic
)
async def get_proposal(
    proposal_id: UUID, db: AsyncSession = Depends(get_db)
) -> proposal_schema.ProposalPublic:
    proposal_repository = ProposalRepository(db)
    proposal = await proposal_repository.get_by_id(proposal_id)
    return proposal_schema.ProposalPublic(**row2dict(proposal))
