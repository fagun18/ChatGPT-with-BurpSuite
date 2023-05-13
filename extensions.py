from burp import IBurpExtender
from burp import IHttpListener
from java.io import PrintWriter
from javax.swing import JPanel, JTextField, JButton, BoxLayout

class BurpExtender(IBurpExtender, IHttpListener):
    
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self._stdout = PrintWriter(callbacks.getStdout(), True)
        self._stderr = PrintWriter(callbacks.getStderr(), True)
        callbacks.setExtensionName("Custom Tab")
        callbacks.registerHttpListener(self)
        self.init_gui()

    def init_gui(self):
        self.panel = JPanel()
        self.panel.setLayout(BoxLayout(self.panel, BoxLayout.Y_AXIS))
        self.text_field = JTextField(25)
        self.button = JButton("Send Request", actionPerformed=self.send_request)
        self.panel.add(self.text_field)
        self.panel.add(self.button)
        self._callbacks.customizeUiComponent(self.panel)
        self._callbacks.addSuiteTab(self)
        
    def send_request(self, event):
        url = self.text_field.getText()
        self._stdout.println("Sending request to: " + url)
        request = self._helpers.buildHttpRequest(self._helpers.analyzeRequest(url).getUrl())
        response = self._callbacks.makeHttpRequest(request.getHost(), request.getPort(), False, request)
        self._stdout.println(self._helpers.bytesToString(response))
        
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        pass

    def getTabCaption(self):
        return "Custom Tab"

    def getUiComponent(self):
        return self.panel
