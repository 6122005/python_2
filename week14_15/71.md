# VoiceHR - Product Specification (Day 71)

## 1. User Story
As an Indian factory worker, I want to ask HR how many leave days I have remaining using a voice note in my native language, so that I don't have to navigate a confusing English app or wait in line outside the manager's office.

## 2. Core Features
- **Intent Classification:** AI determines if the user is asking a policy question ("What is the Diwali bonus?") or a transactional question ("How many sick leaves do I have?").
- **Data Lookup:** Agent securely checks the local JSON database for the user's specific leave balance.
- **Leave Application:** Agent can process a leave request ("I want to take off tomorrow") and update the JSON database to deduct the balance.

## 3. What it will NOT do (Out of Scope for v1)
- It will NOT handle payroll disbursement or show salary slips.
- It will NOT support languages other than Hindi and English for the first release (to ensure prompt accuracy).
- It will NOT connect to WhatsApp directly yet (we will build the terminal/CLI version first to validate the logic).

## 4. Edge Cases Handled
- **Insufficient Leave Balance:** If a worker asks for 5 days of leave but only has 2, the AI must politely decline and state the exact remaining balance.
- **Unclear Intents:** If the AI doesn't understand the voice note, it will ask for clarification instead of guessing.

## 5. Success Metric
**"10 users using it"** means:
- 10 distinct factory workers successfully query their leave balance OR apply for a leave via the terminal interface without supervisor intervention, within a 7-day period.
