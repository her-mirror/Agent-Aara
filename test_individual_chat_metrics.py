#!/usr/bin/env python3
"""
Test script for Individual Chat Metrics System
Demonstrates the new per-chat resource monitoring with peak/low tracking
"""

import requests
import time
import json

# Configure your API endpoint
API_BASE = "http://localhost:8000"

def test_individual_chat_metrics():
    """Test the individual chat metrics system"""
    
    print("🧪 Testing Individual Chat Metrics System")
    print("=" * 60)
    
    # Test conversation ID
    conversation_id = f"test_metrics_{int(time.time())}"
    
    # Test messages with different complexity
    test_messages = [
        "Hello Ara! How are you?",
        "I have oily skin and acne. What skincare routine do you recommend?",
        "Can you suggest specific products for combination skin with sensitive areas?",
        "Based on my previous question about skincare, recommend some affordable serums."
    ]
    
    print(f"📞 Starting conversation: {conversation_id}")
    print(f"📝 Testing {len(test_messages)} messages\n")
    
    for i, message in enumerate(test_messages, 1):
        print(f"📨 Message {i}: {message}")
        print("-" * 50)
        
        # Send chat request
        try:
            response = requests.post(f"{API_BASE}/chat", json={
                "message": message,
                "conversation_id": conversation_id,
                "chat_history": []
            })
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract performance summary
                perf = data["metadata"]["performance_summary"]
                
                print(f"✅ Response received!")
                print(f"⏱️  Duration: {perf['total_duration_ms']}ms")
                print(f"🔥 CPU Range: {perf['low_cpu_percent']}% - {perf['peak_cpu_percent']}%")
                print(f"💾 Memory Range: {perf['low_memory_mb']:.1f}MB - {perf['peak_memory_mb']:.1f}MB")
                print(f"📊 Rating: {perf['performance_rating']}")
                print(f"📈 Stages: {perf['stages_tracked']}")
                print()
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
        
        time.sleep(1)  # Brief pause between requests
    
    # Get conversation metrics summary
    print("\n📊 Getting Conversation Metrics Summary")
    print("=" * 60)
    
    try:
        metrics_response = requests.get(f"{API_BASE}/conversation-metrics/{conversation_id}")
        
        if metrics_response.status_code == 200:
            metrics_data = metrics_response.json()
            
            print(f"📊 Conversation ID: {conversation_id}")
            print(f"💬 Total Chats: {metrics_data['total_chats']}")
            print(f"⏱️  Total Duration: {metrics_data['aggregate_stats']['total_duration_ms']}ms")
            print(f"⏱️  Average Duration: {metrics_data['aggregate_stats']['average_duration_ms']}ms")
            print(f"🔥 Peak CPU: {metrics_data['aggregate_stats']['peak_cpu_overall']}%")
            print(f"💾 Peak Memory: {metrics_data['aggregate_stats']['peak_memory_overall']}MB")
            
            print("\n📈 Individual Chat Details:")
            for i, chat in enumerate(metrics_data['individual_chats'], 1):
                print(f"  Chat {i}: {chat['total_duration_ms']}ms | "
                      f"CPU: {chat['summary']['cpu_range']} | "
                      f"Memory: {chat['summary']['memory_range']} | "
                      f"Rating: {chat['summary']['performance_rating']}")
        else:
            print(f"❌ Error getting metrics: {metrics_response.status_code}")
            
    except Exception as e:
        print(f"❌ Metrics request failed: {e}")

def test_live_metrics():
    """Test live metrics streaming"""
    print("\n🔴 Testing Live Metrics Stream")
    print("=" * 60)
    print("📡 Connecting to live metrics stream...")
    print("(This will show 10 seconds of live metrics)")
    
    try:
        response = requests.get(f"{API_BASE}/live-metrics", stream=True)
        
        if response.status_code == 200:
            print("✅ Connected! Streaming live metrics:\n")
            
            start_time = time.time()
            for line in response.iter_lines():
                if time.time() - start_time > 10:  # Stop after 10 seconds
                    break
                    
                if line and line.decode().startswith('data: '):
                    data_str = line.decode()[6:]  # Remove 'data: ' prefix
                    try:
                        metrics = json.loads(data_str)
                        if 'error' not in metrics:
                            print(f"🖥️  CPU: {metrics['system_cpu_percent']}% | "
                                  f"Memory: {metrics['process_memory_mb']:.1f}MB | "
                                  f"Time: {metrics['timestamp']}")
                    except json.JSONDecodeError:
                        pass
                        
            print("\n📡 Live stream test completed!")
        else:
            print(f"❌ Error connecting to live stream: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Live stream test failed: {e}")

def test_system_metrics():
    """Test system metrics endpoint"""
    print("\n🖥️  Testing System Metrics Endpoint")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE}/system-metrics")
        
        if response.status_code == 200:
            data = response.json()
            metrics = data["metrics"]
            
            print("✅ System Metrics Retrieved:")
            print(f"🔸 System CPU: {metrics['system_cpu_percent']}%")
            print(f"🔸 System Memory: {metrics['system_memory_used_mb']:.1f}MB / {metrics['system_memory_total_mb']:.1f}MB ({metrics['system_memory_percent']}%)")
            print(f"🔸 Process Memory: {metrics['process_memory_mb']:.1f}MB")
            print(f"🔸 Process CPU: {metrics['process_cpu_percent']}%")
            print(f"🔸 Timestamp: {metrics['timestamp']}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ System metrics test failed: {e}")

def main():
    """Run all tests"""
    print("🚀 Individual Chat Metrics Test Suite")
    print("=" * 60)
    print("This will test:")
    print("1. Individual chat metrics tracking with peak/low values")
    print("2. Live metrics streaming")
    print("3. System metrics endpoint")
    print("4. Conversation metrics aggregation")
    print()
    
    # Check if server is running
    try:
        health_response = requests.get(f"{API_BASE}/health")
        if health_response.status_code != 200:
            print("❌ Server not responding. Make sure to start the API server first:")
            print("   python render_start.py")
            return
    except:
        print("❌ Cannot connect to server. Make sure to start the API server first:")
        print("   python render_start.py")
        return
    
    print("✅ Server is running. Starting tests...\n")
    
    # Run tests
    test_system_metrics()
    test_individual_chat_metrics()
    test_live_metrics()
    
    print("\n🎉 All tests completed!")
    print("\n💡 API Endpoints Available:")
    print(f"   🔗 Live Metrics: {API_BASE}/live-metrics")
    print(f"   🔗 System Metrics: {API_BASE}/system-metrics")
    print(f"   🔗 All Conversations: {API_BASE}/all-conversation-metrics")
    print(f"   🔗 Specific Conversation: {API_BASE}/conversation-metrics/{{conversation_id}}")
    print(f"   🔗 Chat: {API_BASE}/chat")

if __name__ == "__main__":
    main() 