import os
import re
import sys
import argparse
import tempfile
import subprocess
from tqdm import tqdm
from pathlib import Path
from typing import Optional

from backends import get_backend
from actions import ActionRunner

base_dir = Path(__file__).resolve().parent
temp_dir = base_dir / '../temp'
temp_dir.mkdir(parents=True, exist_ok=True)
context_file = os.path.join(temp_dir, 'context.txt')
_env = os.environ.copy()
_env['TORCH_CPP_LOG_LEVEL'] = 'ERROR'


class Agent:
    def __init__(self, backend: str, max_tokens: int):
        self.backend = get_backend()
        self.actions = ActionRunner()
        self.max_tokens = max_tokens
    
    def response(self, text: str, context: str = '') -> str:
        prompt = f"""Information:
{self.actions.desc()}

Context:
{context}

Answer:
{text}
"""
        return self.backend.get_response(prompt, self.max_tokens, stream_print=True)
    
    def maybe_take_action(self, text: str) -> str:
        res = self.actions(text)
        if res:
            return res
        else:
            return ''
    
    def run(self, text: str):
        resp = self.response(text)
        action_resp = self.maybe_take_action(resp)
        self.response(text, )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Code Agent")
    parser.add_argument("--model", type=str, default='claude-opus-4.6')
    parser.add_argument("--max_tokens", type=int, default=65536)
    parser.add_argument("--input", type=str, default='None')
    args = parser.parse_args()
    agent = Agent(args.model, max_tokens=args.max_tokens)
    with open(args.input.strip(), 'r') as f:
        text = f.read()
    agent.response(text)
