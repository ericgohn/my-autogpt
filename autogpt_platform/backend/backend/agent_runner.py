from backend.app import run_processes


def pre_agent():
    """
    Run all the processes before AgentServer(rest)
    """
    from backend.executor import DatabaseManager, Scheduler
    from backend.notifications import NotificationManager
    from backend.server.ws_api import WebsocketServer

    run_processes(
        DatabaseManager().set_log_level("warning"),
        Scheduler(),
        NotificationManager(),
        WebsocketServer(),
    )


def post_agent():
    """
    Run all the processes before AgentServer(rest)
    """
    from backend.executor import ExecutionManager
    from backend.server.rest_api import AgentServer

    run_processes(AgentServer(), ExecutionManager())
