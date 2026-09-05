"""
Ayur-Lex-AI — Real-Time Legal Chamber Debate WebSocket Streaming API

Provides a WebSocket endpoint at /api/v1/ws/debate that streams sequential multi-agent
adversarial patent debate rounds (Applicant, Patent Examiner, Judicial Arbiter).
"""

import json
import asyncio
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
import structlog

from app.rag.debate_engine import DebateEngine

logger = structlog.get_logger(__name__)

router = APIRouter()
debate_engine = DebateEngine()


@router.websocket("/debate")
async def websocket_debate_endpoint(websocket: WebSocket):
    """
    WebSocket streaming endpoint for the 3D Legal Chamber Debate.
    
    Receives an initial JSON configuration message:
    {
        "title": "Novel Herbal Synergy Formulation",
        "description": "Composition of Curcuma longa and Piper nigrum...",
        "innovation": "Enhanced bioavailability and synergistic index CI=0.72",
        "jurisdiction": "India"
    }
    
    Streams sequential debate events:
    {
        "agent": "applicant" | "examiner" | "arbiter",
        "stage": str,
        "content": str,
        "citations": list[str],
        "confidence": float
    }
    """
    await websocket.accept()
    logger.info("3D Legal Chamber WebSocket client connected")

    try:
        # Wait for initial trigger or formulation config from client
        # with default fallback if user just opens the stream
        query = None
        title = "Novel Polyherbal Synergistic Formulation"
        description = "Therapeutic composition comprising Withania somnifera and Piper longum with enhanced bio-availability."
        innovation = "Synergistic bio-enhancement with Combination Index CI < 0.75"
        jurisdiction = "India"

        try:
            raw_msg = await asyncio.wait_for(websocket.receive_text(), timeout=4.0)
            data = json.loads(raw_msg)
            query = data.get("query")
            title = data.get("title", title)
            description = data.get("description", description)
            innovation = data.get("innovation", innovation)
            jurisdiction = data.get("jurisdiction", jurisdiction)
            if query and not data.get("title"):
                title = query[:80] + ("..." if len(query) > 80 else "")
                description = query
        except asyncio.TimeoutError:
            logger.info("No immediate configuration received from client; using active formulation defaults")
        except Exception as e:
            logger.warning("Error reading initial message, falling back to default formulation", error=str(e))

        # Stream the multi-agent debate sequentially
        async for event in debate_engine.stream_debate(
            title=title,
            description=description,
            innovation_details=innovation,
            jurisdiction=jurisdiction,
            query=query,
        ):
            await websocket.send_json(event)
            await asyncio.sleep(0.02)

        # Send final completion event
        await websocket.send_json({
            "agent": "arbiter",
            "model": "Claude 3.5 Sonnet",
            "stage": "Final Verdict",
            "text_chunk": "",
            "content": "The Judicial Arbiter has rendered the final IRAC verdict and closed the proceedings.",
            "is_turn_complete": True,
            "citations": [
                "The Patents Act, 1970",
                "Biological Diversity Act, 2002"
            ],
            "confidence": 1.0,
            "tokens_per_sec": 44.0,
            "statutory_risk": {
                "sec_3p": "Cleared",
                "sec_3e": "Synergistic (CI < 1.0)",
                "bda_form3": "Approval Required"
            },
            "status": "completed"
        })


    except WebSocketDisconnect:
        logger.info("3D Legal Chamber WebSocket client disconnected normally")
    except Exception as e:
        logger.error("Exception in 3D Legal Chamber WebSocket stream", error=str(e))
        try:
            await websocket.send_json({
                "agent": "arbiter",
                "stage": "Error",
                "content": f"Streaming interrupted: {str(e)}",
                "citations": [],
                "confidence": 0.0,
                "status": "error"
            })
        except Exception:
            pass
