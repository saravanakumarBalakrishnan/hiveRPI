class ExceptionHandling(Exception):
    """Base class for other exceptions"""

    def __init__(self, value, context=None):
        print(value)
        if "[Errno 6] Device not configured" in value:
            print("TG Stick not connected")
            if context:
                self.skipScenario(context, value)
            exit()

        if "Error opening port" in value:
            print("TG Stick not connected")
            exit(context)
        if "unsupported operand type" in value:
            if context:
                self.skipScenario(context, value)

        if "TIMEOUT: sendCommand()" in value:
            if context:
                self.skipScenario(context, value)
            else:
                exit()
        if "'NoneType' object has no attribute 'close'" in value:
            print("No serial connection exists at the moment")

        if "AttributeError: 'MyApp' object has no attribute 'listDetailsZDump'" in value:
            print("Please select the device")

        if "list index out of range" in value:
            if context:
                self.skipScenario(context, value)

        if "'NoneType' object has no attribute 'children'" in value:
            print(value)

        if "[Errno 2] No such file or directory" in value:
            if context:
                self.skipScenario(context, value)
            else:
                exit()
        if "Config error" in value:
            if context:
                self.skipScenario(context, value)

    def skipScenario(self, context, value):
        context.strStepFailReason = str(value)
        context.scenario.skip()
        context.reporter.ReportEvent("Exception", str(value), "FAIL")
        context.reporter.ReportEvent("Traceback", str(context.tb).replace("\n","<br>"), "DONE")
