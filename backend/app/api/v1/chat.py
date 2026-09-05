from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models import User, Conversation
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse, ConversationListResponse, ConversationDetailResponse
from app.services.chat_service import ChatService
from sqlalchemy import select, desc

router = APIRouter(tags=["chat"])
chat_service = ChatService()

@router.post("", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await chat_service.process_message(
        db=db,
        user_id=current_user.id,
        message=request.message,
        conversation_id=request.conversation_id,
        jurisdiction=request.jurisdiction
    )
    return result

@router.get("/conversations", response_model=List[ConversationListResponse])
async def list_conversations(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Conversation).where(Conversation.user_id == current_user.id).order_by(desc(Conversation.created_at))
    result = await db.execute(stmt)
    convos = result.scalars().all()
    # In a real app we'd get message count properly
    return [
        {**c.__dict__, "message_count": 0} for c in convos
    ]

@router.get("/conversations/{id}", response_model=ConversationDetailResponse)
async def get_conversation(
    id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Conversation).where(Conversation.id == id, Conversation.user_id == current_user.id)
    result = await db.execute(stmt)
    convo = result.scalar_one_or_none()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Needs messages loaded, simplified here
    return {**convo.__dict__, "messages": []}

@router.delete("/conversations/{id}")
async def delete_conversation(
    id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Conversation).where(Conversation.id == id, Conversation.user_id == current_user.id)
    result = await db.execute(stmt)
    convo = result.scalar_one_or_none()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    await db.delete(convo)
    await db.commit()
    return {"status": "success"}
