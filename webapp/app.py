from flask import Flask, render_template, request, redirect, url_for
import os
import json
import socket
import requests

app = Flask(__name__)

NGINX_CONF_DIR = '/nginx/conf.d'
CONFIG_DATA_FILE = 'config_data.json'

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except:
        return "Could not determine IP"

def save_config_data(name, domain, target_host, target_port):
    data = {}
    if os.path.exists(CONFIG_DATA_FILE):
        with open(CONFIG_DATA_FILE, 'r') as f:
            data = json.load(f)
    
    data[name] = {
        'domain': domain,
        'target_host': target_host,
        'target_port': target_port,
    }
    
    with open(CONFIG_DATA_FILE, 'w') as f:
        json.dump(data, f)

def get_config_data():
    if os.path.exists(CONFIG_DATA_FILE):
        with open(CONFIG_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_proxy_config(name, domain, target_host, target_port):
    config_content = f"""server {{
    listen 80;
    server_name {domain};

    location / {{
        proxy_pass http://{target_host}:{target_port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}"""
    with open(os.path.join(NGINX_CONF_DIR, f"{name}.conf"), 'w') as f:
        f.write(config_content)
    
    save_config_data(name, domain, target_host, target_port)

def get_existing_configs():
    configs = {}
    config_data = get_config_data()
    
    for filename in os.listdir(NGINX_CONF_DIR):
        if filename.endswith('.conf') and filename != 'default.conf':
            name = filename[:-5]  # Remove .conf extension
            if name in config_data:
                configs[name] = config_data[name]
            else:
                configs[name] = {
                    'domain': 'Unknown',
                    'target_host': 'Unknown',
                    'target_port': 'Unknown'
                }
    return configs

@app.route('/')
def index():
    configs = get_existing_configs()
    public_ip = get_public_ip()
    local_ip = socket.gethostbyname(socket.gethostname())
    return render_template('index.html', configs=configs, public_ip=public_ip, local_ip=local_ip)

@app.route('/add_proxy', methods=['POST'])
def add_proxy():
    name = request.form['name']
    domain = request.form['domain']
    target_host = request.form['target_host']
    target_port = request.form['target_port']
    
    save_proxy_config(name, domain, target_host, target_port)
    
    # Reload Nginx to apply the changes
    os.system('nginx -s reload')
    return redirect(url_for('index'))

@app.route('/delete_proxy/<name>')
def delete_proxy(name):
    config_file = os.path.join(NGINX_CONF_DIR, f"{name}.conf")
    if os.path.exists(config_file):
        os.remove(config_file)
        
        # Remove from config data
        data = get_config_data()
        if name in data:
            del data[name]
            with open(CONFIG_DATA_FILE, 'w') as f:
                json.dump(data, f)
        
        # Reload Nginx to apply the changes
        os.system('nginx -s reload')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 