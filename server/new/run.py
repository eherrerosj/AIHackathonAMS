import os
import time
import redis
import tasks
import configparser

from model import Model

from flask import Flask, request, json
from flask_sockets import Sockets

from rq import Queue
from rq.job import Job
from worker import conn

from sys import stdout
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

current_dir = os.path.dirname(__file__)
config_dir = os.path.join(current_dir, 'app.conf')
config = configparser.ConfigParser()
config.read(config_dir)

app = Flask(__name__)
sockets = Sockets(app)

redis_host = config.get('ai', 'redis-host')
redis_port = config.get('ai', 'redis-port')
server_port = int(config.get('ai', 'server-port'))

redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
q = Queue(connection=redis_conn)


model = Model()

# Serve landing page here TODO add landing page
@app.route("/")
def index():
    return "Oh hello there!"


# Serve dashboard page here TODO add dashboard page
@app.route("/dash")
def dash():
    return "Quite dashing!"


@sockets.route('/check')
def check(ws):
    while not ws.closed:
        message = ws.receive()
        if message is not None:
            js = (json.loads(message))

            job = q.enqueue_call(func=tasks.check_url, args=(js,model,), result_ttl=5000)

            while not job.is_finished:
                time.sleep(0.5)

            result = job.result
            
            # print(dir(job))

            # reult = job.wait_result(timeout=360)
            
            
            # res = json.dumps({ 'result': job.get_id() })
            ws.send(result)


# Not used anymore :(
@sockets.route('/result')
def check(ws):
    while not ws.closed:
        message = ws.receive()
        if message is not None:
            js = (json.loads(message))

            job_key = js['job_key']
            job = Job.fetch(job_key, connection=conn)

            if job.is_finished:
                res = json.dumps({ 'result': str(job.result) })
            else:
                res = json.dumps({ 'result': None })
            ws.send(res)


if __name__ == "__main__":
    print('Starting server..')
    pywsgi.WSGIServer(('', server_port), app, log=stdout, handler_class=WebSocketHandler).serve_forever()
