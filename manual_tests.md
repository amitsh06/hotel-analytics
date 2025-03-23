# Manual Test Cases for Hotel Analytics API

This document provides a set of manual test cases to validate the functionality of the Hotel Analytics API. These tests should be performed after any significant changes to the system.

## Prerequisites
- Server is running on localhost:8000
- Test data is loaded correctly

## Basic API Tests

### Test Case 1: Health Check Endpoint
**Objective**: Verify that the health check endpoint returns the correct status and system metrics.

**Steps**:
1. Send a GET request to `/health`
2. Verify that the response status code is 200
3. Verify that the response contains the following fields:
   - `status` (should be "healthy")
   - `timestamp`
   - `system` with CPU, memory, and disk usage
   - `components` with status of key system components
   - `performance` metrics

**Expected Response Format**:
```json
{
  "status": "healthy",
  "timestamp": 1692725956.9512255,
  "system": {
    "cpu_usage_percent": 17.9,
    "memory_usage_percent": 83.3,
    "disk_usage_percent": 67.6
  },
  "components": {
    "analytics_engine": "healthy",
    "database": "healthy",
    "llm_service": "healthy"
  },
  "performance": {
    "avg_response_time_seconds": 0,
    "successful_queries": 0,
    "failed_queries": 0,
    "total_queries": 0
  }
}
```

### Test Case 2: Root Endpoint
**Objective**: Verify that the root endpoint returns a welcome message.

**Steps**:
1. Send a GET request to `/`
2. Verify that the response status code is 200
3. Verify that the response contains a welcome message

**Expected Response Format**:
```json
{
  "message": "Welcome to the Hotel Analytics API!"
}
```

## Analytics Tests

### Test Case 3: Generate Analytics Report
**Objective**: Verify that the analytics endpoint generates a comprehensive report.

**Steps**:
1. Send a POST request to `/analytics`
2. Verify that the response status code is 200
3. Verify that the response contains booking summary, seasonal analysis, guest demographics, and financial insights

**Expected Response Format**:
Should match the format described in the API documentation with realistic values.

## Question Answering Tests

### Test Case 4: Basic Question
**Objective**: Verify that the system can answer a simple question about the data.

**Steps**:
1. Send a POST request to `/ask` with the following JSON body:
   ```json
   {
     "text": "What is the average daily rate?"
   }
   ```
2. Verify that the response status code is 200
3. Verify that the response contains a reasonable answer about the average daily rate, with confidence and sources

### Test Case 5: Complex Question
**Objective**: Verify that the system can answer a more complex question requiring analysis.

**Steps**:
1. Send a POST request to `/ask` with the following JSON body:
   ```json
   {
     "text": "What months have the highest booking rates and why?"
   }
   ```
2. Verify that the response status code is 200
3. Verify that the response contains a detailed analysis of booking rates by month with explanations

### Test Case 6: Out-of-Domain Question
**Objective**: Verify that the system handles questions outside its domain appropriately.

**Steps**:
1. Send a POST request to `/ask` with the following JSON body:
   ```json
   {
     "text": "What is the weather like in Bermuda?"
   }
   ```
2. Verify that the response status code is 200
3. Verify that the response indicates the question is outside the scope of the hotel booking data

## Error Handling Tests

### Test Case 7: Invalid Request Format
**Objective**: Verify that the system handles invalid requests appropriately.

**Steps**:
1. Send a POST request to `/ask` with the following JSON body:
   ```json
   {
     "invalid_field": "What is the average daily rate?"
   }
   ```
2. Verify that the response status code is 400 (Bad Request)
3. Verify that the response contains an error message

### Test Case 8: Internal Error Simulation
**Objective**: Verify that the system handles internal errors gracefully.

**Steps**:
1. (This may require temporary modification of code) Introduce a deliberate error in the analytics engine
2. Send a POST request to `/analytics`
3. Verify that the response status code is 500 (Internal Server Error)
4. Verify that the response contains an error message
5. Check logs for appropriate error reporting

## Load Testing

### Test Case 9: Multiple Concurrent Requests
**Objective**: Verify that the system can handle multiple concurrent requests.

**Steps**:
1. Use a tool like Apache Bench or wrk to send 10 concurrent requests to the `/health` endpoint
2. Verify that all requests complete successfully
3. Check the response times and ensure they are within acceptable limits

### Test Case 10: Sustained Load
**Objective**: Verify that the system can handle sustained load.

**Steps**:
1. Use a tool to send 100 requests over 60 seconds to the `/ask` endpoint with a mix of questions
2. Verify that all requests complete successfully
3. Check the response times and ensure they do not degrade significantly over time
4. Check system resource usage during the test

## Test Results Reporting

After completing the tests, document the results including:
- Test date and time
- Environment details (OS, Python version, etc.)
- Test results (Pass/Fail)
- Any observations or issues found
- Performance metrics
- Recommendations for improvements

A template for reporting:

```
Test Date: YYYY-MM-DD HH:MM
Environment: Windows 10, Python 3.10.4
Tester: [Your Name]

Results:
- Test Case 1: PASS
- Test Case 2: PASS
- Test Case 3: PASS
- Test Case 4: PASS
- Test Case 5: FAIL - Explanation not detailed enough
- Test Case 6: PASS
- Test Case 7: PASS
- Test Case 8: PASS
- Test Case 9: PASS - Avg response time: 120ms
- Test Case 10: PASS - Max response time: 350ms

Observations:
[Any notable observations]

Recommendations:
[Recommendations for improving the system]
``` 