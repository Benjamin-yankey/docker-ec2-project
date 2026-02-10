# Evidence Directory

Store test outputs and evidence files here.

## Required Evidence Files

- `docker-ps.txt` - Container status
- `docker-logs-web.txt` - Web container logs
- `docker-logs-db.txt` - Database container logs
- `api-responses.txt` - API endpoint responses

## Collect Evidence

```bash
# Use automated script
./collect-evidence.sh

# Or manually:
docker-compose ps > evidence/docker-ps.txt
docker-compose logs web > evidence/docker-logs-web.txt
docker-compose logs db > evidence/docker-logs-db.txt
curl http://localhost:5000/api/health > evidence/api-health.txt
```
