import asyncio
from mock_api.models.dag import Dag
from mock_api.models.task import Task
from mock_api.models.task_result import TaskResult
from mock_api.models.task_error import TaskError

# import async functions to add to DAG

# List of operations to perform
dag = Dag()

# Sample functions
async def process_double(value: int) -> TaskResult:
    await asyncio.sleep(1)  # Simulate async work
    if value < 0:
        raise ValueError("Value cannot be negative for doubling")
    return TaskResult(operation="double", result=value * 2)

async def process_square(value: int) -> TaskResult:
    await asyncio.sleep(1)
    return TaskResult(operation="square", result=value ** 2)

async def process_increment(value: int) -> TaskResult:
    await asyncio.sleep(1)
    return TaskResult(operation="increment", result=value + 1)


dag.add('process_double', process_double)
dag.add('process_square', process_square, 'process_double')
dag.add('process_increment', process_increment)