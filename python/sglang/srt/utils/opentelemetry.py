"""
OpenTelemetry configuration for SGLang HTTP server.
"""

import os
from typing import Optional

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentation
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

def setup_opentelemetry(
    service_name: str = "sglang-server",
    otlp_endpoint: Optional[str] = None,
    otlp_headers: Optional[dict] = None,
) -> None:
    """
    Set up OpenTelemetry instrumentation for the FastAPI server.
    
    Args:
        service_name: Name of the service for tracing
        otlp_endpoint: OTLP endpoint URL (e.g. "http://localhost:4317")
        otlp_headers: Headers for OTLP exporter (e.g. {"Authorization": "Bearer token"})
    """
    # Get OTLP endpoint from environment if not provided
    if otlp_endpoint is None:
        otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    
    # Get OTLP headers from environment if not provided
    if otlp_headers is None:
        auth_token = os.getenv("OTEL_EXPORTER_OTLP_HEADERS")
        if auth_token:
            otlp_headers = {"Authorization": auth_token}
        else:
            otlp_headers = {}

    # Create a tracer provider
    resource = Resource.create({
        "service.name": service_name,
    })
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # Create and add the OTLP exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint=otlp_endpoint,
        headers=otlp_headers,
    )
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    return provider 