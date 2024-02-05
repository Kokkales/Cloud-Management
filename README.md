<h1 align="center" id="title">Resource Monitoring in restAPIs</h1>

<p id="description">Monitoring the CPU RAM bandwidth of a restful API.</p>

<h2>🛠️ Installation Steps:</h2>

<p>1. Create Virtual Environment</p>

```
# On macOS/Linux:
python3 -m venv .venv
. .venv/bin/activate

# On Windows:
py -3 -m venv .venv
.venv\Scripts\activate
```

<p>2. Install Necessary Requirements</p>

```
pip install -r ./Other_files/requirements.txt
```

<p>3. Run Server</p>

```
python3 server.py
```

<p>4. Run Simulator</p>

```
python3 main.py 1 a nostress

#exapmle: python3 main.py <#number of experiments> <type of workloads a=all, p=peak, n=normal, s=stable> <stress/nostress>
```

<p>5. Test with different load sizes using locus.io framework</p>
```
$locust
```
After running the command open http://localhost:8089

<h2>💻 Built with</h2>

Technologies used in the project:

- Python
