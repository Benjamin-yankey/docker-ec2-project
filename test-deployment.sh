#!/bin/bash

# Allow overriding the default host and port via command-line arguments
PORT=${1:-5000}
HOST=${2:-localhost}

echo "🧪 Testing Multi-Container Deployment"
echo "====================================="
echo "Target: http://$HOST:$PORT"
echo ""

# Counters for tracking test results
PASSED=0
FAILED=0

# Helper function to test a specific API endpoint and compare its HTTP status code
test_endpoint() {
    local name=$1
    local endpoint=$2
    local expected=$3
    
    echo -n "Testing $name... "
    # Perform a curl request and extract the HTTP status code
    response=$(curl -s -o /dev/null -w "%{http_code}" "http://$HOST:$PORT$endpoint")
    
    if [ "$response" == "$expected" ]; then
        echo "✅ PASSED"
        ((PASSED++))
    else
        echo "❌ FAILED (got $response, expected $expected)"
        ((FAILED++))
    fi
}

# Run tests for standard read-only endpoints
test_endpoint "Health Check" "/api/health" "200"
test_endpoint "Home Page" "/" "200"
test_endpoint "Get Users" "/api/users" "200"
test_endpoint "Stats" "/api/stats" "200"

echo ""
echo -n "Testing Create User... "
# Test user creation via a POST request
response=$(curl -s -X POST "http://$HOST:$PORT/api/users" \
    -H "Content-Type: application/json" \
    -d '{"name":"Test User","email":"test@example.com"}' \
    -w "%{http_code}" -o /dev/null)

if [ "$response" == "201" ]; then
    echo "✅ PASSED"
    ((PASSED++))
else
    echo "❌ FAILED"
    ((FAILED++))
fi

# Print the final test summary
echo ""
echo "📊 Test Results"
echo "==============="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

# Exit with an error code if any test failed
if [ $FAILED -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed"
    exit 1
fi
