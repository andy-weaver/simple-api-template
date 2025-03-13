from __future__ import annotations

from graphlib import TopologicalSorter, CycleError
from typing import Callable, List, Dict, Union

from mock_api.dag import Dag, dag
from mock_api.models.task import Task
from mock_api.models.task_result import TaskResult
from mock_api.models.task_error import TaskError

CyclicDagError = TaskError(1, lambda e: f"DAG contains a cycle:\n{e}")

def _build_dag(dag: Dag) -> dict[str, set[str]]:
    graph = {task.name: set(task.dependencies) for task in tasks}
    try:
        ts = TopologicalSorter(graph)
        ts.prepare()
        return graph
    except CycleError as e:
        return CyclicDagError(e)
    except Exception as e:
        return TaskError(-999, lambda e: "Unknown error in _build_dag:\n")


async def run_tasks_concurrently(dag: Dag, value: int) -> dict[str, TaskResult | TaskError]:
    """Build a dependency graph and run tasks in batches.
    - Tasks whose dependencies have failed are skipped and marked with a TaskError.
    - If a task fails during execution, its exception is caught and transformed into a TaskError.
    """
    graph = _build_dag(dag)

    results: Dict[str, Union[TaskResult, TaskError]] = {}
    while ts.is_active():
        ready = list(ts.get_ready())
        tasks_to_run = []
        tasks_to_skip = []
        for task_name in ready:
            task_obj = next(task for task in tasks if task.name == task_name)
            # Check if any dependency failed.
            failed_deps = [dep for dep in task_obj.dependencies if isinstance(results.get(dep), TaskError)]
            if failed_deps:
                tasks_to_skip.append(task_obj)
            else:
                tasks_to_run.append(task_obj)

        # Mark tasks that must be skipped due to dependency failure.
        for task_obj in tasks_to_skip:
            failed_deps = [dep for dep in task_obj.dependencies if isinstance(results.get(dep), TaskError)]
            results[task_obj.name] = TaskError(
                error_code=424,
                error_message=f"Dependency failure in: {', '.join(failed_deps)}"
            )
            ts.done(task_obj.name)

        # Run eligible tasks concurrently.
        if tasks_to_run:
            coroutines = [task_obj.func(value) for task_obj in tasks_to_run]
            batch_results = await asyncio.gather(*coroutines, return_exceptions=True)
            for task_obj, res in zip(tasks_to_run, batch_results):
                if isinstance(res, Exception):
                    results[task_obj.name] = TaskError(error_code=500, error_message=str(res))
                else:
                    results[task_obj.name] = res
                ts.done(task_obj.name)
    return results