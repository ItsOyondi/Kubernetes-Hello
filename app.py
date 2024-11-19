from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return """
            Kubernetes "Hello World" Application.
            Using hello-world YAML file to deploy simple "Hello World" equivalent application
            on already setup kubernetes cluster.
            more details can be found at Medium Blog,
            https://medium.com/@bhargavshah2011/hello-world-on-kubernetes-cluster-6bec6f4b1bfd
            Thank You.
            """
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
