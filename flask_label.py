from flask import Flask, render_template, url_for,request
app = Flask(__name__)
import os
import json

@app.route('/')
def hello_world():
    return render_template('choose.html')

@app.route('/action')
def action():
    action = request.args.get('action')
    start = "http://140.116.39.73:5000/static/" + action + '/';
    file_path = "/media/ts/data/hand_standalone/static/" + action + '/'
    file_name = []
    for root, dirs, files in os.walk(file_path):
        for f in files:
            if f.endswith('.jpg'):
                if not os.path.exists(file_path + f[:-4] + "_label.json"):
                    file_name.append(f)

    print(file_name)
    return render_template('index.html' , action=action,file_name=file_name, start=start, length=len(file_name))

@app.route('/label_data', methods=['POST'])
def label_data_post():
    name = request.values['name']
    print(name)
    action_type = ''
    if( 'assemble' in name ) :
        action_type = 'assemble'
    if ('keyboard' in name):
        action_type = 'keyboard'
    if ('measure' in name):
        action_type = 'measure'
    if ('mouse' in name):
        action_type = 'mouse'
    if ('padding' in name):
        action_type = 'padding'
    if ('tablet' in name):
        action_type = 'tablet'

    os.chdir('/media/ts/data/hand_standalone/static/' + action_type)

    correct = request.values['correct']
    other = request.values['other']
    error = request.values['error']

    handkps = []
    with open( name[:-4] + '.json', 'r') as reader:
        jf = json.loads(reader.read())
        handkps = jf['handkps']
        reader.close()

    handData = {'action': '', 'correct': [], 'error':[], 'other':[] }
    handData['action'] = action_type
    if correct != "":
        for c in correct :
            handData["correct"].append(handkps[int(c)-1])

    if error != "":
        for c in error :
            handData["error"].append(handkps[int(c)-1])

    if other != "":
        for c in other :
            handData["other"].append(handkps[int(c)-1])

    jsonobj = json.dumps(handData)
    with open(name[:-4] + "_label.json", 'w') as fp:
        fp.write(jsonobj)
        fp.close()

    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)