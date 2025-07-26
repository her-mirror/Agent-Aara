# 📊 Individual Chat Metrics System

## Overview

The AAara Health Agent now includes **comprehensive individual chat metrics tracking** that monitors CPU and RAM usage for every single question and response, providing:

- **SepAarate metrics for each chat question**
- **Peak and low resource values** during each conversation
- **Live real-time monitoring** with streaming metrics
- **Detailed performance analysis** per conversation

## 🎯 What You Get

### 1. **Individual Chat Tracking**
Every single chat question gets its own detailed metrics:
```
💬 CHAT METRICS [WORKFLOW_START] - chat_1234567890
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Message: "I have oily skin and acne. What skincare routine..."
⏱️  Elapsed: 850ms
🔸 Current CPU: 45.2% | Peak: 47.8% | Low: 12.1%
🔸 Current Memory: 156.8MB | Peak: 168.3MB | Low: 145.2MB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2. **Peak & Low Value Tracking**
Each chat tracks:
- **Peak CPU usage** during AI processing
- **Peak memory usage** during the response
- **Low CPU/memory values** for baseline comparison
- **Performance rating** (Good/High Usage)

### 3. **6-Stage Monitoring**
Each chat is monitored through these stages:
1. **request_received** - Initial request processing
2. **processing_history** - Chat history conversion
3. **workflow_start** - AI workflow begins
4. **workflow_completed** - AI response generated
5. **storing_conversation** - Saving conversation
6. **response_prepAaration** - Final response prep

### 4. **Live Metrics Streaming**
Real-time metrics with Server-Sent Events:
```
🖥️  CPU: 25.4% | Memory: 145.2MB | Time: 2024-01-20T10:30:45
🖥️  CPU: 28.6% | Memory: 153.5MB | Time: 2024-01-20T10:30:46
```

## 📡 **API Endpoints**

### Main Chat Endpoint (Enhanced)
```http
POST /chat
Content-Type: application/json

{
  "message": "I have oily skin, what routine do you recommend?",
  "conversation_id": "my_skincare_chat",
  "chat_history": []
}
```

**Response includes individual metrics:**
```json
{
  "response": "For oily skin, I recommend...",
  "conversation_id": "my_skincare_chat",
  "metadata": {
    "individual_chat_metrics": {
      "total_duration_ms": 1250,
      "peak_metrics": {
        "cpu": 47.8,
        "memory": 168.3
      },
      "low_metrics": {
        "cpu": 12.1,
        "memory": 145.2
      },
      "summary": {
        "cpu_range": "12.1% - 47.8%",
        "memory_range": "145.2MB - 168.3MB",
        "performance_rating": "Good"
      }
    },
    "performance_summary": {
      "total_duration_ms": 1250,
      "peak_cpu_percent": 47.8,
      "peak_memory_mb": 168.3,
      "low_cpu_percent": 12.1,
      "low_memory_mb": 145.2,
      "performance_rating": "Good",
      "stages_tracked": 6
    }
  }
}
```

### Live Metrics Stream
```http
GET /live-metrics
Accept: text/event-stream
```

Connect to this endpoint for real-time metrics every second.

### Conversation Metrics Summary
```http
GET /conversation-metrics/{conversation_id}
```

Get detailed metrics for all chats in a specific conversation:
```json
{
  "conversation_id": "my_skincare_chat",
  "total_chats": 4,
  "aggregate_stats": {
    "total_duration_ms": 4850,
    "average_duration_ms": 1212.5,
    "peak_cpu_overall": 52.3,
    "peak_memory_overall": 185.7
  },
  "individual_chats": [
    {
      "message": "Hello Aara! How are you?",
      "total_duration_ms": 450,
      "peak_metrics": { "cpu": 25.4, "memory": 148.2 },
      "low_metrics": { "cpu": 12.1, "memory": 145.2 },
      "summary": {
        "performance_rating": "Good"
      }
    }
  ]
}
```

### All Conversations Overview
```http
GET /all-conversation-metrics
```

Summary of all conversations with individual chat counts and peak usage.

### System Metrics Snapshot
```http
GET /system-metrics
```

Current system resource usage snapshot.

## 🚀 **How to Use**

### 1. **Start the Server**
```bash
python render_start.py
```

### 2. **Test Individual Chat Metrics**
```bash
python test_individual_chat_metrics.py
```

This test script will:
- Send 4 different chat messages
- Show individual metrics for each
- Display conversation summary
- Test live metrics streaming

### 3. **Monitor Live Metrics**

**HTML Example:**
```html
<!DOCTYPE html>
<html>
<head><title>Live Aara Metrics</title></head>
<body>
<div id="metrics"></div>
<script>
const eventSource = new EventSource('http://localhost:8000/live-metrics');
eventSource.onmessage = function(event) {
    const metrics = JSON.parse(event.data);
    document.getElementById('metrics').innerHTML = 
        `CPU: ${metrics.system_cpu_percent}% | 
         Memory: ${metrics.process_memory_mb}MB`;
};
</script>
</body>
</html>
```

**cURL Example:**
```bash
curl -N -H "Accept: text/event-stream" http://localhost:8000/live-metrics
```

### 4. **Check Specific Conversation**
```bash
curl http://localhost:8000/conversation-metrics/my_skincare_chat
```

## 📊 **Example Console Output**

```
💬 CHAT METRICS [REQUEST_RECEIVED] - chat_1234567890
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Message: "I have oily skin and acne. What skincare routine..."
⏱️  Elapsed: 12ms
🔸 Current CPU: 25.4% | Peak: 25.4% | Low: 25.4%
🔸 Current Memory: 145.2MB | Peak: 145.2MB | Low: 145.2MB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 CHAT METRICS [WORKFLOW_START] - chat_1234567890
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Message: "I have oily skin and acne. What skincare routine..."
⏱️  Elapsed: 120ms
🔸 Current CPU: 42.1% | Peak: 42.1% | Low: 25.4%
🔸 Current Memory: 158.7MB | Peak: 158.7MB | Low: 145.2MB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 INDIVIDUAL CHAT COMPLETED - chat_1234567890
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Question: "I have oily skin and acne. What skincare routine..."
📝 Response Length: 245 chAaracters
⏱️  Total Duration: 1250ms
📊 Performance Rating: Good
🔥 CPU Range: 25.4% - 47.8%
💾 Memory Range: 145.2MB - 168.3MB
📈 Stages Tracked: 6
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🔧 **Performance Ratings**

- **Good**: Peak CPU < 70% AND Peak Memory < 500MB
- **High Usage**: Peak CPU ≥ 70% OR Peak Memory ≥ 500MB

## 💡 **Benefits**

1. **Individual Question Tracking**: See exactly how much each question costs in resources
2. **Performance Optimization**: Identify which types of questions use more resources
3. **Live Monitoring**: Watch real-time resource usage during deployment
4. **Conversation Analysis**: Understand resource patterns across conversations
5. **Deployment Debugging**: Quickly identify resource bottlenecks on Render or other platforms

## ⚡ **Quick Start**

```bash
# 1. Start server
python render_start.py

# 2. Send a chat (in another terminal)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What skincare routine for oily skin?", "conversation_id": "test"}'

# 3. Check metrics
curl http://localhost:8000/conversation-metrics/test

# 4. Watch live metrics
curl -N -H "Accept: text/event-stream" http://localhost:8000/live-metrics
```

Now every chat question gets **individual resource tracking** with **peak/low monitoring** and **live streaming capabilities**! 🎉 