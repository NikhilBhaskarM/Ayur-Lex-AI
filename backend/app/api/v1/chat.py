from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models import User, Conversation, Message
from app.schemas.chat import (
    ChatMessageRequest, ChatMessageResponse, ConversationListResponse,
    ConversationDetailResponse, MessageResponse
)
from app.services.chat_service import ChatService
from sqlalchemy import select, desc, func

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
        jurisdiction=request.jurisdiction,
        language=request.language,
        llm_provider=request.llm_provider,
        llm_model=request.llm_model,
        llm_api_key=request.llm_api_key,
        llm_base_url=request.llm_base_url,
    )
    return result

@router.get("/conversations", response_model=List[ConversationListResponse])
async def list_conversations(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(
            Conversation,
            func.count(Message.id).label("msg_count")
        )
        .outerjoin(Message, Message.conversation_id == Conversation.id)
        .where(Conversation.user_id == current_user.id)
        .group_by(Conversation.id)
        .order_by(desc(Conversation.created_at))
    )
    result = await db.execute(stmt)
    rows = result.all()
    
    return [
        ConversationListResponse(
            id=convo.id,
            title=convo.title,
            jurisdiction=convo.jurisdiction,
            status=convo.status,
            created_at=convo.created_at,
            updated_at=convo.updated_at,
            message_count=count
        )
        for convo, count in rows
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
    
    # Load all messages in chronological order
    msg_stmt = (
        select(Message)
        .where(Message.conversation_id == id)
        .order_by(Message.created_at.asc())
    )
    msg_result = await db.execute(msg_stmt)
    db_messages = msg_result.scalars().all()
    
    formatted_messages = [
        MessageResponse(
            id=m.id,
            role=m.role,
            content=m.content,
            citations=m.citations or [],
            confidence=m.confidence,
            confidence_score=m.confidence_score,
            confidence_data=m.metadata_,
            created_at=m.created_at
        )
        for m in db_messages
    ]

    return ConversationDetailResponse(
        id=convo.id,
        title=convo.title,
        jurisdiction=convo.jurisdiction,
        status=convo.status,
        messages=formatted_messages,
        created_at=convo.created_at,
        updated_at=convo.updated_at
    )

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
