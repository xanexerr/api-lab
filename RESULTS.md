# API lab results

## Part 0

- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: A Good Quattro Stagioni
- Step 0.12, results of the three runs without a session (optional): Not performed; optional step.
- Step 0.16, blocks of "how many of the three tools are excluded": 0, 1, 2, or 3 excluded tools. The 0-, 1-, and 2-tool cases passed. Excluding all 3 caused the defect below.

## Defect report 1

- Title: Excluding all pizza tools returns an empty server error
- Request: `POST /api/pizza` with `{"excludedTools":["Knife","Pizza cutter","Scissors"]}` and the lab authorization header
- Expected result: HTTP 400 with a JSON error explaining that no pizza can satisfy the request
- Actual result: HTTP 500 Internal Server Error with an empty body, confirmed with `curl.exe`
- Severity: High for API reliability because the client receives no actionable response and the request triggers a server error.

## Defect report 2

- Title: A made-up token can read shared ratings
- Request: `GET /api/ratings` with `Authorization: token 0000000000000000`
- Expected result: HTTP 401 Unauthorized
- Actual result: HTTP 200 with the shared ratings list
- Severity: High because an unauthenticated stranger can read data that the API should protect. A test request also unexpectedly created a rating with a made-up token (HTTP 201); this was an unintended test mistake and no further writes were made with that token.

## Part A

- Step A4, status codes when the other user reads, changes and deletes: 404, 400, 400. The owner could still read the original rating unchanged after each attempt.

## Part B

1. API tests can find integration failures such as a route returning the wrong status or data not being saved correctly by the real server. Stubbed unit tests cannot find failures in the network, server configuration, or real database integration. Unit tests are still useful because they run quickly and isolate logic without depending on the network.
2. Each test creates a unique user so it owns its data and does not interfere with another student's ratings. The same approach in Project 2 is to use a unique test account or unique records for each test and clean up records created by that test.
3. A single session retains the load-balancer cookie so requests continue to the same server, which keeps a newly created user available during login and later requests. The optional three no-session runs were not performed.
4. The defect came from the block where all three tools are excluded. A 500 with an empty body gives the client no useful explanation and can break error handling. The test stays as `xfail` so the defect remains visible and strict mode alerts us if the API fixes it.
5. Base choice needs 9 tests: 1 base test plus 2 other C1 blocks, 3 other C2 blocks, 1 other C3 block, and 2 other C4 blocks. All combinations need 3 × 4 × 2 × 3 = 72 tests.
6. The other user received 404 for reading, 400 for changing, and 400 for deleting. Any 4xx response is acceptable for denying access. The rating remained unchanged for its owner, so these results meet the requirement and are not a defect.
7. The made-up 16-character token received HTTP 200 and the shared ratings list. This is a defect because a stranger can read ratings without logging in. On a real system, the same authorization failure could expose sensitive records. The lab instruction was followed for this probe using GET only.
8. An API test checks response status, headers, and data fields directly and quickly. A browser test can check what a user sees and does on the page, including layout, buttons, and client-side behavior.
