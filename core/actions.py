import os
import re
import inspect


def calculator(args: str) -> str:
    """
    Directly outputs Python-style calculation results
    """
    result = eval(args)
    return str(result)


GLOBAL_ACTIONS = [
    calculator,
]


class ActionRunner:
    def __init__(self):
        self.pattern = r'\[\[\[(.*?)\]\]\]<<<(.*?)>>>'
        global GLOBAL_ACTIONS
        self.actions = {}
        for function in GLOBAL_ACTIONS:
            name = str(function.__name__)
            desc = str(inspect.getsource(function))
            self.actions[name] = {
                'name': name,
                'desc': desc,
                'func': function
            }
    
    def __call__(self, text: str) -> bool:
        m = re.match(self.pattern, text)
        if m:
            action_name = m.group(1)
            action_args = m.group(2)
            return self.actions[action_name]['func'](action_args)
        return None

    def desc(self) -> str:
        text_head = """Output [[[$ACTION]]]<<<$ARGS>>> to indicate that an action is required.
Below are the available $ACTION options along with their descriptions and code:\n\n"""
        text_actions = []
        for key, value in self.actions.items():
            text_actions.append(
                f"$ACTION={key}\n{value['desc']}"
            )
        text_actions = '\n'.join(text_actions)
        return text_head + text_actions


if __name__ == '__main__':
    action_runner = ActionRunner()
    print(action_runner.desc())
