import os
import sys
import json

from jsonschema import Draft4Validator, RefResolver


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


def buildPath(seq):
  return '/'.join([str(x) for x in error.absolute_path])

API_VERSIONS = {
    'schema': [
        'catalog.json',
        'post.json',
        'thread.json',
    ]
}

TESTS = {
    'schema': {
        'catalog': [
            'test-catalog-vg'
        ]
    }
}

IsTTY = sys.stdout.isatty()
if sys.platform.startswith('win'):
  IsTTY = False

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
        sys.exit(1)

for version, files in TESTS.items():
  for filename, tests in files.items():
    schema_path = os.path.join(version, filename + '.json')
    for test in tests:
      test_path = os.path.join('tests', filename, test + '.json')
      console_write('Running test {}... '.format(test))

      schema = None
      with open(schema_path, 'r') as f:
        schema_data = json.load(f)
        rootdir = 'file:///' + os.path.abspath(version).replace('\\', '/') + '/'
        #print('Initializing schema {} from {}'.format(filename, rootdir))
        resolver = RefResolver(rootdir, None)
        schema = Draft4Validator(schema_data, resolver=resolver)

      test_data = None
      with open(test_path, 'r') as f:
        test_data = json.load(f)
        if not isinstance(test_data, (list, dict)):
          print('test_data = ' + test_data.__class__.__name__)

      firstError = True
      lastCtx = None
      for error in schema.iter_errors(test_data):
        if firstError:
          console_write("FAIL", Colors.FAIL)
          firstError = False
          print('')
        ctx = '{}#/{}'.format(test_path, buildPath(error.absolute_path))
        if ctx != lastCtx:
          print('  In {}:'.format(ctx))
          lastCtx = ctx
        print('    E: {}#/{} - {}'.format(error.schema['id'], '/'.join(error.schema_path), error.message.strip()))
        # print(error.validator_value)
      if firstError:
        console_write('OK!', Colors.OKGREEN)
