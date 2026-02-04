---
name: cloudflare-tunnel
description: "Manage and create Cloudflare Tunnels to expose local ports to the internet."
---

# Cloudflare Tunnel Skill

Use this skill to expose local services to the internet using `cloudflared`.

## Prerequisites

- `cloudflared` installed (for direct binary use) OR Docker installed.
- Cloudflare account with a configured domain.

## Deployment Options

### 1. Direct Binary (Current Local Setup)
Run directly on the host. This is how the tunnel is currently running on this system:
```bash
cloudflared --no-autoupdate tunnel run --token <YOUR_TOKEN>
```

### 2. Docker (Recommended for isolation)
Run the tunnel as a lightweight container.

**One-liner:**
```bash
docker run -d --name cloudflare-tunnel cloudflare/cloudflared:latest tunnel --no-autoupdate run --token <YOUR_TOKEN>
```

**Docker Compose:**
Create a `docker-compose.yml`:
```yaml
services:
  tunnel:
    container_name: cloudflare-tunnel
    image: cloudflare/cloudflared:latest
    restart: always
    command: tunnel --no-autoupdate run --token ${TUNNEL_TOKEN}
```
Run with: `TUNNEL_TOKEN=your_token_here docker-compose up -d`

## Manual Setup (CLI)

### 1. Login
Authenticate the CLI with your Cloudflare account:
```bash
cloudflared tunnel login
```

### 2. Create a Tunnel
```bash
cloudflared tunnel create <TUNNEL_NAME>
```

### 3. Configure Ingress Rules
Create/edit `~/.cloudflared/config.yml`:
```yaml
tunnel: <TUNNEL_ID_OR_NAME>
credentials-file: /home/USER/.cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: your-service.yourdomain.com
    service: http://localhost:8080
  - service: http_status:404
```

### 4. Create DNS Route
```bash
cloudflared tunnel route dns <TUNNEL_NAME> your-service.yourdomain.com
```

### 5. Run the Tunnel
```bash
cloudflared tunnel run <TUNNEL_NAME>
```

## Maintenance
- **List tunnels:** `cloudflared tunnel list`
- **Check status:** `cloudflared tunnel info <TUNNEL_NAME>`
- **Delete tunnel:** `cloudflared tunnel delete <TUNNEL_NAME>`
