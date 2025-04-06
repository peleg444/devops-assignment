# DevOps Assignment - Flask + MySQL + NGINX with Docker Compose

## 🌐 Overview
This project demonstrates a full DevOps-style deployment using Docker Compose. It includes:
- Python Flask web application
- MySQL database
- NGINX as a load balancer
- Cookie-based stickiness engine
- Scaling via Docker Compose

---

## 📚 Project Structure
```
.
├── my_app/                 # Flask application source code
│   ├── app.py              # Main Python server file
│   ├── Dockerfile          # Builds Flask app container
│   └── requirements.txt    # Python dependencies
├── nginx/
│   └── nginx.conf          # NGINX load balancer configuration
├── docker-compose.yml      # Orchestration for all services
├── scale_to_5.sh           # Bash script to scale app to 5 instances
```

---

## ⚙️ How to Run
1. **Build and start the system:**
   ```bash
   docker-compose down --volumes --remove-orphans
   docker-compose build --no-cache
   ./scale_to_5.sh
   ```

2. **Go to your browser:**
   ```
   http://localhost/
   ```
   You will see:
   ```
   Internal IP: <container internal IP>
   ```

3. **Check cookies:**
   - Open browser dev tools → Application → Cookies
   - See `server_ip` with internal IP

4. **Go to:**
   ```
   http://localhost/showcount
   ```
   See the global counter value.

5. **Scale to 10 replicas:**
   ```bash
   docker-compose up -d --scale app=10
   ```

---

## 🤔 Stickiness Behavior
- The application creates a cookie named `server_ip` with the container's internal IP.
- Cookie expiration: 5 minutes
- NGINX does **not** natively support cookie-based stickiness without third-party modules (e.g. NGINX Plus or Lua scripting).

> ✅ This project fulfills the requirement by managing stickiness at the application level.

---

## 📚 Technologies Used
- Python 3.11 + Flask
- MySQL 5.7
- NGINX (official image)
- Docker Compose v3

---

## 📂 DB Structure
### Table: `access_log`
- `id` (INT, AUTO_INCREMENT)
- `client_ip` (VARCHAR)
- `internal_ip` (VARCHAR)
- `access_time` (DATETIME)

### Table: `counter`
- `id` (INT)
- `count` (INT)

---

## 🔄 Cleanup
To remove all services, volumes, and networks:
```bash
docker-compose down --volumes --remove-orphans
```

---

## ✨ Author
Peleg Gidasi