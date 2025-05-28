from pydantic import BaseModel, EmailStr, UUID4, Field
from typing import Optional, List, Any, Dict # Added Dict for Guardrail rules
import enum

# This should match the Enum in your models.py
class ToolTypeEnumSchema(str, enum.Enum):
    BUILTIN = "builtin"
    MCP_SERVER = "mcp_server"

class RoleEnum(str, enum.Enum):
    admin = "admin"
    devops = "devops"
    user = "user"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: UUID4
    created_at: Any
    updated_at: Any

    class Config:
        orm_mode = True

# MCPServer Schemas
class MCPServerBase(BaseModel):
    toolgroup_id: str # LlamaStack identifier (now PK)
    name: str
    description: Optional[str] = None
    endpoint_url: str
    configuration: Optional[Dict[str, Any]] = None

class MCPServerCreate(MCPServerBase):
    pass

class MCPServerRead(MCPServerBase):
    created_by: Optional[UUID4] = None
    created_at: Any
    updated_at: Any

    class Config:
        orm_mode = True

# KnowledgeBase Schemas
class KnowledgeBaseBase(BaseModel):
    vector_db_name: str # LlamaStack identifier (now PK)
    name: str
    version: str
    embedding_model: str
    provider_id: Optional[str] = None
    is_external: bool = False
    source: Optional[str] = None
    source_configuration: Optional[Dict[str, Any]] = None # More specific type

class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass

class KnowledgeBaseRead(KnowledgeBaseBase):
    created_by: Optional[UUID4] = None
    created_at: Any
    updated_at: Any

    class Config:
        orm_mode = True

# Tool Association Info for VirtualAssistant
class ToolAssociationInfo(BaseModel):
    toolgroup_id: str # This refers to MCPServer.toolgroup_id or BuiltInTool.toolgroup_id

# VirtualAssistant Schemas
class VirtualAssistantBase(BaseModel):
    name: str
    prompt: str
    model_name: str
    knowledge_base_ids: List[str] = [] # Now expecting list of vector_db_names
    tools: List[ToolAssociationInfo] = [] # Changed from tool_ids: List[str]

class VirtualAssistantCreate(VirtualAssistantBase):
    pass

class VirtualAssistantUpdate(VirtualAssistantBase):
    name: Optional[str] = None
    prompt: Optional[str] = None
    model_name: Optional[str] = None
    knowledge_base_ids: Optional[List[str]] = None # Now expecting list of vector_db_names
    tools: Optional[List[ToolAssociationInfo]] = None


class VirtualAssistantRead(VirtualAssistantBase):
    id: UUID4
    created_by: Optional[UUID4] = None
    created_at: Any
    updated_at: Any

    class Config:
        orm_mode = True

class ChatHistoryBase(BaseModel):
    virtual_assistant_id: UUID4
    user_id: UUID4
    message: str
    response: str

class ChatHistoryCreate(ChatHistoryBase):
    pass

class ChatHistoryRead(ChatHistoryBase):
    id: UUID4
    created_at: Any

    class Config:
        orm_mode = True

class GuardrailBase(BaseModel):
    name: str
    rules: Dict[str, Any]

class GuardrailCreate(GuardrailBase):
    pass

class GuardrailRead(GuardrailBase):
    id: UUID4
    created_by: Optional[UUID4] = None
    created_at: Any
    updated_at: Any

    class Config:
        orm_mode = True

# ModelServer Schemas (These seemed largely okay with your models.py)
class ModelServerBase(BaseModel):
    name: str
    provider_name: str
    model_name: str
    endpoint_url: str
    token: Optional[str] = None

class ModelServerCreate(ModelServerBase):
    pass

class ModelServerUpdate(ModelServerBase):
    name: Optional[str] = None
    provider_name: Optional[str] = None
    model_name: Optional[str] = None
    endpoint_url: Optional[str] = None
    token: Optional[str] = None

class ModelServerRead(ModelServerBase):
    id: UUID4

    class Config:
        orm_mode = True