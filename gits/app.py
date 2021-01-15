import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from flask_cors import CORS, cross_origin #导入包
from flask_mail import Mail, Message
from celery import Celery
import requests
import util
import redis
import random
import json
import signal
from functools import wraps
from flask import make_response
 

# 跨域问题的解决方案：
def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        rst.headers['Access-Control-Allow-Credentials'] = 'true'
        return rst
    return wrapper_fun

conn = redis.StrictRedis(host='localhost', port=6379, db=8,decode_responses=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.corp.kuaishou.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_USERNAME'] = "acfunqa@kuaishou.com"
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_PASSWORD'] = ('acfun_QA01')
app.config['MAIL_DEFAULT_SENDER'] = 'acfunqa@kuaishou.com'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/8'
app.config['CELERYD_MAX_TASKS_PER_CHILD'] = 100
app.config['CELERYD_FORCE_EXECV'] = True
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/8'


# Initialize extensions
mail = Mail(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)


@celery.task(bind=True)
def set_chance2(self,pool_id,uid,per_count):
    start_time = time.time()
    print("开始设置2")
    # response = requests.get('http://hb2-acf-staging-ls011.aliyun:31706/test/prize/addDrawTimes?userId=' + str(uid) +'&numberOfDraws=' + str(per_count) + '&prizePoolId=' + str(pool_id) )
    response = requests.get('http://localhost:8885/hello?userId=' + str(uid) + '&numberOfDraws=' + str(per_count) + '&prizePoolId=' + str(pool_id))
    res_text = json.loads(response.text)
    res_success = res_text["success"]
    # print("type",type(json.loads(response.text)["success"]))
    if res_success:
        for i in range(per_count):
            conn.lpush("set_changce_result_"+str(pool_id),uid)
    end_time = time.time()
    if int (end_time - start_time) >= 0.2:
        pass
    else:
        time.sleep(0.2 + start_time - end_time) # 保证每次请求的时间是200ms
    return { 'status': 'Task completed!',
     'result': "success"}




@celery.task(bind=True)
def set_chance(self,pool_id,uid_start,uid_end):
    print("开始设置")
    uids_all = range(int(uid_start),int(uid_end),1)
    # time.sleep(10)
    per_count = 10
    for uid in uids_all:
        # print("haha")
        response = requests.get('http://hb2-acf-staging-ls011.aliyun:31706/test/prize/addDrawTimes?userId=' + str(uid) +'&numberOfDraws=' + str(per_count) + '&prizePoolId=' + str(pool_id) )
        res_text = json.loads(response.text)
        res_success = res_text["success"]
        # print("type",type(json.loads(response.text)["success"]))
        if res_success:
            for i in range(per_count):
                conn.lpush("set_changce_result_"+str(pool_id),uid)
    return { 'status': 'Task completed!',
     'result': "success"}

@celery.task()
def set_mid_chance( pool_id,uid_start,uid_end):
    print("pool_id",pool_id)
    print("uid_start",uid_start)
    print("uid_end",uid_end)
    uids_all = range(int(uid_start), int(uid_end), 1)
    # set_chance.apply_async(args=(pool_id,uid_start,uid_end), queue='set_changce_' + pool_id)
    # 杀掉其他奖池的set_changce worker
    util.kill_other_worker("set_changce_\d+", 'set_changce_' + str(pool_id))
    set_chance_worker_command = 'nohup celery worker -A app.celery --loglevel=INFO -Q set_changce_' + str(pool_id) + ' --concurrency=10 &'
    time.sleep(0.5)
    has_contain, pids = util.has_contain_pid('set_changce_' + str(pool_id))
    if has_contain:
        pass
    else:
        os.system(set_chance_worker_command)
    per_count = 1
    for uid in uids_all:
        set_chance2.apply_async(args=(pool_id, uid, per_count), queue='set_changce_' + pool_id)

    return "set_chance start"
    # 计算开始抽奖的时间
    pool_start_time = '2020-10-10 14:32:00'
    # 转换成时间数组
    timeArray = time.strptime(pool_start_time, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    pool_start_timestamp = time.mktime(timeArray)
    delay_time = int(time.time() - pool_start_timestamp) + 1



    # 杀掉其他奖池的mid worker
    util.kill_other_worker("lucky_draw_mid_\d+", "lucky_draw_mid_" + str(pool_id))
    # 判断是否有draw_mid worker，如果无，通过系统命令启动
    lucky_draw_mid_worker_command = 'nohup celery worker -A app.celery --loglevel=INFO -Q lucky_draw_mid_' + str(
        pool_id) + ' --concurrency=2 &'
    has_contain, pids = util.has_contain_pid('lucky_draw_mid_' + str(pool_id))
    if has_contain:
        pass
    else:
        pass
        # os.system(lucky_draw_mid_worker_command)


    # 杀掉其他奖池的draw worker
    util.kill_other_worker("lucky_draw_\d+", "lucky_draw_" + str(pool_id))
    # 判断是否有draw worker，如果无，通过系统命令启动
    lucky_draw_worker_command = 'nohup celery worker -A app.celery --loglevel=INFO -Q lucky_draw_' + str(pool_id) + ' --concurrency=100 &'
    has_contain, pids = util.has_contain_pid('lucky_draw_' + str(pool_id))
    if has_contain:
        pass
    else:
        os.system(lucky_draw_worker_command)



    delay_time = 200
    draw_task_mid.apply_async(args=(pool_id,), countdown=delay_time, queue='lucky_draw_mid_' + str(pool_id))

    return "set_chance start"

@app.route('/startSstartetChance',methods=['GET'])
def startSetChance():
    pool_id = request.args.get("pool_id")
    uid_start = request.args.get("uid_start")
    uid_end = request.args.get("uid_end")
    if not util.is_num(pool_id) or not util.is_num(uid_start) or not util.is_num(uid_end):
        return {'code':2, 'err_message':'格式不对'}
    uids_cover = request.args.get("uids_cover")
    has_set_changce_mid,pids = util.has_contain_pid("set_changce_mid")

    if has_set_changce_mid:
        print("已经包含了")
        pass
    else:
        print("指定系统命令")
        set_mid_chance_worker_command = 'nohup celery worker -A app.celery --loglevel=INFO -Q set_changce_mid --concurrency=2 &'
        os.system(set_mid_chance_worker_command)
    # if has_set_changce:
    #     print(pids)
    # else:
    #     print(pids)
    print("yunxing ")
    task = set_mid_chance.apply_async(args=(pool_id,uid_start,uid_end), queue='set_changce_mid')
    return {'code':1,"pool_id":pool_id}


@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


@celery.task()
def draw_task_mid(pool_id):
    # 杀掉其他奖池的worker
    util.kill_other_worker("lucky_draw_\d+", "lucky_draw_" + str(pool_id))
    # 判断是否有draw worker，如果无，通过系统命令启动
    lucky_draw_worker_command = 'nohup celery worker -A app.celery --loglevel=INFO -Q lucky_draw_' + str(pool_id) + ' --concurrency=20 &'
    # lucky_draw_worker_command = 'nohup celery worker -A app.celery --loglevel=INFO -Q lucky_draw_' + str(pool_id) + ' &'
    time.sleep(0.5) #
    has_contain, pids = util.has_contain_pid('lucky_draw_' + str(pool_id))
    if has_contain:
        pass
    else:
        pass
        os.system(lucky_draw_worker_command)



    # lucky_draw_worker_command = 'nohup celery worker -A app.celery --loglevel=INFO -Q lucky_draw_' + str(pool_id) + ' --concurrency=10 &'
    # os.system(lucky_draw_worker_command)

    set_changce_result_key = 'set_changce_result_' + str(pool_id)
    drawable_uids = conn.lrange(set_changce_result_key, 0, -1)
    random.shuffle(drawable_uids)
    for uid in drawable_uids:
        draw_task.apply_async(args=('http://localhost:8885/hello?pool_id=' + pool_id + "&uid=" + str(uid), pool_id),queue="lucky_draw_"+str(pool_id))
    # time.sleep(10)


    # 杀掉其他奖池的worker
    util.kill_other_worker("lucky_draw_\d+", "lucky_draw_" + str(pool_id))
    # 判断是否有draw worker，如果无，通过系统命令启动
    lucky_draw_worker_command = 'nohup celery worker -A app.celery --loglevel=INFO -Q lucky_draw_' + str(pool_id) + ' --concurrency=20 &'
    # lucky_draw_worker_command = 'nohup celery worker -A app.celery --loglevel=INFO -Q lucky_draw_' + str(pool_id) + ' &'
    has_contain, pids = util.has_contain_pid('lucky_draw_' + str(pool_id))
    if has_contain:
        pass
    else:
        pass
        os.system(lucky_draw_worker_command)


    return "抽奖触发任务完成"

@celery.task()
def draw_task(request_url, pool_id):
    start_time = time.time()
    print("进入抽奖",request_url)
    response = requests.get(request_url)
    draw_result = json.loads(response.text)
    prize_id = (draw_result["message"])
    conn.lpush('draw_result_' + str(pool_id), str(int(time.time())) + '____'  + str(request_url.split("uid=")[-1].strip()) + '____' + str(prize_id))
    end_time = time.time()
    if int (end_time - start_time) >= 0.2:
        pass
    else:
        time.sleep(0.2 + start_time - end_time) # 保证每次请求的时间是200ms

    return "开始抽奖"



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # send the email
    email_data = {
        'subject': 'Hello from Flask',
        'to': email,
        'body': 'This is a test email sent from a background Celery task.'
    }
    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(email_data)
        flash('Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[email_data], countdown=60, queue="send_mail_delay")
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        if task.state == 'SUCCESS':
            print("SUCCESS", task.info)
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


@app.route('/lucky/draw',methods=['GET'])
def lucky_draw():
    pass
    pool_id = request.args.get("pool_id")
    set_changce_result_key = 'set_changce_result_' + str(pool_id)
    drawable_count = conn.llen(set_changce_result_key)
    draw_result_key = 'draw_result_' + str(pool_id)
    draw_result_count = conn.llen(draw_result_key)
    if draw_result_count>0:
        return {"code": 1, "pool_id": pool_id} # 已经有抽奖，不能再次抽奖
    elif drawable_count==0:
        return {"code": 2, "pool_id": pool_id} # 未设置抽奖机会，不能抽奖
    elif draw_result_count==0 and drawable_count>0 :
        # drawable_uids =

        # 计算开始抽奖的时间
        pool_start_time = '2020-10-10 14:36:00'
        # 转换成时间数组
        timeArray = time.strptime(pool_start_time, "%Y-%m-%d %H:%M:%S")
        # 转换成时间戳
        pool_start_timestamp = time.mktime(timeArray)
        delay_time = int(time.time() - pool_start_timestamp) + 1
        delay_time = 200
        print(delay_time)



        # 杀掉其他奖池的mid worker
        util.kill_other_worker("lucky_draw_mid_\d+", "lucky_draw_mid_" + str(pool_id))
        # 判断是否有draw_mid worker，如果无，通过系统命令启动
        lucky_draw_mid_worker_command = 'nohup celery worker -A app.celery --loglevel=INFO -Q lucky_draw_mid_' + str(pool_id) + ' --concurrency=2 &'
        has_contain, pids = util.has_contain_pid('lucky_draw_mid_' + str(pool_id))
        if has_contain:
            pass
        else:
            os.system(lucky_draw_mid_worker_command)




        # draw_task_mid.apply_async(args=(pool_id,), countdown=delay_time, queue='lucky_draw_mid_'+str(pool_id))

        draw_task_mid.apply_async(args=(pool_id,), queue='lucky_draw_mid_' + str(pool_id))

        return {"code": 0, "pool_id": pool_id} # 开始抽奖任务


@app.route('/test', methods=['GET', 'POST'])
@allow_cross_domain
def test():
    return {"code": 0, "pool_id": 1}


if __name__ == '__main__':
    app.run(debug=True)
