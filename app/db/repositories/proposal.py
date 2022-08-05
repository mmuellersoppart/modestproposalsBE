from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.tables.proposal import Proposal
from app.models.schema import proposal_schema


class ProposalRepository(BaseRepository[proposal_schema.ProposalCreate, proposal_schema.ProposalSchema, Proposal]):
    @property
    def _in_schema(self) -> Type[proposal_schema.ProposalCreate]:
        return proposal_schema.ProposalCreate

    @property
    def _schema(self) -> Type[proposal_schema.ProposalSchema]:
        return proposal_schema.ProposalSchema

    @property
    def _table(self) -> Type[Proposal]:
        return Proposal
