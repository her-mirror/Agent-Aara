# Workflow API Reference

## 🔌 Overview

The Aara Health Agent provides a comprehensive API for integrating with and extending the workflow system. This documentation covers all available endpoints, classes, and methods for developers.

## 🏗️ Core Workflow API

### WorkflowManager Class

The main entry point for workflow operations.

```python
from src.agent.workflow import WorkflowManager

class WorkflowManager:
    """
    Main workflow orchestration class
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize workflow manager
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.workflow = self._create_workflow()
        self.state_manager = StateManager()
    
    def process_message(
        self, 
        message: str, 
        session_id: str = None,
        context: Dict[str, Any] = None
    ) -> WorkflowResponse:
        """
        Process a user message through the workflow
        
        Args:
            message: User input message
            session_id: Optional session identifier
            context: Additional context information
            
        Returns:
            WorkflowResponse: Complete response object
            
        Example:
            >>> manager = WorkflowManager(config)
            >>> response = manager.process_message(
            ...     "I have irregular periods",
            ...     session_id="user123"
            ... )
            >>> print(response.final_response)
        """
```

### WorkflowResponse Class

Response object containing all workflow output.

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class WorkflowResponse:
    """
    Complete workflow response object
    """
    # Core response
    final_response: str
    session_id: str
    
    # Processing information
    processing_time: float
    nodes_executed: List[str]
    tools_used: List[str]
    
    # Safety information
    safety_flags: List[str]
    emergency_detected: bool
    
    # Context and state
    updated_context: Dict[str, Any]
    conversation_state: Dict[str, Any]
    
    # Metadata
    timestamp: str
    workflow_version: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert response to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
```

## 🔄 State Management API

### ConversationState

Core state management for conversations.

```python
from typing import TypedDict, List, Dict, Any, Optional

class ConversationState(TypedDict):
    """
    Conversation state structure
    """
    # Current interaction
    user_input: str
    final_response: Optional[str]
    
    # History and context
    chat_history: List[Dict[str, str]]
    context: Dict[str, Any]
    
    # Processing metadata
    intermediate_steps: List[Dict[str, Any]]
    route_to: Optional[str]
    tool_output: Optional[str]
    
    # Safety tracking
    safety_flags: List[str]
    emergency_detected: bool
    
    # Session information
    session_id: str
    timestamp: str
    processing_time: float
```

### StateManager Class

Manages conversation state persistence and retrieval.

```python
class StateManager:
    """
    Manage conversation state across sessions
    """
    
    def __init__(self, storage_backend: str = "memory"):
        """
        Initialize state manager
        
        Args:
            storage_backend: Storage type (memory, redis, file)
        """
        self.storage = self._init_storage(storage_backend)
    
    def get_state(self, session_id: str) -> Optional[ConversationState]:
        """
        Retrieve conversation state for session
        
        Args:
            session_id: Session identifier
            
        Returns:
            ConversationState or None if not found
        """
    
    def save_state(self, session_id: str, state: ConversationState):
        """
        Save conversation state for session
        
        Args:
            session_id: Session identifier
            state: Conversation state to save
        """
    
    def clear_state(self, session_id: str):
        """
        Clear conversation state for session
        
        Args:
            session_id: Session identifier
        """
    
    def list_sessions(self) -> List[str]:
        """
        List all active session IDs
        
        Returns:
            List of session identifiers
        """
```

## 🔧 Node API

### Custom Node Development

Create custom workflow nodes for specialized functionality.

```python
from abc import ABC, abstractmethod

class WorkflowNode(ABC):
    """
    Abstract base class for workflow nodes
    """
    
    @abstractmethod
    def execute(self, state: ConversationState) -> ConversationState:
        """
        Execute node logic
        
        Args:
            state: Current conversation state
            
        Returns:
            Updated conversation state
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get node name"""
        pass
    
    def validate_input(self, state: ConversationState) -> bool:
        """
        Validate input state
        
        Args:
            state: Conversation state to validate
            
        Returns:
            True if valid, False otherwise
        """
        return True

# Example custom node
class CustomHealthNode(WorkflowNode):
    """
    Custom node for specialized health processing
    """
    
    def execute(self, state: ConversationState) -> ConversationState:
        """
        Custom health processing logic
        """
        # Your custom logic here
        user_input = state["user_input"]
        
        # Process input
        result = self.process_health_query(user_input)
        
        # Update state
        state["final_response"] = result
        state["intermediate_steps"].append({
            "node": self.get_name(),
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return state
    
    def get_name(self) -> str:
        return "custom_health_node"
    
    def process_health_query(self, query: str) -> str:
        """Custom health processing logic"""
        # Implement your logic
        return "Custom health response"
```

### Node Registration

Register custom nodes with the workflow.

```python
class WorkflowBuilder:
    """
    Build and configure workflows
    """
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
    
    def add_node(self, node: WorkflowNode):
        """
        Add custom node to workflow
        
        Args:
            node: Custom workflow node
        """
        self.nodes[node.get_name()] = node
    
    def add_edge(self, from_node: str, to_node: str, condition: callable = None):
        """
        Add edge between nodes
        
        Args:
            from_node: Source node name
            to_node: Target node name
            condition: Optional condition function
        """
        self.edges.append({
            "from": from_node,
            "to": to_node,
            "condition": condition
        })
    
    def build(self) -> StateGraph:
        """
        Build the workflow graph
        
        Returns:
            Compiled StateGraph
        """
        workflow = StateGraph(ConversationState)
        
        # Add nodes
        for name, node in self.nodes.items():
            workflow.add_node(name, node.execute)
        
        # Add edges
        for edge in self.edges:
            if edge["condition"]:
                workflow.add_conditional_edges(
                    edge["from"],
                    edge["condition"],
                    {True: edge["to"], False: END}
                )
            else:
                workflow.add_edge(edge["from"], edge["to"])
        
        return workflow.compile()
```

## 🛠️ Tool Integration API

### Tool Interface

Standard interface for integrating tools with the workflow.

```python
from abc import ABC, abstractmethod

class WorkflowTool(ABC):
    """
    Abstract base class for workflow tools
    """
    
    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute tool logic
        
        Args:
            input_data: Tool input pAarameters
            
        Returns:
            Tool execution results
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get tool name"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get tool description"""
        pass
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate tool input
        
        Args:
            input_data: Input to validate
            
        Returns:
            True if valid, False otherwise
        """
        return True

# Example custom tool
class CustomAnalysisTool(WorkflowTool):
    """
    Custom analysis tool
    """
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform custom analysis
        """
        query = input_data.get("query", "")
        context = input_data.get("context", {})
        
        # Your analysis logic here
        analysis_result = self.analyze(query, context)
        
        return {
            "success": True,
            "result": analysis_result,
            "tool": self.get_name(),
            "metadata": {
                "processing_time": 0.5,
                "confidence": 0.9
            }
        }
    
    def get_name(self) -> str:
        return "custom_analysis_tool"
    
    def get_description(self) -> str:
        return "Performs custom analysis on user queries"
    
    def analyze(self, query: str, context: Dict[str, Any]) -> str:
        """Custom analysis logic"""
        # Implement your analysis
        return "Analysis result"
```

### Tool Registry

Manage and discover available tools.

```python
class ToolRegistry:
    """
    Registry for workflow tools
    """
    
    def __init__(self):
        self.tools = {}
    
    def register_tool(self, tool: WorkflowTool):
        """
        Register a tool
        
        Args:
            tool: Tool to register
        """
        self.tools[tool.get_name()] = tool
    
    def get_tool(self, name: str) -> Optional[WorkflowTool]:
        """
        Get tool by name
        
        Args:
            name: Tool name
            
        Returns:
            Tool instance or None
        """
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """
        List all registered tools
        
        Returns:
            List of tool names
        """
        return list(self.tools.keys())
    
    def get_tool_info(self, name: str) -> Dict[str, str]:
        """
        Get tool information
        
        Args:
            name: Tool name
            
        Returns:
            Tool information dictionary
        """
        tool = self.get_tool(name)
        if tool:
            return {
                "name": tool.get_name(),
                "description": tool.get_description()
            }
        return {}
```

## 🔍 Monitoring API

### Workflow Metrics

Monitor workflow performance and usage.

```python
class WorkflowMetrics:
    """
    Collect and analyze workflow metrics
    """
    
    def __init__(self):
        self.metrics = {
            "total_executions": 0,
            "node_execution_times": {},
            "tool_usage": {},
            "error_counts": {},
            "safety_triggers": {}
        }
    
    def record_execution(self, response: WorkflowResponse):
        """
        Record workflow execution metrics
        
        Args:
            response: Workflow response to analyze
        """
        self.metrics["total_executions"] += 1
        
        # Record processing time
        self._record_processing_time(response.processing_time)
        
        # Record node usage
        for node in response.nodes_executed:
            self._record_node_usage(node)
        
        # Record tool usage
        for tool in response.tools_used:
            self._record_tool_usage(tool)
        
        # Record safety triggers
        for flag in response.safety_flags:
            self._record_safety_trigger(flag)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get metrics summary
        
        Returns:
            Metrics summary dictionary
        """
        return {
            "total_executions": self.metrics["total_executions"],
            "average_processing_time": self._calculate_average_processing_time(),
            "most_used_tools": self._get_top_tools(5),
            "safety_trigger_rate": self._calculate_safety_rate(),
            "error_rate": self._calculate_error_rate()
        }
    
    def export_metrics(self, format: str = "json") -> str:
        """
        Export metrics in specified format
        
        Args:
            format: Export format (json, csv, yaml)
            
        Returns:
            Formatted metrics string
        """
        if format == "json":
            return json.dumps(self.metrics, indent=2)
        elif format == "yaml":
            return yaml.dump(self.metrics, indent=2)
        # Add other formats as needed
```

## 🔐 Security API

### Access Control

Manage access to workflow functionality.

```python
class WorkflowSecurity:
    """
    Security controls for workflow access
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.rate_limiter = RateLimiter(config.get("rate_limit", {}))
        self.access_control = AccessControl(config.get("access_control", {}))
    
    def validate_request(self, request: WorkflowRequest) -> bool:
        """
        Validate incoming workflow request
        
        Args:
            request: Workflow request to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check rate limits
        if not self.rate_limiter.check_limit(request.session_id):
            return False
        
        # Check access permissions
        if not self.access_control.check_permission(request):
            return False
        
        # Validate input content
        if not self._validate_content(request.message):
            return False
        
        return True
    
    def sanitize_input(self, message: str) -> str:
        """
        Sanitize user input
        
        Args:
            message: Raw user message
            
        Returns:
            Sanitized message
        """
        # Remove potentially harmful content
        sanitized = self._remove_harmful_patterns(message)
        
        # Limit message length
        max_length = self.config.get("max_message_length", 1000)
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
```

## 📊 Analytics API

### Usage Analytics

Track and analyze workflow usage patterns.

```python
class WorkflowAnalytics:
    """
    Analytics for workflow usage
    """
    
    def __init__(self, storage_backend: str = "memory"):
        self.storage = self._init_storage(storage_backend)
        self.analyzers = {
            "conversation": ConversationAnalyzer(),
            "health": HealthTopicAnalyzer(),
            "safety": SafetyAnalyzer()
        }
    
    def track_interaction(self, request: WorkflowRequest, response: WorkflowResponse):
        """
        Track user interaction
        
        Args:
            request: Original request
            response: Workflow response
        """
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "session_id": request.session_id,
            "user_input": request.message,
            "response": response.final_response,
            "processing_time": response.processing_time,
            "tools_used": response.tools_used,
            "safety_flags": response.safety_flags
        }
        
        self.storage.store_interaction(interaction)
        
        # Run analyzers
        for analyzer in self.analyzers.values():
            analyzer.analyze_interaction(interaction)
    
    def generate_report(self, time_period: str = "24h") -> Dict[str, Any]:
        """
        Generate analytics report
        
        Args:
            time_period: Time period for report (1h, 24h, 7d, 30d)
            
        Returns:
            Analytics report
        """
        interactions = self.storage.get_interactions(time_period)
        
        report = {
            "period": time_period,
            "total_interactions": len(interactions),
            "conversation_insights": self.analyzers["conversation"].get_insights(),
            "health_topics": self.analyzers["health"].get_top_topics(),
            "safety_events": self.analyzers["safety"].get_safety_summary()
        }
        
        return report
```

## 🔄 Integration Examples

### Basic Integration

```python
# Initialize workflow manager
config = {
    "agent": {"name": "Aara", "personality": "empathetic"},
    "safety": {"emergency_detection": True},
    "tools": {"health_advice": {"enabled": True}}
}

workflow_manager = WorkflowManager(config)

# Process user message
response = workflow_manager.process_message(
    message="I have been having irregular periods",
    session_id="user123",
    context={"user_age": 25, "previous_topics": ["menstrual_health"]}
)

print(f"Response: {response.final_response}")
print(f"Tools used: {response.tools_used}")
print(f"Processing time: {response.processing_time}s")
```

### Custom Tool Integration

```python
# Create custom tool
class NutritionTool(WorkflowTool):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Custom nutrition analysis logic
        return {"success": True, "result": "Nutrition advice"}
    
    def get_name(self) -> str:
        return "nutrition_analysis"
    
    def get_description(self) -> str:
        return "Provides nutrition analysis and recommendations"

# Register tool
tool_registry = ToolRegistry()
tool_registry.register_tool(NutritionTool())

# Use in workflow
workflow_manager.register_tool_registry(tool_registry)
```

### Monitoring Integration

```python
# Set up monitoring
metrics = WorkflowMetrics()
analytics = WorkflowAnalytics()

# Process with monitoring
response = workflow_manager.process_message("Hello Aara")

# Record metrics
metrics.record_execution(response)
analytics.track_interaction(request, response)

# Get insights
summary = metrics.get_metrics_summary()
report = analytics.generate_report("24h")
```

This API provides comprehensive access to all workflow functionality, enabling developers to integrate, extend, and monitor the Aara Health Agent effectively. 