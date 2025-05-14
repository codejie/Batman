import threading

class InstanceBase(threading.Thread):
  def __init__(self, exit_event: threading.Event, **kwargs):
    super().__init__()
    self.exit_event = exit_event

  def run(self):
    pass

class Service:
  def __init__(self):
    self.exit_event = threading.Event()
    self.threads: list[threading.Thread] = [] # no name now

  def start(self):
    pass

  def run(self, target: callable, **kwargs):
    t = threading.Thread(target=target, kwargs=kwargs)
    self.threads.append(t)
    t.start()

  def run_instance(self, instance: InstanceBase, **kwargs):
    self.threads.append(instance)
    instance.start()

  def shutdown(self):
    self.exit_event.set()
    for t in self.threads:
      t.join()
    self.threads.clear()

app_service: Service = Service()