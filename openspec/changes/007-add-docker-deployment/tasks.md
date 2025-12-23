# Tasks: Add Docker Deployment Configuration

## 1. Dockerfile
- [x] 1.1 Create multi-stage Dockerfile with builder and runtime stages
- [x] 1.2 Use python:3.11-slim as base image
- [x] 1.3 Install dependencies in builder stage
- [x] 1.4 Copy only necessary files to runtime stage
- [x] 1.5 Configure non-root user for security
- [x] 1.6 Set health check using `/health/live` endpoint
- [x] 1.7 Expose port 8000

## 2. Docker Compose
- [x] 2.1 Create `docker-compose.yml` for development
- [x] 2.2 Configure environment variable mapping
- [x] 2.3 Add volume mount for local development
- [x] 2.4 Configure port mapping (8000:8000)
- [x] 2.5 Add health check configuration

## 3. Environment Configuration
- [x] 3.1 Create `.env.example` with all settings documented
- [x] 3.2 Include AIXBT_API_KEY placeholder
- [x] 3.3 Include optional EVM_PRIVATE_KEY for x402
- [x] 3.4 Document LOG_LEVEL and LOG_FORMAT options
- [x] 3.5 Document budget control settings

## 4. Build Optimization
- [x] 4.1 Create `.dockerignore` file
- [x] 4.2 Exclude tests, docs, .git, __pycache__
- [x] 4.3 Exclude development files (.env, *.pyc)
- [x] 4.4 Include only necessary source files

## 5. Security Hardening
- [x] 5.1 Run container as non-root user
- [x] 5.2 Use read-only filesystem where possible
- [x] 5.3 Drop unnecessary capabilities
- [x] 5.4 Set appropriate file permissions

## 6. Validation
- [x] 6.1 Build Docker image successfully
- [x] 6.2 Verify health checks pass in container
- [x] 6.3 Test docker-compose up workflow
- [x] 6.4 Verify environment variables are loaded
- [x] 6.5 Test container restart behavior
- [x] 6.6 Verify image size is optimized (< 200MB target)
