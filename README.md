# Emotional Drift Detection Simulation

**Project by:** Matthew Marietta
**Date:** July 25, 2025

---

## 1. Project Overview

I built a program that simulates a team's chat conversation, like you'd see in Slack. Its main job is to read the chat in real-time and automatically spot when the conversation starts to become unhealthy or when team members are getting frustrated with each other. I focused on making the code clean and easy to understand, so you can see exactly why it makes a decision. I also built it in a flexible way, so different parts can be upgraded or swapped out later. I included the bonus features, too: a fake 'heart rate' signal to show stress, and a log file that keeps a permanent record of the most serious problems.

---

## 2. My Scoring Logic

My system figures out if a message is "negative" in a few steps, starting simple and getting smarter as it gathers more context.

#### The Foundation: A "Red Flag" Dictionary

First, the system has a built-in list of words and phrases that are red flags in a workplace chat. Things like "whatever," "must be nice," or "I guess." Each phrase has a pre-defined score based on how problematic it is, which was easy to map with the script. This provides the initial, foundational analysis for every message. In addition to this, the setup allowed me to test easily and reproduce the same results over and over for observability.


| Signal Phrase           | Score | Reason / Detected Pattern                           |
| ----------------------- | ----- | --------------------------------------------------- |
| `"must be nice"`        | 0.93  | High passive-aggressive tone detected.              |
| `"sure, whatever"`      | 0.90  | Dismissive and confrontational.                     |
| `"you know what"`       | 0.85  | Defensive and confrontational.                      |
| `"whatever"`            | 0.84  | Dismissive tone, can be rude to colleagues.         |
| `"i thought"`           | 0.72  | Potential contradiction or blame-shifting.          |
| `"per my last message"` | 0.70  | Passive-aggressive; implies 'you didn't read'.      |
| `"it's fine"`           | 0.66  | Passive-aggressive tone.                            |
| `"a 'snag'?"`           | 0.62  | Sarcastic questioning; challenges competence.       |
| `"just circling back"`  | 0.61  | Passive-aggressive follow-up; implies lateness.     |
| `"noted."`              | 0.53  | Dismissive acknowledgement.                         |
| `"swamped"`             | 0.50  | Avoiding responsibility in some cases.              |
| `"i guess"`             | 0.40  | Reluctance or lack of buy-in.                       |
| `"making progress"`     | 0.30  | Ambiguous update, not very informative.             |

#### B. Looking for Patterns

A single negative message isn't always a disaster; the real problems are in the patterns. While the calculations are simple, they effectively model the patterns of a real conversation. On top of the basic score, the system adds penalties for three specific situations:

Consistent Negativity: If someone sends a negative message (score > 0.5), and their last message was also negative, they get a +0.1 penalty. This catches users who are being difficult over and over again. This was done with a simple if statement check.

Suddenly Snapping: If someone seems perfectly fine one moment (last score < 0.2) and then suddenly sends a very negative message (current score > 0.7), the system flags this as a critical event by setting the score to 1.0.

"Body Language" (The Bonus): This was the hardest part for me to figure out, as in how it would affect the scoring. The system also looks at a fake heart rate signal (HRV). If someone says something moderately negative (score > 0.4) AND their HRV is low (a sign of stress), it adds a +0.1 penalty. It's like seeing someone say "I'm fine" through gritted teeth—the body language helps confirm the real meaning.

---

## 3. How I Simulated Different Personalities

To create a realistic simulation, I designed three distinct user personas and crafted a pre-written, 31-message script that tells a coherent story of a team's communication degrading.

* **Priya (The Proactive Project Lead):** Her communication is direct, clear, and focused on resolving issues. She acts as the anchor, trying to maintain balance and coherence.
* **Ben (The Avoidant Developer):** When under pressure, he gives vague updates ("making progress"), deflects commitment ("I'm swamped"), and becomes defensive.
* **Sara (The Passive-Aggressive QA):** She is precise and detail-oriented, but when blocked, her frustration manifests as sarcasm (`"A 'snag'?"`), dismissiveness (`"noted."`), and passive-aggression (`"Must be nice"`).

Using a scripted narrative instead of random messages allows the simulation to effectively model how "meaning drift" occurs within the context of a real, evolving conversation. It also allows for easier testing and when to expect something. Ben and Sara are conflicting the most when Priya tries to resolve their conversation.

---

## 4. Where Real-Time AI Would Enhance This

This system was intentionally built with a deterministic, rule-based engine to prioritize **observability**. However, in a production environment, real-time AI should be swapped in to enhance the system in some areas:

1.  **A More Nuanced Scoring Engine:** While the current engine is transparent, it can't detect sarcasm or frustration that doesn't use a keyword. It might also mark something that is not meant in a negative way, which all depends on the context. A fine-tuned model or AI that could understand the full context of the conversation and catch more subtle problems would perform much better. Introducing a new engine file that uses an AI brain would perform much better and be a lot more scalable.  
2.  **Automated, Helpful Interventions:** The current system's output is a `warning_message`. Right now, my system just raises a red flag. A true AI agent could see that flag and then post a helpful, neutral message in the chat to try and fix the problem, like saying, 'Hey, let's quickly clarify who owns this task.' It could actively help the team get back on track." This would have a lot more meaning and be beneficial for the team in a hostile environment.

---

## 5. How to Run the Project

1.  Ensure you have Python 3 installed.
2.  Place all `.py` files (`main.py`, `data_simulator.py`, `scoring_engine.py`, `biometric.py`) in the same directory.
3.  Run the main simulation file from your terminal:
    ```bash
    python main.py
    ```
4.  Flagged events will be printed to the console and also stored in the `misalignment_log.json` file.

---

## Thank you for taking the time to read this document!
