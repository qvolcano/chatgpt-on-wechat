import os;
def default(query,context):
  process = os.popen('tail nohup.out')
  output = process.read()
  process.close()
  return output

