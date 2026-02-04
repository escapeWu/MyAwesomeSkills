---
name: cloudflare-tunnel
description: Manage and create Cloudflare Tunnels (Argo Tunnel) to expose local ports to the internet. Use when you need to set up remote access for local services like WebChat or Nginx without opening firewall ports.
---

# Cloudflare Tunnel

Expose local services to the internet securely via `cloudflared`.

## Workflows

### 🚀 Quick Start (Token-based)

If you already have a tunnel token from the Cloudflare Dashboard:

- **Docker (Isolated)**:
  ```bash
  docker run -d --name cloudflare-tunnel cloudflare/cloudflared:latest tunnel --no-autoupdate run --token <YOUR_TOKEN>
  ```
- **Direct Binary**:
  ```bash
  cloudflared --no-autoupdate tunnel run --token <YOUR_TOKEN>
  ```

### 🛠️ Manual Setup (CLI)

1.  **Login**: `cloudflared tunnel login`
2.  **Create**: `cloudflared tunnel create <name>`
3.  **Route**: `cloudflared tunnel route dns <name> <hostname>`
4.  **Run**: `cloudflared tunnel run <name>`

## Maintenance

- **List Tunnels**: `cloudflared tunnel list`
- **Check Status**: `cloudflared tunnel info <name>`
