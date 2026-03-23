# API Test Coverage Gap Analysis

**Date**: 2026-03-22
**Status**: Test files created, ready for execution
**Scope**: API Middleware and Routes

## Executive Summary

The codebase has extensive E2E and integration tests via Playwright but **lacks unit tests for critical middleware components**. The middleware layer (authentication, error handling, rate limiting, logging) is tested only indirectly through E2E tests.

## Coverage Summary

| Module | File | Functions/Classes | Tested? | Priority |
|--------|------|-------------------|---------|----------|
| **auth.ts** | `src/api/middleware/auth.ts` | `authMiddleware`, `requireRoles`, `requirePermissions` | ❌ No | **CRITICAL** |
| **error-handler.ts** | `src/api/middleware/error-handler.ts` | `AppError` hierarchy, `errorHandler`, `notFoundHandler`, `asyncHandler` | ❌ No | **CRITICAL** |
| **rate-limiter.ts** | `src/api/middleware/rate-limiter.ts` | `rateLimiter`, `rateLimitByUser`, `incrementRedisCounter` | ❌ No | **HIGH** |
| **logger.ts** | `src/api/middleware/logger.ts` | `requestLogger`, `logAuditEvent`, helpers | ❌ No | **HIGH** |
| **health.ts** | `src/api/routes/health.ts` | `/, /detailed, /ready, /live` endpoints | ❌ No | **MEDIUM** |

## Test Files Created

All test skeletons have been created in the appropriate locations:

### 1. Authentication Tests
**File**: `src/api/middleware/__tests__/auth.test.ts`
- Tests for `authMiddleware` authentication flow
- Tests for `requireRoles` role-based access control
- Tests for `requirePermissions` permission-based access control
- Mock setup for Auth0 authentication

### 2. Error Handler Tests
**File**: `src/api/middleware/__tests__/error-handler.test.ts`
- Tests for error class hierarchy (AppError, ValidationError, NotFoundError, etc.)
- Tests for error handler middleware response formatting
- Tests for `notFoundHandler` 404 handling
- Tests for `asyncHandler` wrapper

### 3. Rate Limiter Tests
**File**: `src/api/middleware/__tests__/rate-limiter.test.ts`
- Tests for IP-based rate limiting
- Tests for user-based rate limiting
- Tests for Redis fallback behavior
- Tests for rate limit exceeded scenarios

### 4. Logger Tests
**File**: `src/api/middleware/__tests__/logger.test.ts`
- Tests for request logging
- Tests for audit event logging
- Tests for helper functions (getActionType, getResourceType, getResourceId)

### 5. Health Endpoint Tests
**File**: `src/api/routes/__tests__/health.test.ts`
- Tests for basic health endpoint (`/`)
- Tests for detailed health endpoint (`/detailed`)
- Tests for readiness endpoint (`/ready`)
- Tests for liveness endpoint (`/live`)

### 6. Middleware Stack Integration Tests
**File**: `src/api/middleware/__tests__/middleware-stack.integration.test.ts`
- Tests for middleware chaining
- Tests for error propagation
- Tests for context preservation across middlewares

## Test Execution

To run the tests once they are properly configured:

```bash
# Run middleware unit tests
npm run test:unit -- src/api/middleware/__tests__

# Run with coverage
npm run test:coverage -- src/api/middleware/__tests__

# Run specific test file
npx vitest run src/api/middleware/__tests__/auth.test.ts
```

## Expected Coverage

After implementation, these tests should provide:
- **auth.ts**: 95%+ coverage
- **error-handler.ts**: 100% coverage
- **rate-limiter.ts**: 90%+ coverage
- **logger.ts**: 85%+ coverage
- **health.ts**: 100% coverage

## Next Steps

1. **Verify test file placement** - Ensure test files are in correct locations
2. **Run test suite** - Execute tests and fix any implementation mismatches
3. **Add missing implementations** - Create actual middleware implementations if needed
4. **Integrate into CI/CD** - Add middleware tests to continuous integration pipeline
5. **Monitor coverage** - Track coverage metrics and add tests for edge cases

## Test Design Notes

### Mocking Strategy
- Auth0 authentication mocked via `vi.mock()`
- Redis client mocked for rate limiting tests
- Express Request/Response objects mocked with vitest
- Database connections mocked for health endpoint tests

### Test Patterns
- Follow existing project patterns from `src/lib/` tests
- Use Vitest framework (project standard)
- Mock external dependencies (Redis, Auth0, databases)
- Test both success and failure scenarios
- Include edge cases (empty headers, missing tokens, etc.)

### Integration Notes
- Tests designed to run in isolation without real database
- Middleware tests use mocked Request/Response objects
- Health endpoint tests use fetch API with mocked services
- Integration tests verify middleware stack behavior

## Related Documentation

- Main analysis: `/TEST-COVERAGE-ANALYSIS.md` (if exists)
- Existing test patterns: `src/lib/ai/bias-detection/__tests__/`
- Playwright E2E tests: `tests/e2e/`
- API security tests: `tests/api/api-security.spec.ts`
