#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://localhost:8001/categories"

request() {
  local description="$1"
  shift

  printf '\n========================================\n'
  printf ' %s\n' "$description"
  printf '========================================\n'

  curl -sS "$@" | jq .
  printf '\n'
}

# List all categories
request "List categories" \
  -X GET \
  "${BASE_URL}" \
  -H 'accept: application/json'

# Get a category by ID
request "Get category (ID: 1)" \
  -X GET \
  "${BASE_URL}/1" \
  -H 'accept: application/json'

# Create a category
request "Create category" \
  -X POST \
  "${BASE_URL}?name=Europe" \
  -H 'accept: application/json'

# Update a category
request "Update category (ID: 1)" \
  -X PATCH \
  "${BASE_URL}/1" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Europe",
    "countries": [
      "Estonia",
      "Latvia",
      "Lithuania"
    ]
  }'

# Delete a category
printf '\n========================================\n'
printf ' Delete category (ID: 1)\n'
printf '========================================\n'

curl -sS -o /dev/null -w 'HTTP Status: %{http_code}\n' \
  -X DELETE \
  "${BASE_URL}/1" \
  -H 'accept: */*'
