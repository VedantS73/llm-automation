# LLM Automation
<p>
An automation agent that accepts plain‑English tasks, carries out the required (multi‑step) process leveraging an LLM where required. 
</p>

### Build file with
```
docker build -t etherking/llm-automation:latest .
docker login
docker push etherking/llm-automation:latest
```

### Pull
```
podman pull docker.io/etherking/llm-automation:latest
```

### Testing
```
podman run -e AIPROXY_TOKEN=$AIPROXY_TOKEN -p 8000:8000 etherking/llm-automation:latest
<!-- OR -->
podman run --env-file .env -p 8000:8000 etherking/llm-automation:latest
```

### BATCH
```
docker build -t etherking/llm-automation:latest .
docker push etherking/llm-automation:latest
podman pull docker.io/etherking/llm-automation:latest
podman run --env-file .env -p 8000:8000 etherking/llm-automation:latest
```