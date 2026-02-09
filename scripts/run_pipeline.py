import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import structlog

from dataforge.pipeline.executor import PipelineExecutor
from dataforge.pipeline.loader import PipelineLoader

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer(),
    ]
)


async def main():
    if len(sys.argv) < 2:
        print("Uso: python run_pipeline.py <pipeline_name>")
        sys.exit(1)

    pipeline_name = sys.argv[1]

    pipelines = PipelineLoader.load_from_file("config/pipelines.yaml")
    pipeline = next((p for p in pipelines if p["name"] == pipeline_name), None)

    if not pipeline:
        print(f"Pipeline '{pipeline_name}' não encontrado")
        sys.exit(1)

    PipelineLoader.validate_pipeline(pipeline)

    executor = PipelineExecutor()
    await executor.execute(pipeline)


if __name__ == "__main__":
    asyncio.run(main())
