#!/usr/bin/env python3
"""
Automated test for knowledge extraction flow
Simulates a user conversation without requiring manual input
"""

import requests
import json
import uuid
from typing import Dict, Any

API_URL = "http://localhost:8000"

# Test user ID (generate a valid UUID)
TEST_USER_ID = str(uuid.uuid4())

def log(message: str):
    """Pretty print log messages"""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}")

def log_response(response: requests.Response):
    """Log HTTP response details"""
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return data
    except:
        print(f"Response: {response.text}")
        return None

def test_conversation_flow():
    """Simulate complete conversation flow"""

    log("TEST 1: Start Conversation")
    response = requests.post(
        f"{API_URL}/conversation/start",
        json={"user_id": TEST_USER_ID}
    )
    start_data = log_response(response)

    if not start_data or not start_data.get("success"):
        print("❌ Failed to start conversation")
        return False

    conversation_id = start_data.get("conversation_id", TEST_USER_ID)
    print(f"✅ Conversation started: {conversation_id}")

    # Build conversation history
    conversation_history = [
        {"role": "assistant", "content": start_data["question"]}
    ]

    # Simulated user responses
    user_responses = [
        "I worked as a consultant helping organizations with graphic design and video editing.",
        "I did this from January 2020 to December 2023 at Creative Solutions Inc.",
        "I'm skilled in Adobe Photoshop, Premiere Pro, and Figma.",
        "I increased client enrollment by 40% through better storytelling.",
        "I also built a mobile app for tracking design projects using React Native."
    ]

    # Send each response
    for i, user_response in enumerate(user_responses, 1):
        log(f"TEST 2.{i}: Send User Response")
        print(f"User: {user_response}")

        conversation_history.append({"role": "user", "content": user_response})

        response = requests.post(
            f"{API_URL}/conversation/continue",
            json={
                "conversation_id": conversation_id,
                "user_response": user_response,
                "conversation_history": conversation_history
            }
        )

        continue_data = log_response(response)

        if continue_data and continue_data.get("success"):
            next_question = continue_data.get("next_question", "")
            if next_question:
                conversation_history.append({"role": "assistant", "content": next_question})
                print(f"✅ AI: {next_question}")
        else:
            print(f"⚠️ Continue failed at response {i}")

    log("TEST 3: End Conversation & Extract Knowledge")
    print(f"Total messages in conversation: {len(conversation_history)}")

    response = requests.post(
        f"{API_URL}/conversation/end",
        json={
            "conversation_id": conversation_id,
            "user_id": TEST_USER_ID,
            "conversation_history": conversation_history
        }
    )

    end_data = log_response(response)

    if not end_data:
        print("❌ Failed to end conversation")
        return False

    if end_data.get("success"):
        facts_extracted = end_data.get("facts_extracted", 0)
        print(f"✅ Extracted {facts_extracted} facts")
        print(f"   Entities: {json.dumps(end_data.get('entities', []), indent=2)}")
    else:
        print(f"❌ End conversation failed: {end_data.get('detail', 'Unknown error')}")
        return False

    log("TEST 4: Fetch Pending Facts")
    response = requests.get(f"{API_URL}/knowledge/pending/{TEST_USER_ID}")
    pending_data = log_response(response)

    if not pending_data:
        print("❌ Failed to fetch pending facts")
        return False

    entities = pending_data.get("entities", [])
    print(f"✅ Found {len(entities)} pending entities")

    if len(entities) == 0:
        print("⚠️ No entities found! Knowledge extraction may have failed")
        return False

    log("TEST 5: Confirm Facts")
    entity_ids = [e["id"] for e in entities]

    response = requests.post(
        f"{API_URL}/knowledge/confirm",
        json={
            "user_id": TEST_USER_ID,
            "entity_ids": entity_ids
        }
    )

    confirm_data = log_response(response)

    if confirm_data and confirm_data.get("success"):
        print(f"✅ Confirmed {confirm_data.get('confirmed_count', 0)} entities")
    else:
        print("❌ Failed to confirm entities")
        return False

    log("TEST 6: Fetch Confirmed Knowledge")
    response = requests.get(f"{API_URL}/knowledge/confirmed/{TEST_USER_ID}")
    confirmed_data = log_response(response)

    if confirmed_data:
        confirmed_entities = confirmed_data.get("entities", [])
        print(f"✅ Knowledge base has {len(confirmed_entities)} confirmed entities")

        # Show breakdown by type
        by_type = confirmed_data.get("grouped_by_type", {})
        for entity_type, entities in by_type.items():
            if entities:
                print(f"   - {entity_type}: {len(entities)}")

    log("TEST 7: Get Summary Stats")
    response = requests.get(f"{API_URL}/knowledge/summary/{TEST_USER_ID}")
    summary_data = log_response(response)

    if summary_data:
        print(f"✅ Summary:")
        print(f"   Total: {summary_data.get('total', 0)}")
        print(f"   Confirmed: {summary_data.get('confirmed', 0)}")
        print(f"   Pending: {summary_data.get('pending', 0)}")

    log("✅ ALL TESTS PASSED!")
    print(f"\nTest User ID: {TEST_USER_ID}")
    print("You can inspect this user's data in Supabase")

    return True

def test_direct_extraction():
    """Test the extraction service directly"""
    log("BONUS TEST: Direct Extraction API")

    test_text = """
    I worked as a Senior Software Engineer at Google from 2018 to 2023.
    I specialized in Python, React, and PostgreSQL.
    I built a customer analytics platform that served 10 million users.
    I graduated from MIT in 2017 with a degree in Computer Science.
    """

    response = requests.post(
        f"{API_URL}/knowledge/extract",
        json={
            "user_id": TEST_USER_ID,
            "content": test_text,
            "source": "manual_entry"
        }
    )

    extraction_data = log_response(response)

    if extraction_data and extraction_data.get("success"):
        entities = extraction_data.get("entities", [])
        print(f"✅ Extracted {len(entities)} entities from text")
        for entity in entities:
            print(f"   - {entity['entity_type']}: {entity['title']}")
    else:
        print("❌ Direct extraction failed")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  RESUMAKER KNOWLEDGE FLOW TEST")
    print("="*60)
    print(f"\nAPI URL: {API_URL}")
    print(f"Test User ID: {TEST_USER_ID}")

    try:
        # Run main flow test
        success = test_conversation_flow()

        # Run bonus direct extraction test
        # test_direct_extraction()

        if success:
            print("\n" + "🎉 "*20)
            print("\nALL TESTS PASSED! Knowledge extraction is working.")
            print("\n" + "🎉 "*20)
        else:
            print("\n" + "❌ "*20)
            print("\nTESTS FAILED! Check errors above.")
            print("\n" + "❌ "*20)

    except Exception as e:
        print(f"\n❌ TEST CRASHED: {e}")
        import traceback
        traceback.print_exc()
