import os;
def default(query):
  process = os.popen('tail nohup.out')
  output = process.read()
  process.close()
  return output

