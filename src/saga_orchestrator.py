"""
Saga Orchestrator
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import config
from flask import Flask, jsonify, request
from controllers.order_saga_controller import OrderSagaController
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

app = Flask(__name__)

# TODO: Indiquez un nom pertinent à votre service
resource = Resource.create({
    "service.name": "saga-orchestrator",
   "service.version": "1.0.0"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Indiquez l'endpoint Jaeger (hostname dans Docker)
otlp_exporter = OTLPSpanExporter(
   endpoint="http://jaeger:4317",
   insecure=True
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Automatic Flask instrumentation
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.get('/health-check')
def health():
    """ Return OK if app is up and running """
    return jsonify({'status': 'ok'})

@app.post('/saga/order')
def saga_order():
    """ Start order saga """
    with tracer.start_as_current_span("saga.orchestrator.saga_order"):
        order_saga_controller = OrderSagaController()
        result = order_saga_controller.run(request)

        if result["status"] == "OK":
            return jsonify(result), 200
        else:
            return jsonify(result), 500

# Start Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.FLASK_PORT)
