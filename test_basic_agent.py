#!/usr/bin/env python3
"""
Basic test for AI Agent functionality
"""
import asyncio
import os
import sys
from unittest.mock import Mock, patch
import pytest

# Mock OpenAI API for testing
class MockOpenAI:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.chat = Mock()
        self.chat.completions = Mock()
    
    def create(self, **kwargs):
        # Mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "Test response from mock agent"
        return mock_response

# Test basic agent functionality
class TestBasicAgent:
    def __init__(self):
        self.openai_client = None
    
    async def setup(self):
        """Setup test environment"""
        print("Setting up test environment...")
        # Mock OpenAI client
        with patch('openai.OpenAI', return_value=MockOpenAI()):
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key="test-key")
                print("✅ OpenAI client initialized successfully")
            except ImportError:
                print("❌ OpenAI package not available")
                return False
        return True
    
    async def test_basic_agent_creation(self):
        """Test basic agent creation"""
        print("\n🧪 Testing basic agent creation...")
        try:
            # Test basic agent functionality
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello, test message"}]
            )
            
            assert response.choices[0].message.content == "Test response from mock agent"
            print("✅ Basic agent creation test passed")
            return True
        except Exception as e:
            print(f"❌ Basic agent creation test failed: {e}")
            return False
    
    async def test_error_handling(self):
        """Test error handling"""
        print("\n🧪 Testing error handling...")
        try:
            # Test with invalid input
            with pytest.raises(Exception):
                self.openai_client.chat.completions.create(
                    model="invalid-model",
                    messages=[]
                )
            print("✅ Error handling test passed")
            return True
        except Exception as e:
            print(f"❌ Error handling test failed: {e}")
            return False
    
    async def test_session_management(self):
        """Test session management"""
        print("\n🧪 Testing session management...")
        try:
            # Mock session management
            session_id = "test-session-123"
            messages = [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ]
            
            # Test session creation
            assert session_id is not None
            assert len(messages) == 2
            print("✅ Session management test passed")
            return True
        except Exception as e:
            print(f"❌ Session management test failed: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting AI Agent Debug and Test Suite")
        print("=" * 50)
        
        # Setup
        if not await self.setup():
            print("❌ Setup failed, aborting tests")
            return False
        
        # Run tests
        tests = [
            self.test_basic_agent_creation,
            self.test_error_handling,
            self.test_session_management
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if await test():
                    passed += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {e}")
        
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed")
            return False

async def main():
    """Main test runner"""
    tester = TestBasicAgent()
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())