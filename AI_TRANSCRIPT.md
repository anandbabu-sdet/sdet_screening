# AI_TRANSCRIPT.md

**Tools used:**

* ChatGPT (OpenAI)
* Claude (Anthropic)

**Candidate** Anandababu
**Date:** 15-June 2026

**Exercise:** SDET Candidate Screening – TCS / SIX GCC

---

## Summary

I used AI tools to assist with brainstorming, validating approaches, improving code structure, and refining documentation for this exercise.

AI-generated outputs were reviewed, modified where necessary, executed locally, and verified manually.

All submitted code and documentation reflect my final decisions, and I am able to explain, modify, debug, and extend every part of the solution.

---

## Primary Prompt

> Act as a Senior SDET with expertise in Python, SQL, API testing, and test automation.
>
> I have a TCS SDET screening assessment consisting of four sections:
>
> 1. SQL queries involving two product tables
> 2. A Python CSV header comparison tool
> 3. API test case design
> 4. README and AI usage documentation
>
> Generate complete, interview-ready deliverables using Python best practices.
>
> Prioritize simplicity, readability, maintainability, and ease of explanation. Avoid unnecessary framework complexity and keep the solution aligned with a take-home exercise expected to be completed within 2–3 hours.

---

## AI Assistance Used

AI tools assisted with:

* SQL query generation and review
* Python function decomposition
* Error-handling recommendations
* Test case brainstorming
* README structure and wording
* API test design

---

## What I Accepted

* Overall project structure
* SQL query logic
* Separation of CSV parsing and comparison logic
* Unit test approach using pytest
* API test case organization

---

## What I Modified

* Added explanations for NULL-safe SQL comparisons using `IS DISTINCT FROM`.
* Added additional edge-case tests for header comparison.
* Simplified the implementation to align with the exercise requirement of keeping the solution readable and easy to run.
* Updated the README to include assumptions, AI usage disclosure, and candidate acknowledgement.
* Reviewed all naming conventions and console outputs.

---

## What I Verified Manually

### SQL Validation

* Confirmed product 1002 changed price from 38.00 to 35.00.
* Confirmed product 1003 changed price from 19.99 to 21.99.
* Confirmed products 1006 and 1007 are new today.
* Confirmed product 1004 is missing today.
* Confirmed product 1005 changed status from ACTIVE to INACTIVE.

### Python Validation

* Executed the CSV comparison tool locally.
* Verified output against expected results.
* Confirmed error handling for:

  * Missing arguments
  * Missing files
  * Empty files
  * Invalid headers

### Test Validation

* Executed all pytest tests locally.
* Verified all tests pass successfully.

---

## Key Design Decisions

### Separation of Concerns

Core comparison logic is separated from the command-line interface to improve testability and maintainability.

### Standard Library Usage

Only Python standard libraries were used for CSV processing to comply with the exercise requirements.

### Error Handling

The application raises specific exceptions within the business logic and handles user-facing messaging in the CLI layer.

### SQL Strategy

* `INNER JOIN` is used for identifying changes between matching records.
* `LEFT JOIN ... IS NULL` or `NOT EXISTS` is used for set-difference operations.
* NULL-safe comparisons are considered for nullable fields.

---

## Candidate Statement

I confirm that:

* I reviewed all AI-generated content before submission.
* I understand the complete solution.
* I can explain, modify, debug, and extend the submitted code without AI assistance.
* The final submission reflects my own judgment and decisions.
