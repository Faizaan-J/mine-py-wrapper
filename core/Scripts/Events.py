import Logger

class Event:
    def __init__(self, event_name: str):
        self._listeners = []
        self.event_name = event_name
        self.enabled = True

    def subscribe(self, func: callable):
        if not hasattr(self, "_listeners"):
            self._listeners = []
        self._listeners.append(func)

    def unsubscribe(self, func: callable):
        if hasattr(self, "_listeners") and func in self._listeners:
            self._listeners.remove(func)

    def invoke_event(self, *args, **kwargs):
        if not self.enabled:
            Logger.Log(Logger.LogLevel.WARNING, f"Event {self.event_name} is disabled; skipping invocation.")
            return
        
        for listener in getattr(self, "_listeners", []):
            try:
                listener(*args, **kwargs)
            except Exception as e:
                Logger.Log(Logger.LogLevel.ERROR, f"Event error: {e}")

    def clear_listeners(self):
        if hasattr(self, "_listeners"):
            self._listeners.clear()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False