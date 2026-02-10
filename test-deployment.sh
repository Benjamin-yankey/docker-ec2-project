#!/bin/bash

PORT=${1:-5000}
HOST=${2:-localhost}

echo "🧪 Testing Multi-Container Deployment"
echo "====================================="
echo "Target: http://$HOST:$PORT"
echo ""

PASSED=0
FAILED=0

test_endpoint() {
    local name=$1
    local endpoint=$2
    local expected=$3
    
    echo -n "Testing $name... "
    response=$(curl -s -o /dev/null -w "%{http_code}" "http://$HOST:$PORT$endpoint")
    
    if [ "$response" == "$expected" ]; then
        echo "✅ PASSED"
        ((PASSED++))
    else
        echo "❌ FAILED (got $response, expected $expected)"
        ((FAILED++))
    fi
}

test_endpoint "Health Check" "/api/health" "200"
test_endpoint "Home Page" "/" "200"
test_endpoint "Get Users" "/api/users" "200"
test_endpoint "Stats" "/api/stats" "200"

echo ""
echo -n "Testing Create User... "
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

echo ""
echo "📊 Test Results"
echo "==============="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed"
    exit 1
fi
