import os
import sys
import json
from jsonschema import Draft4Validator


class Colors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'


def console_write(msg, color=None):
  global IsTTY
  if color and IsTTY:
    sys.stdout.write(color)
  sys.stdout.write(msg)
  if color and IsTTY:
    sys.stdout.write(Colors.ENDC)

API_VERSIONS = {
    'v1.0': [
        'catalog.json_schema',
        'post.json_schema',
        'thread.json_schema',
    ]
}

IsTTY = sys.stdout.isatty()
if sys.platform.startswith('win'):
  #print('Is Windows :( - Disabling colors.')
  IsTTY = False
#else:
#  print('Is not Windows.')
print('%s a TTY.' % ('Is' if IsTTY else 'Is not'))

for version, files in API_VERSIONS.items():
  for filename in files:
    path = os.path.join(version, filename)
    console_write('Validating {}... '.format(path))
    with open(path, 'r') as f:
      schema = json.load(f)
      o = Draft4Validator.check_schema(schema)
      if o is None:
        console_write('OK!', Colors.OKGREEN)
        print('')
        continue
      else:
        console_write('FAIL', Colors.FAIL)
        print('')
        print(repr(o))
