# Tasks: Add MCP Tool Endpoints

## 1. Request Models
- [ ] 1.1 Add `ChatMessage` model with role and content validation
- [ ] 1.2 Add `IndigoRequest` model with message and conversation_history
- [ ] 1.3 Add `ListProjectsRequest` model with filter parameters
- [ ] 1.4 Add `GetSignalsRequest` model with filter parameters

## 2. Indigo Service
- [ ] 2.1 Create `src/mcp_aixbt/services/indigo.py`
- [ ] 2.2 Implement `IndigoService` class
- [ ] 2.3 Add `chat()` method that constructs messages array
- [ ] 2.4 Handle 404 responses gracefully (no information found)
- [ ] 2.5 Parse `data.text` from response

## 3. Tools Router
- [ ] 3.1 Create `src/mcp_aixbt/routers/tools.py`
- [ ] 3.2 Implement `POST /tools/query-indigo` endpoint
- [ ] 3.3 Implement `POST /tools/list-projects` endpoint
- [ ] 3.4 Implement `POST /tools/get-signals` endpoint
- [ ] 3.5 Add request body validation with Pydantic

## 4. Router Registration
- [ ] 4.1 Update `main.py` to include tools router
- [ ] 4.2 Add router prefix `/tools`
- [ ] 4.3 Configure OpenAPI tags

## 5. Error Handling
- [ ] 5.1 Handle AIXBT 404 responses (return friendly message)
- [ ] 5.2 Handle API errors with appropriate status codes
- [ ] 5.3 Validate message content length (max 10000 chars)

## 6. Validation
- [ ] 6.1 Write integration tests for query-indigo endpoint
- [ ] 6.2 Test conversation history handling
- [ ] 6.3 Test list-projects with various filters
- [ ] 6.4 Test get-signals with category filters
- [ ] 6.5 Test error responses (invalid input, API errors)
