from datetime import datetime
from graphs.health_monitoring_flow import graph
from rich.console import Console
from rich.panel import Panel
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import csv
import io
import json
import asyncio

console = Console()
app = FastAPI()

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return StreamingResponse(
            (line async for line in error_stream("Only .csv files are allowed")), 
            media_type="text/event-stream"
        )

    content = await file.read()
    decoded = content.decode("utf-8")
    csv_reader = csv.DictReader(io.StringIO(decoded))
    rows = [row for row in csv_reader]

    async def stream_patients():
        for idx, sensor_data in enumerate(rows, 1):
            console.rule(f"🧑 Patient #{idx} — {sensor_data['device_id']}", style="bold green")
            output = graph.invoke({"input": sensor_data})

            response_data = {
                "patient_index": idx,
                "device_id": sensor_data["device_id"],
                "analysis": output["health_report"]["llm_analysis"],
                "reason": output["alert_result"].get("reason"),
                "notify": output["alert_result"].get("notify"),
                "message": "ALERT TRIGGERED" if output["alert_result"]["raise_alert"] else "Reminder"
            }

            # Simulate real-time delay (optional)
            await asyncio.sleep(0.5)

            # Yield Server-Sent Event formatted message
            yield f"data: {json.dumps(response_data)}\n\n"

    return StreamingResponse(stream_patients(), media_type="text/event-stream")

async def error_stream(message: str):
    yield f"data: {json.dumps({'error': message})}\n\n"
