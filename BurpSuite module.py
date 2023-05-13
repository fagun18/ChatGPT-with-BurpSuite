import sys
from burp import IBurpExtender
from burp import IContextMenuFactory
from burp import ITab
import openai_secret_manager
import openai

class BurpExtender(IBurpExtender, ITab, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        callbacks.setExtensionName("OpenAI Integration")

        # Get API credentials from the OpenAI Secret Manager
        openai_secrets = openai_secret_manager.get_secret("openai")

        # Set up OpenAI API credentials
        openai.api_key = openai_secrets["api_key"]

        # Set up Burp Suite Tab
        self.tab = MyCustomTab()
        callbacks.addSuiteTab(self.tab)

        # Set up Context Menu
        callbacks.registerContextMenuFactory(self)

    def createMenuItems(self, invocation):
        menu_list = []
        menu_list.append(ContextMenuItem(self, invocation))
        return menu_list

class ContextMenuItem(IContextMenuFactory):
    def __init__(self, extender, invocation):
        self.extender = extender
        self.invocation = invocation

    def createMenuItems(self, invocation):
        self.context = invocation
        menu_list = []
        menu_list.append(JMenuItem("OpenAI Integration", actionPerformed=self.menuItemClicked))
        return menu_list

    def menuItemClicked(self, event):
        # Call OpenAI API
        response = openai.Completion.create(
            engine="davinci",
            prompt="Hello, World!",
            max_tokens=5
        )

        # Print response to console
        print(response)

class MyCustomTab(ITab):
    def __init__(self):
        self.panel = JPanel()
        self.text = JTextArea(20, 50)
        scroll = JScrollPane(self.text)
        self.panel.add(scroll)

    def getTabCaption(self):
        return "OpenAI Integration"

    def getUiComponent(self):
        return self.panel
