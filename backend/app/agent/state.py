
from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ExtractedIntent(BaseModel):
    intent_type: str = Field(
        description="Type of task: 'segmentation', 'eda', 'explainability', 'conversion_analysis', or 'ambiguous'"
    )
    features_requested: List[str] = Field(
        default_factory=list, 
        description="Columns or metrics mentioned in the query (e.g., ['avg_monthly_balance', 'transaction_frequency'])"
    )
    target_segments: List[str] = Field(
        default_factory=list, 
        description="Named segments mentioned (e.g., ['priority', 'regular', 'dormant'])"
    )
    filters: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Numerical or categorical filters extracted (e.g., {'min_balance': 50000})"
    )
    is_ambiguous: bool = Field(
        default=False, 
        description="Set to True if the query lacks necessary detail or feature selection"
    )
    clarification_question: Optional[str] = Field(
        default=None, 
        description="Question to ask the user if intent is ambiguous"
    )

class AgentState(TypedDict):
    raw_query: str
    thread_id: str
    intent_data: Optional[Dict[str, Any]]
    requires_human_input: bool
    human_clarification: Optional[str]
    prepared_data: Optional[Dict[str, Any]]
    execution_results: Optional[Dict[str, Any]]
    persona_explanations: Optional[Dict[str, Any]]
    final_output: Optional[Dict[str, Any]]