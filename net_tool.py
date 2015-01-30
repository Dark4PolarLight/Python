#!/usr/bin/env python2.7
#-*-coding: utf-8 -*-

import sys
import getopt
import socket
import subprocess

# define some global variables
listen = False
command = False
execute = ''
host = ''
port = 0


def usage():
  '''
  How to use this tools
  '''
  print 'Dark4PolarLight Net Tool'
  print 'Usage: d4plnet.py -t host -p port' 
  print '-t --target_host: host ip addr'
  print '-p --port: host port'
  print '-l --listen: listen on [host]:[port] for incoming connections'
  print '-c --command: initialize a command line'
  print '-e --execute: run a command'
  print '-h --help: help use this tools'


def args():
  '''
  Get command line arguments
  '''
  global listen
  global command
  global execute
  global host
  global port

  if len(sys.argv[1:]) == 0:
    usage()
    sys.exit(0)

  opts, args = getopt.getopt(sys.argv[1:], 't:p:lce:h', ['--target_host=', '--port=', '--listen', '--command', '--execute=', '--help'])

  for a, o in opts:
    if a in ('-t', '--target_host'):
      host = o
    if a in ('-p', '--port'):
      port = int(o)
    if a in ('-l', '--listen'):
      listen = True
    if a in ('-c', '--command'):
      command = True
    if a in ('-e', '--execute'):
      execute = o
    if a in ('-h', '--help'):
      usage()
      sys.exit(0)


def tcpcliSock(remote_host, remote_port):
  '''
  Client connect Server
  '''
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((remote_host, remote_port))

# Get shell command line
  if command:

    try:
      while True:
        date = raw_input('>> ')
        if not date:
          break
        client.send(date)
        date = client.recv(2048)
        print '> ', date
    except:
      print "OVER"
    client.close()

# set execute
  if len(execute) != 0:
    client.send(execute)
    date = client.recv(2048)
    print '> ', date
    client.close()
    

def tcpserSock(local_host, local_port):
  '''
  Create Server listening
  '''
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((local_host, local_port))
  server.listen(2)

  while True:
    tcpser, addr = server.accept()

    while True:
      date = tcpser.recv(2048)
      
      if not date:
        break

      process = subprocess.Popen(date, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
      output, err_output = process.communicate()
      
      if len(output) == 0 and len(err_output) == 0:
        tcpser.send('ok')
      elif len(output) == 0 and len(err_output) != 0:
        tcpser.send(err_output)
      else:
        tcpser.send(output)

  tcpser.close()


def main():
  args()

  if listen:
    tcpserSock(host, port)
  else:
    tcpcliSock(host, port)



if __name__ == '__main__':
  main()
