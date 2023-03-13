import os;
def default(query,context):
  process = os.popen('git pull -q -v') # return file
  output = process.read()
  process.close()
  return output
