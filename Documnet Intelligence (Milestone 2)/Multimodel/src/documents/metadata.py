from pydantic import BaseModel, Field
from typing import Optional
 
 
class ChunkMetadata(BaseModel):
 
    document_name: str = Field(
        ...,
        description="Name of the source document"
    )
 
    document_type: str = Field(
        ...,
        description="File type"
    )
 
    page_number: int = Field(
        0,
        description="Page number"
    )
 
    chunk_id: str = Field(
        ...,
        description="Unique ID for this chunk"
    )
 
    uploaded_by: Optional[str] = Field(
        None,
        description="Who uploaded"
    )