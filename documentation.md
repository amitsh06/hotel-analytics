# Hotel Analytics System - Health Check Documentation

## Overview
The Health Check endpoint provides real-time monitoring of system health and performance metrics. It allows system administrators and developers to verify that all components are functioning properly and to diagnose issues when they arise.

## psutil Integration
The system uses the `psutil` library to monitor system resources such as CPU usage, memory usage, and disk space. This integration allows the API to provide accurate system metrics that can be used for performance monitoring and alerting.

## Endpoint Details

### URL
```
GET /health
```

### Response Format
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

### Response Fields

| Field | Description |
|-------|-------------|
| `status` | Overall health status: "healthy", "degraded", or "unhealthy" |
| `timestamp` | Unix timestamp when the health check was performed |
| `system.cpu_usage_percent` | Current CPU usage as a percentage |
| `system.memory_usage_percent` | Current memory usage as a percentage |
| `system.disk_usage_percent` | Current disk usage as a percentage |
| `components.analytics_engine` | Status of the analytics engine component |
| `components.database` | Status of the database component |
| `components.llm_service` | Status of the LLM service component |
| `performance.avg_response_time_seconds` | Average response time for queries |
| `performance.successful_queries` | Count of successful queries |
| `performance.failed_queries` | Count of failed queries |
| `performance.total_queries` | Total number of queries processed |

## Implementation Details

The health check endpoint uses the `psutil` library to gather system metrics:

```python
# System metrics
cpu_usage = psutil.cpu_percent(interval=0.1)
memory_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage('/').percent
```

The endpoint also checks if the analytics engine is functioning properly by verifying that the dataframe has been loaded:

```python
# Check if analytics module is working
analytics_working = hasattr(analytics, "df") and len(analytics.df) > 0
```

Performance metrics are collected throughout the system's operation and can be accessed through this endpoint to monitor system performance over time.

## Error Handling

If an error occurs during the health check, the endpoint will return a degraded status with error details:

```json
{
  "status": "degraded",
  "error": "Error message details",
  "timestamp": 1692725956.9512255
}
```

## Use Cases

1. **Monitoring**: Regular polling of this endpoint can be used for system monitoring and alerting.
2. **Diagnostics**: When issues arise, this endpoint can provide insight into which component might be failing.
3. **Performance Tracking**: The performance metrics can be collected over time to identify trends and potential issues.
4. **Load Testing**: During load testing, this endpoint can provide real-time feedback on system resource usage.

## Integration with Monitoring Systems

This health check endpoint can be integrated with monitoring systems like Prometheus, Grafana, or custom dashboards to provide real-time visibility into system health. 