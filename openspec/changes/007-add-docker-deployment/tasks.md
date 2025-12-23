# Tasks: Add Docker Deployment Configuration

## 1. Dockerfile
- [ ] 1.1 Create multi-stage Dockerfile with builder and runtime stages
- [ ] 1.2 Use python:3.11-slim as base image
- [ ] 1.3 Install dependencies in builder stage
- [ ] 1.4 Copy only necessary files to runtime stage
- [ ] 1.5 Configure non-root user for security
- [ ] 1.6 Set health check using `/health/live` endpoint
- [ ] 1.7 Expose port 8000

## 2. Docker Compose
- [ ] 2.1 Create `docker-compose.yml` for development
- [ ] 2.2 Configure environment variable mapping
- [ ] 2.3 Add volume mount for local development
- [ ] 2.4 Configure port mapping (8000:8000)
- [ ] 2.5 Add health check configuration

## 3. Environment Configuration
- [ ] 3.1 Create `.env.example` with all settings documented
- [ ] 3.2 Include AIXBT_API_KEY placeholder
- [ ] 3.3 Include optional EVM_PRIVATE_KEY for x402
- [ ] 3.4 Document LOG_LEVEL and LOG_FORMAT options
- [ ] 3.5 Document budget control settings

## 4. Build Optimization
- [ ] 4.1 Create `.dockerignore` file
- [ ] 4.2 Exclude tests, docs, .git, __pycache__
- [ ] 4.3 Exclude development files (.env, *.pyc)
- [ ] 4.4 Include only necessary source files

## 5. Security Hardening
- [ ] 5.1 Run container as non-root user
- [ ] 5.2 Use read-only filesystem where possible
- [ ] 5.3 Drop unnecessary capabilities
- [ ] 5.4 Set appropriate file permissions

## 6. Validation
- [ ] 6.1 Build Docker image successfully
- [ ] 6.2 Verify health checks pass in container
- [ ] 6.3 Test docker-compose up workflow
- [ ] 6.4 Verify environment variables are loaded
- [ ] 6.5 Test container restart behavior
- [ ] 6.6 Verify image size is optimized (< 200MB target)
