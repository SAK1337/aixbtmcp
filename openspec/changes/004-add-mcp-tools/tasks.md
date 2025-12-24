# Tasks: Add MCP Tool Endpoints

## 1. Request Models
- [x] 1.1 Add `ChatMessage` model with role and content validation
- [x] 1.2 Add `IndigoRequest` model with message and conversation_history
- [x] 1.3 Add `ListProjectsRequest` model with filter parameters
- [x] 1.4 Add `GetSignalsRequest` model with filter parameters

## 2. Indigo Service
- [x] 2.1 Create `src/mcp_aixbt/services/indigo.py`
- [x] 2.2 Implement `IndigoService` class
- [x] 2.3 Add `chat()` method that constructs messages array
- [x] 2.4 Handle 404 responses gracefully (no information found)
- [x] 2.5 Parse `data.text` from response

## 3. Tools Router
- [x] 3.1 Create `src/mcp_aixbt/routers/tools.py`
- [x] 3.2 Implement `POST /tools/query-indigo` endpoint
- [x] 3.3 Implement `POST /tools/list-projects` endpoint
- [x] 3.4 Implement `POST /tools/get-signals` endpoint
- [x] 3.5 Add request body validation with Pydantic

## 4. Router Registration
- [x] 4.1 Update `main.py` to include tools router
- [x] 4.2 Add router prefix `/tools`
- [x] 4.3 Configure OpenAPI tags

## 5. Error Handling
- [x] 5.1 Handle AIXBT 404 responses (return friendly message)
- [x] 5.2 Handle API errors with appropriate status codes
- [x] 5.3 Validate message content length (max 10000 chars)

## 6. Validation
- [x] 6.1 Write integration tests for query-indigo endpoint
- [x] 6.2 Test conversation history handling
- [x] 6.3 Test list-projects with various filters
- [x] 6.4 Test get-signals with category filters
- [x] 6.5 Test error responses (invalid input, API errors)
