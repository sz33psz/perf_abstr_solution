from javax.swing import JTextArea, JFrame, JLabel, JScrollPane, ScrollPaneConstants
from javax.swing.event import DocumentListener
from java.awt import GridBagLayout, GridBagConstraints
from ResponseBuilder import process
from ResponsePostProcessor import JsonResponsePostProcessor
import sys


class MainWindow(object):
    def __init__(self):
        self.frame = JFrame('Hello, Jython!',
                            defaultCloseOperation=JFrame.EXIT_ON_CLOSE,
                            size=(400, 600))
        bag_layout = GridBagLayout()
        self.frame.layout = bag_layout
        grid_constraints = GridBagConstraints()

        format_1_string_label = JLabel("Format 1 string:")
        grid_constraints.weightx = 0.1
        grid_constraints.weighty = 0.1
        grid_constraints.gridy = 0
        grid_constraints.fill = GridBagConstraints.NONE
        self._add_component(format_1_string_label, bag_layout, grid_constraints)

        self.input_textbox = JTextArea()
        grid_constraints.weightx = 1
        grid_constraints.weighty = 1
        grid_constraints.gridy = 1
        grid_constraints.fill = GridBagConstraints.BOTH
        input_scroll_pane = JScrollPane(self.input_textbox)
        input_scroll_pane.verticalScrollBarPolicy = ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS
        self._add_component(input_scroll_pane, bag_layout, grid_constraints)

        output_string_label = JLabel("Output:")
        grid_constraints.weightx = 0.1
        grid_constraints.weighty = 0.1
        grid_constraints.gridy = 2
        grid_constraints.fill = GridBagConstraints.NONE
        self._add_component(output_string_label, bag_layout, grid_constraints)

        self.output_textbox = JTextArea()
        grid_constraints.weightx = 1
        grid_constraints.weighty = 1
        grid_constraints.gridy = 3
        grid_constraints.fill = GridBagConstraints.BOTH
        self.output_textbox.editable = False
        output_scroll_pane = JScrollPane(self.output_textbox)
        output_scroll_pane.verticalScrollBarPolicy = ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS
        self._add_component(output_scroll_pane, bag_layout, grid_constraints)

    def _add_component(self, component, layout, constraint):
        layout.setConstraints(component, constraint)
        self.frame.add(component)

    def show(self):
        self.frame.visible = True
        listener = InputTextDocumentListener(self.input_textbox, self.output_textbox)
        self.input_textbox.document.addDocumentListener(listener)


class InputTextDocumentListener(DocumentListener):
    def __init__(self, input_textbox, output_textbox):
        self.input_textbox = input_textbox
        self.output_textbox = output_textbox

    def _change_output(self):
        input_value = self.input_textbox.text
        self.output_textbox.text = "aaa"
        try:
            output_value = process(input_value, JsonResponsePostProcessor("  "))
            self.output_textbox.text = output_value
        except Exception:
            _, err, _ = sys.exc_info()
            self.output_textbox.text = str(err)


    def insertUpdate(self, event):
        self._change_output()

    def removeUpdate(self, event):
        self._change_output()

    def changedUpdate(self, event):
        self._change_output()
